from typing import Dict


def paginate_serializer(page, size, data, data_key_name="data") -> Dict:
    return {
        "page": page,
        "size": size,
        data_key_name: data
    }
