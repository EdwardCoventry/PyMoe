# get.py
import json
import requests
from .ratelimiter import rate_limited


class AGet:
    def __init__(self, settings):
        self.settings = settings

    @rate_limited
    def anime(self, query, anime_id):
        """
        The function to retrieve an anime's details.

        :param int anime_id: the anime's ID
        :return: dict or None
        :rtype: dict or NoneType
        """

        vars = {"id": anime_id}
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
    def character(self, query, character_id):
        """
        The function to retrieve a character's details.

        :param int character_id: the character's ID
        :return: dict or None
        :rtype: dict or NoneType
        """
        vars = {"id": character_id}
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
