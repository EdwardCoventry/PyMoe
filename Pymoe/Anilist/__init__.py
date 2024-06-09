# __init__.py
from .search import *
from .get import *
from .ratelimiter import *

class Anilist:
    """
    Initialize a new instance to the Anilist API.
    This instance will handle read-only credentials.
    Pass in your client ID and client secret.
    In calls that require a user's auth token, you will need to provide it.

    :ivar dict settings: Various settings used across the module
    :ivar ASearch search: Handle search endpoints
    :ivar AGet get: Handle get endpoints
    """
    def __init__(self, cid=None, csecret=None, credentials=None):
        """
        :param str cid: Client ID
        :param str csecret: Client Secret
        :param str credentials: If provided, a JWT token for auth requests
        """
        self.settings = {
            'header': {
                'Content-Type': 'application/json',
                'User-Agent': 'Pymoe (github.com/ccubed/PyMoe)',
                'Accept': 'application/json'
            },
            'authurl': 'https://anilist.co/api',
            'apiurl': 'https://graphql.anilist.co',
            'cid': cid,
            'csecret': csecret,
            'token': credentials
        }
        self.search = ASearch(self.settings)
        self.get = AGet(self.settings)
