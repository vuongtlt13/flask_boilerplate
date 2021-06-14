import inspect
import sys
from typing import Optional, Any

from flask import Request, Flask
from flask_jwt_extended.exceptions import NoAuthorizationError
from werkzeug.exceptions import HTTPException

from abc import abstractmethod


class BaseMiddleware(object):
    @abstractmethod
    def handle(self, request: Request):
        pass


class MiddlewareManager(object):
    def __init__(self, flask_app: Flask = None):
        self.flask_app = flask_app
        self.wsgi_app = None
        self.middleware_map = {}
        if flask_app:
            self.init_app(flask_app)

    def init_app(self, flask_app):
        self.flask_app = flask_app
        self.wsgi_app = flask_app.wsgi_app
        flask_app.wsgi_app = self

    def __call__(self, environ, start_response):
        """The actual WSGI application. This is not implemented in
        :meth:`__call__` so that middlewares can be applied without
        losing a reference to the app object. Instead of doing this::

            app = MyMiddleware(app)

        It's a better idea to do this instead::

            app.wsgi_app = MyMiddleware(app.wsgi_app)

        Then you still have the original application object around and
        can continue to call methods on it.

        .. versionchanged:: 0.7
            Teardown events for the request and app contexts are called
            even if an unhandled error occurs. Other events may not be
            called depending on when an error occurs during dispatch.
            See :ref:`callbacks-and-errors`.

        :param environ: A WSGI environment.
        :param start_response: A callable accepting a status code,
            a list of headers, and an optional exception context to
            start the response.
        """
        ctx = self.flask_app.request_context(environ)
        error = None
        try:
            try:
                ctx.push()
                resp = self.go_through_middlewares(ctx.request)
                if resp:
                    response = self.flask_app.finalize_request(resp)
                else:
                    response = self.flask_app.full_dispatch_request()
            except Exception as e:
                error = e
                response = self.flask_app.handle_exception(e)
            except:  # noqa: B001
                error = sys.exc_info()[1]
                raise
            return response(environ, start_response)
        finally:
            if self.flask_app.should_ignore_error(error):
                error = None
            ctx.auto_pop(error)

    def route_middleware(self, middleware_class, *args, **kwargs):
        """
        A decorator to add middleware for a route.
        """
        assert inspect.isclass(middleware_class), f"{middleware_class} not is class"
        if not issubclass(middleware_class, BaseMiddleware):
            raise ValueError(f"{middleware_class.__name__} not is subclass of {BaseMiddleware.__name__}")
        middleware_instance = middleware_class(*args, **kwargs)

        def wrapper(cls):
            class_name = f"{cls.__module__}.{cls.__name__}"
            if class_name not in self.middleware_map:
                self.middleware_map[class_name] = []
            self.middleware_map[class_name].append(middleware_instance)
            return cls

        return wrapper

    def __extract_request(self, environ) -> Request:
        request: Request = self.flask_app.request_class(environ)
        url_adapter = self.flask_app.create_url_adapter(request)
        try:
            result = url_adapter.match(return_rule=True)
            request.url_rule, request.view_args = result
            print('path: %s, url: %s' % (request.path, request.url))
            return request
        except HTTPException as e:
            return request
        except:
            raise

    def go_through_middlewares(self, request: Request) -> Optional[Any]:
        middlewares = self.get_middlewares(request)
        for middleware in middlewares:
            error = middleware.handle(request)
            if error:
                return error
        return None

    def get_middlewares(self, request: Request):
        view_function = self.flask_app.view_functions.get(request.url_rule.endpoint, None)
        if hasattr(view_function, '__self__'):
            cls = view_function.__self__.__class__
        elif hasattr(view_function, 'view_class'):
            cls = view_function.view_class
        else:
            raise ValueError(f"Can't find middlewares!")

        class_name = f"{cls.__module__}.{cls.__name__}"
        return self.middleware_map.get(class_name, [])
