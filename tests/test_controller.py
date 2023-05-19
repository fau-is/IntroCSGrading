import json
import unittest
from unittest.mock import MagicMock
from psgrade.controller import Controller
import os
import csv
import shutil

class TestController(unittest.TestCase):
    def setUp(self):
        self.controller = Controller()
        self.args = MagicMock()
        self.args.inputcsv = ["Resources/cs50_problems_2022_x_mario_less.csv",
                              "Resources/cs50_problems_2022_x_mario_more.csv",
                              "Resources/cs50_problems_2022_x_cash.csv",
                              "Resources/cs50_problems_2022_x_credit.csv"]
        self.args.gradetable = "Resources/grade_table.csv"
        self.args.distribution_code = None
        self.args.psetId = '1'
        self.args.tasks = ["less", "more", "cash", "credit"]
        self.args.choices = ["less-more", "cash-credit"]
        self.args.archive = True
        self.args.sentimental = True
        self.args.plag = True
        self.controller.set_commandline_args(self.args)
        self.student_results_final = self.get_student_results_final()
        self.passing_students = [
            'Gituser1', 'Gituser2', 'Gituser4', 'Gituser5',
            'Gituser6', 'Gituser7', 'Gituser8', 'Gituser9', 'Gituser10'
        ]
        self.plagiarising_students = ['Gituser3']
        self.controller.write_grade_table(self.student_results_final, self.passing_students, self.plagiarising_students)

    def get_student_results_final(self):
        with open("Resources/student_results_final.json", "r") as file:
            data = json.load(file)
        return data

    def test_initial_empty_values(self):
        # This test checks, if the constructor works without any command line arguments
        self.controller = Controller()
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
        # This test checks, if the provided arguments got assigned properly to the controller object
        self.assertEqual(self.controller.InputCS50Csv, self.args.inputcsv)
        self.assertEqual(self.controller.GradeTable, self.args.gradetable)
        self.assertEqual(self.controller.DistributionURL, self.args.distribution_code)
        self.assertEqual(self.controller.ProblemSetName, "Pset1")
        self.assertEqual(self.controller.Tasks, self.args.tasks)
        self.assertTrue(self.controller.Archive)
        self.assertTrue(self.controller.Sentimental)
        self.assertEqual(self.controller.Choices, [["less", "more"], ["cash", "credit"]])
        self.assertTrue(self.controller.PlagiarismCheck)

    def test_compare_number_of_git_usernames(self):
        # This test checks, if all the students of the grade_table can be found in the newly create table
        # Load values from the grade table file
        with open(self.controller.GradeTable, "r") as file:
            reader = csv.reader(file)
            grade_table_values = [row[0] for row in reader if row]

        # Load values from the created table
        with open('Resources/grade_table_Pset1.csv', "r") as file:
            reader = csv.reader(file)
            grade_table_pset1_values = [row[0] for row in reader if row]
        # Compare the number of entered students
        self.assertEqual(grade_table_pset1_values, grade_table_values)

    def test_write_grade_table_values_successful(self):
        # This test checks, if the correct value got inserted into the created table
        # Students who passed should obtain the value 1
        with open('Resources/grade_table_Pset1.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
               if row["Git_username"] in self.passing_students and row["Git_username"] not in self.plagiarising_students:
                    self.assertEqual(row[self.controller.ProblemSetName], "1")

    def test_write_grade_table_values_no_participation(self):
        # This test checks, if the correct value got inserted into the created table
        # Students who did not participate should obatin the value 0
        with open('Resources/grade_table_Pset1.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Git_username"] not in self.passing_students and row["Git_username"] not in self.plagiarising_students:
                    self.assertEqual(row[self.controller.ProblemSetName], "0")

    def test_write_grade_table_values_plagiarised(self):
        # This test checks, if the correct value got inserted into the created table
        # Students who plagiarised should obtain their similiarity score, provided by the plag tool
        with open('Resources/grade_table_Pset1.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Git_username"] in self.plagiarising_students:
                    self.assertEqual(row[self.controller.ProblemSetName], "Similarity_" + str(self.student_results_final[row["Git_username"]]["PlagConfidence"]))


if __name__ == "__main__":
    unittest.main()
