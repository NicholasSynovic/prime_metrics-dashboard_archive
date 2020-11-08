import requests
from requests import Request, Response
import re


class GitHubConnector:
    def __init__(self, oauthToken: str = None) -> None:
        self.token = oauthToken

    def openConnection(self, url: str) -> Response:
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Metrics-Dashboard",
            "Authorization": "token {}".format(self.token),
        }

        return requests.get(url=url, headers=headers)

    def parseResponseHeaders(self, response: Response) -> dict:
        return {
            "Status-Code": response.status_code,
            "X-RateLimit-Limit": response.headers["X-RateLimit-Limit"],
            "X-RateLimit-Remaining": response.headers["X-RateLimit-Remaining"],
            "X-RateLimit-Reset": response.headers["X-RateLimit-Reset"],
            "Last-Page": re.findall("=(\d)>", response.headers["Link"])[-1],
        }

    def returnRateLimit(self) -> int:
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Metrics-Dashboard",
            "Authorization": "token {}".format(self.token),
        }

        data = requests.get(
            url="https://api.github.com/rate_limit", headers=headers
        ).json()

        return data["resources"]["core"]["remaining"]
