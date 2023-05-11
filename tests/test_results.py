from unittest import TestCase
from unittest.mock import MagicMock
from psgrade.results import ResultsGenerator


class TestResultGenerator(TestCase):

    def setUp(self) -> None:
        """
        You can define variables or constants for a test case here.
        Don't forget to assign them to 'self'
        :return: None
        """
        self.rg = ResultsGenerator()
        self.CS50_csv_lists = ["Resources/test1.csv", "Resources/test2.csv"]
    def test_constructor(self):

        self.assertIsInstance(self.rg.CS50FilesAsDict, list)
        self.assertEqual(self.rg.CS50FilesAsDict, [])
        self.assertTrue(self.rg.CS50FilesAsDict == [])

    def test_load_reformat_CS50_dicts(self):
        self.rg.load_reformat_CS50_dicts(self.CS50_csv_lists)


