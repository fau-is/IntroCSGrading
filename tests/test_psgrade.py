import unittest
from unittest.mock import patch
from psgrade.psgrade import main


class TestPsGrade(unittest.TestCase):
    # use the @patch decorator from the unittest.mock module to replace external functions
    @patch('psgrade.parse_args')
    @patch('psgrade.Controller')
    @patch('psgrade.results.ResultsGenerator')

    def test_main(self, mock_results_generator, mock_controller, mock_parse_args):
        args = 'test_args'
        slugs = 'test_slugs'
        tasks = 'test_tasks'
        choices = 'test_choices'
        input_cs50_csv = 'test_csv'
        sentimental = True
        archive = True

        mock_parse_args.return_value = args
        mock_controller_instance = mock_controller.return_value
        mock_results_generator_instance = mock_results_generator.return_value

        main()

        mock_parse_args.assert_called_once()
        mock_controller.assert_called_once()
        mock_controller_instance.set_commandline_args.assert_called_once_with(args)
        mock_results_generator.assert_called_once()
        mock_results_generator_instance.load_reformat_cs50_dicts.assert_called_once_with(input_cs50_csv)
        mock_results_generator_instance.get_student_results.assert_called_once_with(slugs, tasks, choices)

        mock_results_generator_instance.update_student_results_plagiarism.assert_not_called()
        mock_results_generator_instance.update_results_no_plagiarism.assert_called_once()
        mock_controller_instance.write_grade_table.assert_called_once_with(
            mock_results_generator_instance.student_results_final,
            mock_results_generator_instance.passing_students,
            mock_results_generator_instance.plagiarising_students
        )

        # Additional checks if plagiarism check is enabled



if __name__ == '__main__':
    unittest.main()
