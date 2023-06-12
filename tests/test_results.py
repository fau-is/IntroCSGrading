from unittest import TestCase
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
        self.csv_columns = ['slug', 'github_id', 'github_username', 'name', 'github_url', 'timestamp', 'checks_passed',
                            'checks_run', 'style50_score', 'archive']
        self.results_dict_after_plagiarism = {'user1': {'tasks': 2,
                                         'fau-is/introcs/CBubbleSort': 'https://introcs.is.rw.fau.de/landing_page/',
                                         'tasknames': ['cbubblesort', 'copycat'],
                                         'fau-is/introcs/Pset3/Copycat': 'https://introcs.is.rw.fau.de/landing_page/'},
                          'user2': {'tasks': 1,
                                       'fau-is/introcs/CBubbleSort': 'https://introcs.is.rw.fau.de/landing_page/',
                                       'tasknames': ['cbubblesort'],
                                       'IsPlag': True}}

    def test_constructor(self):
        self.assertEqual(self.rg.PlagiarisingStudents, [])
        self.assertEqual(self.rg.PassingStudents, [])
        self.assertEqual(self.rg.CS50FilesAsDict, [])
        self.assertEqual(self.rg.StudentResultsPreliminary, {})
        self.assertEqual(self.rg.StudentResultsFinal, {})

    def test_load_reformat_CS50_dicts(self):
        self.rg.load_reformat_CS50_dicts(self.CS50_csv_lists)

        # check number of loaded csv files
        self.assertEqual(len(self.rg.CS50FilesAsDict), 2)

        # check entries in each loaded csv
        self.assertEqual(list(self.rg.CS50FilesAsDict[0].keys()), ['user1', 'user2', 'user3', 'user4'])
        self.assertEqual(list(self.rg.CS50FilesAsDict[1].keys()), ['user1'])

        # check column names and values that are always the same
        for csv_dict in self.rg.CS50FilesAsDict:
            for user in list(csv_dict.keys()):
                self.assertEqual(list(csv_dict[user].keys()), self.csv_columns)
                self.assertEqual(csv_dict[user]['github_url'], 'https://introcs.is.rw.fau.de/landing_page/')
                self.assertEqual(csv_dict[user]['timestamp'], 'Wed, 15 Feb 2023 12:00:00AM CET')
                self.assertEqual(csv_dict[user]['archive'], 'https://introcs.is.rw.fau.de/landing_page/')

        # check first csv
        for user in self.rg.CS50FilesAsDict[0]:
            self.assertEqual(self.rg.CS50FilesAsDict[0][user]['slug'], 'fau-is/introcs/CBubbleSort')
            self.assertEqual(self.rg.CS50FilesAsDict[0][user]['checks_run'], '4')

        self.assertEqual(self.rg.CS50FilesAsDict[0]['user1']['github_id'], '1')
        self.assertEqual(self.rg.CS50FilesAsDict[0]['user1']['github_username'], 'user1')
        self.assertEqual(self.rg.CS50FilesAsDict[0]['user1']['name'], 'user1')
        self.assertEqual(self.rg.CS50FilesAsDict[0]['user1']['checks_passed'], '4')
        self.assertEqual(self.rg.CS50FilesAsDict[0]['user1']['style50_score'], '1')

        self.assertEqual(self.rg.CS50FilesAsDict[0]['user2']['github_id'], '2')
        self.assertEqual(self.rg.CS50FilesAsDict[0]['user2']['github_username'], 'user2')
        self.assertEqual(self.rg.CS50FilesAsDict[0]['user2']['name'], 'user2')
        self.assertEqual(self.rg.CS50FilesAsDict[0]['user2']['checks_passed'], '4')
        self.assertEqual(self.rg.CS50FilesAsDict[0]['user2']['style50_score'], 'ERROR')

        self.assertEqual(self.rg.CS50FilesAsDict[0]['user3']['github_id'], '3')
        self.assertEqual(self.rg.CS50FilesAsDict[0]['user3']['github_username'], 'user3')
        self.assertEqual(self.rg.CS50FilesAsDict[0]['user3']['name'], 'user3')
        self.assertEqual(self.rg.CS50FilesAsDict[0]['user3']['checks_passed'], '0')
        self.assertEqual(self.rg.CS50FilesAsDict[0]['user3']['style50_score'], '1')

        self.assertEqual(self.rg.CS50FilesAsDict[0]['user4']['github_id'], '4')
        self.assertEqual(self.rg.CS50FilesAsDict[0]['user4']['github_username'], 'user4')
        self.assertEqual(self.rg.CS50FilesAsDict[0]['user4']['name'], 'user4')
        self.assertEqual(self.rg.CS50FilesAsDict[0]['user4']['checks_passed'], '4')
        self.assertEqual(self.rg.CS50FilesAsDict[0]['user4']['style50_score'], '0')

        # check second csv
        self.assertEqual(self.rg.CS50FilesAsDict[1]['user1']['slug'], 'fau-is/introcs/Pset3/Copycat')
        self.assertEqual(self.rg.CS50FilesAsDict[1]['user1']['github_id'], '1')
        self.assertEqual(self.rg.CS50FilesAsDict[1]['user1']['github_username'], 'user1')
        self.assertEqual(self.rg.CS50FilesAsDict[1]['user1']['name'], 'user1')
        self.assertEqual(self.rg.CS50FilesAsDict[1]['user1']['checks_passed'], '3')
        self.assertEqual(self.rg.CS50FilesAsDict[1]['user1']['checks_run'], '3')
        self.assertEqual(self.rg.CS50FilesAsDict[1]['user1']['style50_score'], '1')

    def test_get_student_results(self):
        slugs = []
        tasks = []
        choices = []
        self.rg.load_reformat_CS50_dicts(self.CS50_csv_lists)
        self.rg.get_student_results(slugs, tasks, choices)

        # check preliminary results dict keys
        self.assertEqual(list(self.rg.StudentResultsPreliminary.keys()), ['user1', 'user2'])
        self.assertEqual(list(self.rg.StudentResultsPreliminary['user1'].keys()),
                         ['tasks', 'fau-is/introcs/CBubbleSort', 'tasknames', 'fau-is/introcs/Pset3/Copycat'])
        self.assertEqual(list(self.rg.StudentResultsPreliminary['user2'].keys()),
                         ['tasks', 'fau-is/introcs/CBubbleSort', 'tasknames'])

        # check preliminary results dict values
        self.assertEqual(self.rg.StudentResultsPreliminary['user1']['tasks'], 2)
        self.assertEqual(self.rg.StudentResultsPreliminary['user1']['fau-is/introcs/CBubbleSort'],
                         'https://introcs.is.rw.fau.de/landing_page/')
        self.assertEqual(self.rg.StudentResultsPreliminary['user1']['tasknames'], ['cbubblesort', 'copycat'])
        self.assertEqual(self.rg.StudentResultsPreliminary['user1']['fau-is/introcs/Pset3/Copycat'],
                         'https://introcs.is.rw.fau.de/landing_page/')

        self.assertEqual(self.rg.StudentResultsPreliminary['user2']['tasks'], 1)
        self.assertEqual(self.rg.StudentResultsPreliminary['user2']['fau-is/introcs/CBubbleSort'],
                         'https://introcs.is.rw.fau.de/landing_page/')
        self.assertEqual(self.rg.StudentResultsPreliminary['user2']['tasknames'], ['cbubblesort'])

        # check passing students
        self.assertEqual(self.rg.PassingStudents, ['user1', 'user2'])

    def test_update_results_no_plagiarism(self):
        slugs = []
        tasks = []
        choices = []
        self.rg.load_reformat_CS50_dicts(self.CS50_csv_lists)
        self.rg.get_student_results(slugs, tasks, choices)
        self.rg.update_results_no_plagiarism()

        # check final results dict keys
        self.assertEqual(len(list(self.rg.StudentResultsFinal.keys())), 2)
        self.assertEqual(list(self.rg.StudentResultsFinal.keys()), ['user1', 'user2'])
        self.assertEqual(list(self.rg.StudentResultsFinal['user1'].keys()),
                         ['tasks', 'fau-is/introcs/CBubbleSort', 'tasknames', 'fau-is/introcs/Pset3/Copycat'])
        self.assertEqual(list(self.rg.StudentResultsFinal['user2'].keys()),
                         ['tasks', 'fau-is/introcs/CBubbleSort', 'tasknames'])

        # check final results dict values
        self.assertEqual(self.rg.StudentResultsFinal['user1']['tasks'], 2)
        self.assertEqual(self.rg.StudentResultsFinal['user1']['fau-is/introcs/CBubbleSort'],
                         'https://introcs.is.rw.fau.de/landing_page/')
        self.assertEqual(self.rg.StudentResultsFinal['user1']['tasknames'], ['cbubblesort', 'copycat'])
        self.assertEqual(self.rg.StudentResultsFinal['user1']['fau-is/introcs/Pset3/Copycat'],
                         'https://introcs.is.rw.fau.de/landing_page/')

        self.assertEqual(self.rg.StudentResultsFinal['user2']['tasks'], 1)
        self.assertEqual(self.rg.StudentResultsFinal['user2']['fau-is/introcs/CBubbleSort'],
                         'https://introcs.is.rw.fau.de/landing_page/')
        self.assertEqual(self.rg.StudentResultsFinal['user2']['tasknames'], ['cbubblesort'])

        # check passing students
        self.assertEqual(self.rg.PassingStudents, ['user1', 'user2'])

    def test_update_student_results_plagiarism(self):
        slugs = []
        tasks = []
        choices = []
        self.rg.load_reformat_CS50_dicts(self.CS50_csv_lists)
        self.rg.get_student_results(slugs, tasks, choices)
        self.rg.update_student_results_plagiarism(self.results_dict_after_plagiarism)

        # check final results dict keys
        self.assertEqual(len(list(self.rg.StudentResultsFinal.keys())), 2)
        self.assertEqual(list(self.rg.StudentResultsFinal.keys()), ['user1', 'user2'])
        self.assertEqual(list(self.rg.StudentResultsFinal['user1'].keys()),
                         ['tasks', 'fau-is/introcs/CBubbleSort', 'tasknames', 'fau-is/introcs/Pset3/Copycat'])
        self.assertEqual(list(self.rg.StudentResultsFinal['user2'].keys()),
                         ['tasks', 'fau-is/introcs/CBubbleSort', 'tasknames', 'IsPlag'])

        # check final results dict values
        self.assertEqual(self.rg.StudentResultsFinal['user1']['tasks'], 2)
        self.assertEqual(self.rg.StudentResultsFinal['user1']['fau-is/introcs/CBubbleSort'],
                         'https://introcs.is.rw.fau.de/landing_page/')
        self.assertEqual(self.rg.StudentResultsFinal['user1']['tasknames'], ['cbubblesort', 'copycat'])
        self.assertEqual(self.rg.StudentResultsFinal['user1']['fau-is/introcs/Pset3/Copycat'],
                         'https://introcs.is.rw.fau.de/landing_page/')

        self.assertEqual(self.rg.StudentResultsFinal['user2']['tasks'], 1)
        self.assertEqual(self.rg.StudentResultsFinal['user2']['fau-is/introcs/CBubbleSort'],
                         'https://introcs.is.rw.fau.de/landing_page/')
        self.assertEqual(self.rg.StudentResultsFinal['user2']['tasknames'], ['cbubblesort'])
        self.assertEqual(self.rg.StudentResultsFinal['user2']['IsPlag'], True)

        # check passing and plagiarising students
        self.assertEqual(self.rg.PassingStudents, ['user1'])
        self.assertEqual(self.rg.PlagiarisingStudents, ['user2'])