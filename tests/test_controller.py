import unittest
from unittest.mock import MagicMock
from psgrade.controller import Controller
import os
import csv
import shutil

class TestController(unittest.TestCase):
    def setUp_Grade_Table(self):
        self.controller = Controller()
        args = MagicMock()
        args.inputcsv = ["cs50_problems_2022_x_mario_less.csv", "cs50_problems_2022_x_mario_more.csv",
                         "cs50_problems_2022_x_cash.csv", "cs50_problems_2022_x_credit.csv"]
        args.gradetable = "grade_table.csv"
        args.distribution_code = None
        args.psetId = '1'
        args.tasks = ["less", "more", "cash", "credit"]
        args.choices = ["less-more", "cash-credit"]
        args.archive = False
        args.sentimental = False
        args.plag = True
        self.controller.set_commandline_args(args)
        shutil.copyfile(f'../{self.controller.GradeTable}', f'./{self.controller.GradeTable}')
        self.student_results_final = {
            'Gituser1': {
                'tasks': 2,
                'cs50/problems/2022/x/mario/less': 'url1',
                'tasknames': ['less', 'cash'],
                'cs50/problems/2022/x/cash': 'url2'
            },
            'Gituser2': {
                'tasks': 2,
                'cs50/problems/2022/x/mario/less': 'url1',
                'tasknames': ['less', 'cash'],
                'cs50/problems/2022/x/cash': 'url2'
            },
            'Gituser3': {
                'tasks': 2,
                'cs50/problems/2022/x/mario/less': 'url1',
                'tasknames': ['less', 'cash'],
                'cs50/problems/2022/x/cash': 'url2',
                'PlagConfidence': 93
            },
            'Gituser4': {
                'tasks': 3,
                'cs50/problems/2022/x/mario/less': 'url1',
                'tasknames': ['less', 'more', 'cash'],
                'cs50/problems/2022/x/mario/more': 'url2',
                'cs50/problems/2022/x/cash': 'url3'
            },
            'Gituser5': {
                'tasks': 2,
                'cs50/problems/2022/x/mario/less': 'url1',
                'tasknames': ['less', 'cash'],
                'cs50/problems/2022/x/cash': 'url2'
            },
            'Gituser6': {
                'tasks': 2,
                'cs50/problems/2022/x/mario/less': 'url1',
                'tasknames': ['less', 'cash'],
                'cs50/problems/2022/x/cash': 'url2'
            },
            'Gituser7': {
                'tasks': 2,
                'cs50/problems/2022/x/mario/less': 'url1',
                'tasknames': ['less', 'cash'],
                'cs50/problems/2022/x/cash': 'url2'
            },
            'Gituser8': {
                'tasks': 2,
                'cs50/problems/2022/x/mario/less': 'url1',
                'tasknames': ['less', 'cash'],
                'cs50/problems/2022/x/cash': 'url2'
            },
            'Gituser9': {
                'tasks': 2,
                'cs50/problems/2022/x/mario/less': 'url1',
                'tasknames': ['less', 'cash'],
                'cs50/problems/2022/x/cash': 'url2'
            },
            'Gituser10': {
                'tasks': 2,
                'cs50/problems/2022/x/mario/less': 'url1',
                'tasknames': ['less', 'cash'],
                'cs50/problems/2022/x/cash': 'url2'
            }

        }
        plagiarising_students = ['Gituser3']
        self.passing_students = [
            'Gituser1', 'Gituser2', 'Gituser4', 'Gituser5',
            'Gituser6', 'Gituser7', 'Gituser8', 'Gituser9', 'Gituser10'
        ]
        self.plagiarising_students = ['Gituser3']
        self.controller.write_grade_table(self.student_results_final, self.passing_students, self.plagiarising_students)

    def test_initial_values(self):
        self.assertFalse(self.controller.PlagiarismCheck)
        self.assertFalse(self.controller.Sentimental)
        self.assertFalse(self.controller.Archive)
        self.assertEqual(self.controller.Choices, [])
        self.assertEqual(self.controller.Tasks, [])
        self.assertEqual(self.controller.ProblemSetName, "")
        self.assertEqual(self.controller.DistributionURL, [])
        self.assertEqual(self.controller.GradeTable, "")
        self.assertEqual(self.controller.InputCS50Csv, [])
        self.assertEqual(self.controller.Slugs, [])
        self.assertEqual(self.controller.ResultsPaths, [])

    def test_set_commandline_args(self):
        args = MagicMock()
        args.inputcsv = ["../cs50_problems_2022_x_mario_less.csv", "../cs50_problems_2022_x_mario_more.csv",
                         "../cs50_problems_2022_x_cash.csv", "../cs50_problems_2022_x_credit.csv"]
        args.gradetable = "../grade_table.csv"
        args.distribution_code = ["url1", "url2"]
        args.psetId = 1
        args.tasks = ["less", "more", "cash", "credit"]
        args.archive = True
        args.sentimental = True
        args.choices = ["less-more", "cash-credit"]
        args.plag = True


        self.controller.set_commandline_args(args)

        self.assertEqual(self.controller.InputCS50Csv, args.inputcsv)
        self.assertEqual(self.controller.GradeTable, args.gradetable)
        self.assertEqual(self.controller.DistributionURL, args.distribution_code)
        self.assertEqual(self.controller.ProblemSetName, "Pset1")
        self.assertEqual(self.controller.Tasks, args.tasks)
        self.assertTrue(self.controller.Archive)
        self.assertTrue(self.controller.Sentimental)
        self.assertEqual(self.controller.Choices, [["less", "more"], ["cash", "credit"]])
        self.assertTrue(self.controller.PlagiarismCheck)


    def test_compare_number_of_git_usernames(self):
        self.setUp_Grade_Table()
        # Load values from the grade table file
        with open(self.controller.GradeTable, "r") as file:
            reader = csv.reader(file)
            grade_table_values = [row[0] for row in reader if row]

        # Load values from the created table
        with open('grade_table_Pset1.csv', "r") as file:
            reader = csv.reader(file)
            grade_table_pset1_values = [row[0] for row in reader if row]
        # Compare the number of entered students
        self.assertEqual(grade_table_pset1_values, grade_table_values)
        os.remove('grade_table.csv')
        os.remove('grade_table_Pset1.csv')

    def test_write_grade_table_values(self):
        # This test checks, if the correct value got inserted into the created table
        # Students who passed should obtain the value 1
        # Students who plagiarised should obtain their similiarity score, provided by the plag tool
        # Students who did not participate should obatin the value 0
        self.setUp_Grade_Table()
        with open('grade_table_Pset1.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Git_username"] in self.plagiarising_students:
                    self.assertEqual(row[self.controller.ProblemSetName], "Similarity_" + str(self.student_results_final[row["Git_username"]]["PlagConfidence"]))
                elif row["Git_username"] in self.passing_students and row["Git_username"] not in self.plagiarising_students:
                    self.assertEqual(row[self.controller.ProblemSetName], "1")
                else:
                    self.assertEqual(row[self.controller.ProblemSetName], "0")

        # Clean up the file created during the test
        os.remove('grade_table.csv')
        os.remove('grade_table_Pset1.csv')

if __name__ == "__main__":
    unittest.main()
