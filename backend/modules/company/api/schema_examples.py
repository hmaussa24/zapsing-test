from drf_spectacular.utils import OpenApiExample


EXAMPLE_CREATE_REQUEST = OpenApiExample(
    "Solicitud de creación",
    summary="Body de ejemplo",
    value={"name": "Acme Corp", "api_token": "token-123"},
    request_only=True,
)

EXAMPLE_CREATE_RESPONSE = OpenApiExample(
    "Respuesta de creación",
    summary="Respuesta de ejemplo",
    value={"id": 1, "name": "Acme Corp", "api_token": "token-123"},
    response_only=True,
)

EXAMPLE_UPDATE_REQUEST = OpenApiExample(
    "Actualización parcial",
    summary="Body parcial",
    value={"name": "Acme Updated"},
    request_only=True,
)


