import json
import unittest
from json import load
from unittest.case import TestCase

from . import Commits


class TestCommits(unittest.TestCase):
    def __init__(self) -> None:
        with open("jsonResponses.json", "r") as file:
            self.commitsResponse = load(file)["commits"]
            file.close()

        self.commitsCollector = Commits()
