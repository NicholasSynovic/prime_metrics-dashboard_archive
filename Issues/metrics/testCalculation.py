import unittest
from IssuesCalculation import Calculations

class TestIssuesCalculation(unittest.TestCase):

    def setUp(self):
        self.testCalc = Calculations("alt-tab-macos.db")
        self.conn = self.testCalc.conn

    def test_total_issues(self):
        expected = 639 
        result = self.testCalc.get_total_issues(self.conn)
        self.assertTrue(expected == result)

if __name__ == '__main__':
    unittest.main()
        
