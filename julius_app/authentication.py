from rest_framework.authentication import TokenAuthentication as DRFTokenAuthentication


class TokenAuthentication(DRFTokenAuthentication):
    """
    Simple token based authentication.
    """

    keyword = 'Bearer'
