import unittest
from unittest.mock import patch, MagicMock
from psgrade.psgrade import main


class TestPsGrade(unittest.TestCase):
    """
    Unit tests for the psgrade module.
    The tests check, that all functions which are called in psgarde, are called once
    and with the correct arguments.
    """

    def setUp(self):
        """
        Set up mock objects for testing
        """
        self.mock_parse_args = patch('psgrade.psgrade.parse_args').start()
        self.mock_controller = patch('psgrade.psgrade.Controller').start()
        self.mock_downloader = patch('psgrade.psgrade.Downloader').start()
        self.mock_results_generator = patch('psgrade.psgrade.ResultsGenerator').start()
        self.mock_plagiarism = patch('psgrade.psgrade.Plagiarism').start()

        self.mock_args = MagicMock()
        self.mock_parse_args.return_value = self.mock_args

    def tearDown(self):
        """
        Clean up resources after each test. This method is called after each test method,
        so that the mocks do not interfere with other tests.
        """
        patch.stopall()

    def test_call_parse_args(self):
        """
        Test that the parse_args function is called once.
        """
        main()
        self.mock_parse_args.assert_called_once()

    def test_call_set_commandline_args(self):
        """
        Test that set_commandline_args method is called with the correct arguments.
        """
        main()
        self.mock_controller.return_value.set_commandline_args.assert_called_once_with(self.mock_args)

    def test_call_results_generator_methods(self):
        """
        Test that the methods of the ResultsGenerator class are called.
        """
        main()
        self.mock_results_generator.return_value.load_reformat_cs50_dicts.assert_called_once()
        self.mock_results_generator.return_value.get_student_results.assert_called_once()

    def test_plagiarism_check(self):
        """
        Test the behavior when plagiarism_check is set to True.
        """
        self.mock_controller.return_value.plagiarism_check = True
        self.mock_controller.return_value.distribution_url = ['http://example.com']

        main()

        self.mock_downloader.return_value.submission_downloader.assert_called()
        self.mock_downloader.return_value.distro_downloader.assert_called()
        self.mock_plagiarism.return_value.run_plagiarism_check.assert_called()
        self.mock_results_generator.return_value.update_student_results_plagiarism.assert_called()

    def test_without_plagiarism_check(self):
        """
        Test the behavior when plagiarism_check is set to False.
        """
        self.mock_controller.return_value.plagiarism_check = False

        main()

        self.mock_results_generator.return_value.update_results_no_plagiarism.assert_called()

    def test_call_write_grade_table(self):
        """
        Test that the write_grade_table method is called once.
        """
        main()
        self.mock_controller.return_value.write_grade_table.assert_called_once()

if __name__ == '__main__':
    unittest.main()