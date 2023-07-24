import unittest
from unittest.mock import patch, MagicMock
from psgrade.psgrade import main


class TestPsGrade(unittest.TestCase):

    # def setup
    @patch('psgrade.psgrade.Downloader')
    @patch('psgrade.psgrade.Controller')
    @patch('psgrade.psgrade.parse_args')
    def test_call_parse_args(
        self,
        mock_parse_args,
        mock_controller,
        mock_downloader
    ):
        mock_args = MagicMock()
        mock_parse_args.return_value = mock_args
        main()
        mock_parse_args.assert_called_once()

    @patch('psgrade.psgrade.Downloader')
    @patch('psgrade.psgrade.Controller')
    @patch('psgrade.psgrade.parse_args')
    def test_call_set_commandline_args(
        self,
        mock_parse_args,
        mock_controller,
        mock_downloader
    ):
        mock_args = MagicMock()
        mock_parse_args.return_value = mock_args
        main()
        mock_controller.return_value.set_commandline_args.assert_called_once_with(mock_args)

    @patch('psgrade.psgrade.Downloader')
    @patch('psgrade.psgrade.Controller')
    @patch('psgrade.psgrade.ResultsGenerator')
    @patch('psgrade.psgrade.parse_args')
    def test_call_results_generator_methods(
        self,
        mock_parse_args,
        mock_results_generator,
        mock_controller,
        mock_downloader
    ):
        mock_args = MagicMock()
        mock_parse_args.return_value = mock_args
        main()
        mock_results_generator.return_value.load_reformat_cs50_dicts.assert_called_once()
        mock_results_generator.return_value.get_student_results.assert_called_once()

    @patch('psgrade.psgrade.parse_args')
    @patch('psgrade.psgrade.Downloader')
    @patch('psgrade.psgrade.Plagiarism')
    @patch('psgrade.psgrade.ResultsGenerator')
    @patch('psgrade.psgrade.Controller')
    def test_plagiarism_check(
        self,
        mock_controller,
        mock_results_generator,
        mock_plagiarism,
        mock_downloader,
        mock_parse_args
    ):
        mock_args = MagicMock()
        mock_parse_args.return_value = mock_args
        mock_controller.return_value.plagiarism_check = True
        mock_controller.return_value.distribution_url = ['http://example.com']

        main()

        # Assert that the correct methods are called when plagiarism_check is True
        mock_downloader.return_value.submission_downloader.assert_called()
        mock_downloader.return_value.distro_downloader.assert_called()
        mock_plagiarism.return_value.run_plagiarism_check.assert_called()
        mock_results_generator.return_value.update_student_results_plagiarism.assert_called()

    @patch('psgrade.psgrade.parse_args')
    @patch('psgrade.psgrade.Downloader')
    @patch('psgrade.psgrade.Plagiarism')
    @patch('psgrade.psgrade.ResultsGenerator')
    @patch('psgrade.psgrade.Controller')
    def test_without_plagiarism_check(
        self,
        mock_controller,
        mock_results_generator,
        mock_plagiarism,
        mock_downloader,
        mock_parse_args
    ):
        mock_args = MagicMock()
        mock_parse_args.return_value = mock_args
        mock_controller.return_value.plagiarism_check = False

        main()

        # Assert that the correct method is called when plagiarism_check is False
        mock_results_generator.return_value.update_results_no_plagiarism.assert_called()

    @patch('psgrade.psgrade.Downloader')
    @patch('psgrade.psgrade.Controller')
    @patch('psgrade.psgrade.parse_args')
    def test_call_write_grade_table(
        self,
        mock_parse_args,
        mock_controller,
        mock_downloader
    ):
        mock_args = MagicMock()
        mock_parse_args.return_value = mock_args
        main()
        mock_controller.return_value.write_grade_table.assert_called_once()


if __name__ == '__main__':
    unittest.main()