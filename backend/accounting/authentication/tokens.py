from rest_framework_simplejwt.tokens import AccessToken, BlacklistMixin


class MyAccessToken(AccessToken, BlacklistMixin):
    ...
