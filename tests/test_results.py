"""
Tests for the reslts.py module
"""
import os
from unittest import TestCase
from psgrade.results import ResultsGenerator


class TestResultGenerator(TestCase):
    """
    Test Case for Result Generator
    """

    def setUp(self) -> None:
        """
        You can define variables or constants for a test case here.
        Don't forget to assign them to 'self'
        :return: None
        """
        self.results_generator = ResultsGenerator()
        self.cs50_csv_lists = [
            os.path.dirname(__file__) + "/Resources/test1.csv",
            os.path.dirname(__file__) + "/Resources/test2.csv",
            os.path.dirname(__file__) + "/Resources/test3.csv",
        ]
        self.csv_columns = ['slug', 'github_id', 'github_username',
                            'name', 'github_url', 'timestamp', 'checks_passed',
                            'checks_run', 'style50_score', 'archive']
        self.results_dict_after_plagiarism = \
            {'user1':
                 {'tasks': 2,
                  'fau-is/introcs/task1':
                      'https://introcs.is.rw.fau.de/landing_page/',
                  'tasknames':
                      ['task1', 'task2'],
                  'fau-is/introcs/task2':
                      'https://introcs.is.rw.fau.de/landing_page/'},
             'user2': {'tasks': 1,
                       'fau-is/introcs/task1': 'https://introcs.is.rw.fau.de/landing_page/',
                       'tasknames': ['task1'],
                       'IsPlag': True}}

    def test_constructor(self):
        """
        Tests the constructor
        :return:
        """
        self.assertEqual(self.results_generator.plagiarising_students, [])
        self.assertEqual(self.results_generator.passing_students, [])
        self.assertEqual(self.results_generator.cs50_files_as_dict, [])
        self.assertEqual(self.results_generator.student_results_preliminary, {})
        self.assertEqual(self.results_generator.student_results_final, {})

    def test_load_reformat_cs50_dicts(self):
        """
        Tests loading and reformating submit50 dicts
        :return: None
        """
        self.results_generator.load_reformat_cs50_dicts(self.cs50_csv_lists)

        # check number of loaded csv files
        self.assertEqual(len(self.results_generator.cs50_files_as_dict), 3)

        # check entries in each loaded csv
        self.assertEqual(list(self.results_generator.cs50_files_as_dict[0].keys()),
                         ['user1', 'user2', 'user3', 'user4'])
        self.assertEqual(list(self.results_generator.cs50_files_as_dict[1].keys()),
                         ['user1'],)
        self.assertEqual(list(self.results_generator.cs50_files_as_dict[2].keys()),
                         ['user3'], )

        # check column names and values that are always the same
        for csv_dict in self.results_generator.cs50_files_as_dict:
            for user in list(csv_dict.keys()):
                self.assertEqual(list(csv_dict[user].keys()), self.csv_columns)
                self.assertEqual(csv_dict[user]['github_url'],
                                 'https://introcs.is.rw.fau.de/landing_page/')
                self.assertEqual(csv_dict[user]['timestamp'],
                                 'Wed, 15 Feb 2023 12:00:00AM CET')
                self.assertEqual(csv_dict[user]['archive'],
                                 'https://introcs.is.rw.fau.de/landing_page/')

        # check first csv
        for user in self.results_generator.cs50_files_as_dict[0]:
            self.assertEqual(
                self.results_generator.cs50_files_as_dict[0][user]['slug'],
                'fau-is/introcs/task1'
            )
            self.assertEqual(self.results_generator.cs50_files_as_dict[0][user]['checks_run'], '4')

        self.assertEqual(
            self.results_generator.cs50_files_as_dict[0]['user1']['github_id'],
            '1'
        )
        self.assertEqual(
            self.results_generator.cs50_files_as_dict[0]['user1']['github_username'],
            'user1'
        )
        self.assertEqual(
            self.results_generator.cs50_files_as_dict[0]['user1']['name'],
            'user1'
        )
        self.assertEqual(
            self.results_generator.cs50_files_as_dict[0]['user1']['checks_passed'],
            '4'
        )
        self.assertEqual(
            self.results_generator.cs50_files_as_dict[0]['user1']['style50_score'],
            '1'
        )

        self.assertEqual(
            self.results_generator.cs50_files_as_dict[0]['user2']['github_id'],
            '2'
        )
        self.assertEqual(
            self.results_generator.cs50_files_as_dict[0]['user2']['github_username'],
            'user2'
        )
        self.assertEqual(
            self.results_generator.cs50_files_as_dict[0]['user2']['name'],
            'user2'
        )
        self.assertEqual(
            self.results_generator.cs50_files_as_dict[0]['user2']['checks_passed'],
            '4'
        )
        self.assertEqual(
            self.results_generator.cs50_files_as_dict[0]['user2']['style50_score'],
            'ERROR'
        )

        self.assertEqual(
            self.results_generator.cs50_files_as_dict[0]['user3']['github_id'],
            '3'
        )
        self.assertEqual(
            self.results_generator.cs50_files_as_dict[0]['user3']['github_username'],
            'user3')
        self.assertEqual(
            self.results_generator.cs50_files_as_dict[0]['user3']['name'],
            'user3')
        self.assertEqual(
            self.results_generator.cs50_files_as_dict[0]['user3']['checks_passed'],
            '0')
        self.assertEqual(
            self.results_generator.cs50_files_as_dict[0]['user3']['style50_score'],
            '1'
        )

        self.assertEqual(
            self.results_generator.cs50_files_as_dict[0]['user4']['github_id'],
            '4'
        )
        self.assertEqual(
            self.results_generator.cs50_files_as_dict[0]['user4']['github_username'],
            'user4'
        )
        self.assertEqual(
            self.results_generator.cs50_files_as_dict[0]['user4']['name'],
            'user4'
        )
        self.assertEqual(
            self.results_generator.cs50_files_as_dict[0]['user4']['checks_passed'],
            '4'
        )
        self.assertEqual(
            self.results_generator.cs50_files_as_dict[0]['user4']['style50_score'],
            '0'
        )

        # check second csv
        self.assertEqual(
            self.results_generator.cs50_files_as_dict[1]['user1']['slug'],
            'fau-is/introcs/task2'
        )
        self.assertEqual(
            self.results_generator.cs50_files_as_dict[1]['user1']['github_id'],
            '1'
        )
        self.assertEqual(
            self.results_generator.cs50_files_as_dict[1]['user1']['github_username'],
            'user1'
        )
        self.assertEqual(
            self.results_generator.cs50_files_as_dict[1]['user1']['name'],
            'user1'
        )
        self.assertEqual(
            self.results_generator.cs50_files_as_dict[1]['user1']['checks_passed'],
            '3'
        )
        self.assertEqual(
            self.results_generator.cs50_files_as_dict[1]['user1']['checks_run'],
            '3'
        )
        self.assertEqual(
            self.results_generator.cs50_files_as_dict[1]['user1']['style50_score'],
            '1'
        )

        # check third csv
        self.assertEqual(
            self.results_generator.cs50_files_as_dict[2]['user3']['slug'],
            'fau-is/introcs/task3'
        )
        self.assertEqual(
            self.results_generator.cs50_files_as_dict[2]['user3']['github_id'],
            '3'
        )
        self.assertEqual(
            self.results_generator.cs50_files_as_dict[2]['user3']['github_username'],
            'user3'
        )
        self.assertEqual(
            self.results_generator.cs50_files_as_dict[2]['user3']['name'],
            'user3'
        )
        self.assertEqual(
            self.results_generator.cs50_files_as_dict[2]['user3']['checks_passed'],
            '3'
        )
        self.assertEqual(
            self.results_generator.cs50_files_as_dict[2]['user3']['checks_run'],
            '3'
        )
        self.assertEqual(
            self.results_generator.cs50_files_as_dict[2]['user3']['style50_score'],
            '1'
        )

    def make_asserts_for_results(self, results) -> None:
        """
        Method to unify the assertions for update, and import,
        if no plagiarism check was performed
        :param results: dictionary
        :return: None
        """
        self.assertEqual(list(results.keys()),['user1', 'user2', 'user3'])
        self.assertEqual(list(results['user1'].keys()),
                         ['tasks', 'fau-is/introcs/task1',
                          'tasknames', 'fau-is/introcs/task2'])
        self.assertEqual(list(results['user2'].keys()),
                         ['tasks', 'fau-is/introcs/task1', 'tasknames'])
        # check preliminary results dict values
        self.assertEqual(results['user1']['tasks'], 2)
        self.assertEqual(results['user1']['fau-is/introcs/task1'],
            'https://introcs.is.rw.fau.de/landing_page/')
        self.assertEqual(results['user1']['tasknames'],['task1', 'task2'])
        self.assertEqual(results['user1']['fau-is/introcs/task2'],
                         'https://introcs.is.rw.fau.de/landing_page/')
        self.assertEqual(results['user2']['tasks'], 1)
        self.assertEqual(results['user2']['fau-is/introcs/task1'],
            'https://introcs.is.rw.fau.de/landing_page/')
        self.assertEqual(
            results['user2']['tasknames'], ['task1'])
        self.assertEqual(results['user3']['tasks'], 1)
        self.assertEqual(results['user3']['fau-is/introcs/task3'],
                         'https://introcs.is.rw.fau.de/landing_page/')
        self.assertEqual(
            results['user3']['tasknames'], ['task3'])

        self.assertEqual(self.results_generator.passing_students, ['user1', 'user2'])

    def test_get_student_results(self):
        """
        Student result calculation test
        :return:
        """
        slugs = []
        tasks = ['task2']
        choices = [['task1']]
        self.results_generator.load_reformat_cs50_dicts(self.cs50_csv_lists)
        self.results_generator.get_student_results(slugs, tasks, choices)

        # check preliminary results dict keys
        self.make_asserts_for_results(self.results_generator.student_results_preliminary)



    def test_update_results_no_plagiarism(self):
        """
        Final result after updating the list
        :return:
        """
        slugs = []
        tasks = ['task2']
        choices = [['task1']]
        self.results_generator.load_reformat_cs50_dicts(self.cs50_csv_lists)
        self.results_generator.get_student_results(slugs, tasks, choices)
        self.results_generator.update_results_no_plagiarism()
        self.make_asserts_for_results(self.results_generator.student_results_final)


    def test_update_student_results_plagiarism(self):
        """

        :return:
        """
        slugs = []
        tasks = ['task2']
        choices = [['task1']]
        self.results_generator.load_reformat_cs50_dicts(self.cs50_csv_lists)
        self.results_generator.get_student_results(slugs, tasks, choices)
        self.results_generator.update_student_results_plagiarism(self.results_dict_after_plagiarism)
        results = self.results_generator.student_results_final

        # check final results dict keys
        self.assertEqual(len(list(results.keys())), 2)
        self.assertEqual(list(results.keys()), ['user1', 'user2'])
        self.assertEqual(list(results['user1'].keys()),
                         ['tasks', 'fau-is/introcs/task1',
                          'tasknames', 'fau-is/introcs/task2'])
        self.assertEqual(list(results['user2'].keys()),
                         ['tasks', 'fau-is/introcs/task1',
                          'tasknames', 'IsPlag'])

        # check final results dict values
        self.assertEqual(results['user1']['tasks'], 2)
        self.assertEqual(results['user1']['fau-is/introcs/task1'],
                         'https://introcs.is.rw.fau.de/landing_page/')
        self.assertEqual(results['user1']['tasknames'],
                         ['task1', 'task2'])
        self.assertEqual(results['user1']['fau-is/introcs/task2'],
                         'https://introcs.is.rw.fau.de/landing_page/')

        self.assertEqual(results['user2']['tasks'], 1)
        self.assertEqual(results['user2']['fau-is/introcs/task1'],
                         'https://introcs.is.rw.fau.de/landing_page/')
        self.assertEqual(results['user2']['tasknames'], ['task1'])
        self.assertEqual(results['user2']['IsPlag'], True)

        # check passing and plagiarising students
        self.assertEqual(self.results_generator.passing_students, ['user1'])
        self.assertEqual(self.results_generator.plagiarising_students, ['user2'])
