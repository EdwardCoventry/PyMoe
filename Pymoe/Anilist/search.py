# search.py
import json
import requests
from .ratelimiter import rate_limited

class ASearch:
    def __init__(self, settings):
        self.settings = settings

    @rate_limited
    def series_id_character_names(self, query, anime_id, page=1, perpage=25):
        """
        Search for a character by term.
        Results are paginated by default. Page specifies which page we're on.
        Perpage specifies how many per page to request. 3 is just the example from the API docs.

        :param str query: GraphQL query string
        :param int anime_id: Anime ID to search characters for
        :param int page: Which page are we requesting? Starts at 1.
        :param int perpage: How many results per page are we requesting?
        :return: Json object with returned results.
        :rtype: dict or NoneType
        """
        vars = {"id": anime_id, "page": page, "perpage": perpage}
        r = requests.post(self.settings['apiurl'],
                          headers=self.settings['header'],
                          json={'query': query, 'variables': vars})
        jsd = r.text

        try:
            jsd = json.loads(jsd)
        except ValueError:
            return None, r.headers
        else:
            return jsd, r.headers

    @rate_limited
    def anime(self, term, page=1, perpage=100, query=None):
        """
        Search for an anime by term.
        Results are paginated by default. Page specifies which page we're on.
        Perpage specifies how many per page to request. 3 is just the example from the API docs.

        :param str term: Name to search by
        :param int page: Which page are we requesting? starts at 1.
        :param int perpage: How many results per page? defaults to 3.
        :param str query: GraphQL query string
        :return: Json object with returned results.
        :rtype: dict or NoneType
        """
        assert query

        vars = {"query": term, "page": page, "perpage": perpage}
        r = requests.post(self.settings['apiurl'],
                          headers=self.settings['header'],
                          json={'query': query, 'variables': vars})
        jsd = r.text

        try:
            jsd = json.loads(jsd)
        except ValueError:
            return None, r.headers
        else:
            return jsd, r.headers

    @rate_limited
    def anime_listings(self, sort_by, query, page=1, perpage=100):
        """
        Search for anime listings sorted by the specified criteria.

        :param str sort_by: The criteria to sort by
        :param str query: GraphQL query string
        :param int page: Which page are we requesting? starts at 1.
        :param int perpage: How many results per page? defaults to 3.
        :return: Json object with returned results.
        :rtype: dict or NoneType
        """
        vars = {"page": page, "perpage": perpage}
        r = requests.post(self.settings['apiurl'],
                          headers=self.settings['header'],
                          json={'query': query, 'variables': vars})
        jsd = r.text

        try:
            jsd = json.loads(jsd)
        except ValueError:
            return None, r.headers
        else:
            return jsd, r.headers
