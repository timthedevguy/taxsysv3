from social_core.backends.oauth import BaseOAuth2


class SSODotteOAuth2(BaseOAuth2):
    """TEST SSODotte Backend"""
    name = 'ssodotte'
    BASE_URL = 'https://sso.pleaseignore.com/auth/realms/auth-ng/protocol/openid-connect'
    AUTHORIZATION_URL = BASE_URL + '/auth'
    ACCESS_TOKEN_URL = BASE_URL + '/token'
    ID_KEY = 'sub'
    ACCESS_TOKEN_METHOD = 'POST'
    STATE_PARAMETER = False
    REDIRECT_STATE = False
    EXTRA_DATA = [
        ('CharacterID', 'id'),
        ('expires_in', 'expires'),
        ('CharacterOwnerHash', 'owner_hash', True),
        ('refresh_token', 'refresh_token', True),
    ]

    def get_user_details(self, response):
        """Return user details from EVE Online account"""
        user_data = self.user_data(response['access_token'])
        fullname, first_name, last_name = self.get_user_names(
                user_data['CharacterName']
        )
        return {
            'email'     : '',
            'username'  : fullname,
            'fullname'  : fullname,
            'first_name': first_name,
            'last_name' : last_name,
        }

    def user_data(self, access_token, *args, **kwargs):
        """Get Character data from EVE server"""
        return {'CharacterName': 'Fecal Matters'}

