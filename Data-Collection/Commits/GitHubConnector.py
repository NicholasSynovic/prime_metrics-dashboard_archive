import requests
from requests import Request, Response


class GitHubConnector:
    def __init__(self, oauthToken: str = None) -> None:
        self.oauthToken = oauthToken

    def getConnection(self, url: str) -> Response:
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Metrics-Dashboard",
            "Authorization": "token {}".format(self.oauthToken),
        }

        return requests.get(url=url, headers=headers)

    def createJSON(self, response: Response) -> dict:
        return response.json()

    def parseResponseHeaders(self, response: Response) -> dict:
        return {
            "Status-Code": response.status_code,
            "X-RateLimit-Limit": response.headers["X-RateLimit-Limit"],
            "X-RateLimit-Remaining": response.headers["X-RateLimit-Remaining"],
            "X-RateLimit-Reset": response.headers["X-RateLimit-Reset"],
        }
