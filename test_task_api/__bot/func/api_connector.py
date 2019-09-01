import requests
from rest_framework.utils import json


class APIClient:
    def __init__(self, url, port):
        self.url = url
        self.port = port
        self.request = requests
        self.connection_url = "http://%s:%s" % (self.url, self.port)

    def postrequest_json(self, url, params, headers=None):
        """
        Initiate POST request with JSON raw body

        :param url: Short url to api point starting from user/ or post/ ...
        :param params: { JSON }
        :param headers: { It can be absent in queries without AUTH }
        :return:
        """
        if headers is None:
            headers = {}
        response = self.request.post("%s/%s" % (self.connection_url, url), headers=headers, json=params)
        return response

    def getrequest_json(self, url, params, headers=None):
        """
        Initiate GET request with JSON raw body

        :param url: Short url to api point starting from user/ or post/ ...
        :param params: { JSON }
        :param headers: { It can be absent in queries without AUTH }
        :return:
        """
        if headers is None:
            headers = {}
        full_url = "%s/%s" % (self.connection_url, url)
        response = self.request.get(full_url, headers=headers, json=params)
        return response

    def auth_postrequest_json(self, url, token, params):
        """
        Initiate JWT AUTHENTICATED POST request with JSON raw body

        :param url: Short url to api point starting from user/ or post/ ...
        :param token: JWT_TOKEN include Bearer ....
        :param params: { JSON }
        :return:
        """
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }

        response = self.postrequest_json(url, params, headers)
        return response

    def auth_getrequest_json(self, url, token, params):
        """
        Initiate JWT AUTHENTICATED GET request with JSON raw body

        :param url: Short url to api point starting from user/ or post/ ...
        :param token: JWT_TOKEN include Bearer ....
        :param params: { JSON }
        :return:
        """
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }

        response = self.getrequest_json(url, params, headers)
        return response

    def login(self, email, password):
        url = "user/login/"
        response = self.postrequest_json("%s" % url, params={"email": email, "password": password})
        return json.loads(response.text)['token']

    def creating_post(self, token, title, text):
        url = "post/creation/"
        params = {
            "title": title,
            "text": text
        }

        response = self.auth_postrequest_json(url, token, params)
        return json.loads(response.text)

    def like_or_unlike(self, token, post_id, like=True):
        url_like = "post/like/"
        url_unlike = "post/unlike/"

        if like:
            url = url_like
        else:
            url = url_unlike

        params = {
            "post": post_id
        }
        response = self.auth_postrequest_json(url, token, params)
        return json.loads(response.text)
