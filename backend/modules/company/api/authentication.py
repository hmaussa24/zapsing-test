from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication


class CompanyJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        # No usamos el modelo de usuario de Django; devolvemos AnonymousUser
        # y trabajamos con claims (company_id) vía utilidades propias.
        return AnonymousUser()


