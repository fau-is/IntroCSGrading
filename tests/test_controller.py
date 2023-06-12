import json
import unittest
from unittest.mock import MagicMock
from psgrade.controller import Controller
import os
import csv
import shutil


class TestController(unittest.TestCase):
    """A test class for the Controller class."""

    def setUp(self):
        """
        Setup function to prepare necessary objects for the tests.
        """
        self.grade_table_link = 'Resources/grade_table_Pset1.csv'
        self.student_results_link = 'Resources/student_results_final.json'
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
        """
        A function to load the final student results from a JSON file.

        Returns:
            data (dict): A dictionary with student results data.
        """
        with open(self.student_results_link, "r") as file:
            data = json.load(file)
        return data

    def test_initial_empty_values(self):
        """
        Test if the controller constructor works without any command line arguments.
        """
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

    def test_property_types(self):
        """
        Test if the controller properties return the expected types or None.
        """
        self.assertIsInstance(self.controller.PlagiarismCheck, (bool, type(None)))
        self.assertIsInstance(self.controller.Choices, (list, type(None)))
        if self.controller.Choices is not None:
            for choice in self.controller.Choices:
                self.assertIsInstance(choice, list)
        self.assertIsInstance(self.controller.Tasks, (list, type(None)))
        self.assertIsInstance(self.controller.ProblemSetName, (str, type(None)))
        self.assertIsInstance(self.controller.DistributionURL, (list, type(None)))
        self.assertIsInstance(self.controller.GradeTable, (str, type(None)))
        self.assertIsInstance(self.controller.InputCS50Csv, (list, type(None)))
        self.assertIsInstance(self.controller.Slugs, (list, type(None)))
        self.assertIsInstance(self.controller.ResultsPaths, (list, type(None)))
        self.assertIsInstance(self.controller.Sentimental, (bool, type(None)))
        self.assertIsInstance(self.controller.Archive, (bool, type(None)))

    def test_set_commandline_args(self):
        """
        Test if the provided command-line arguments got assigned properly to the controller object.
        """
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
        """
        Test if all students from the grade_table can be found in the newly created table.
        Compare the number of entered students.
        """
        with open(self.controller.GradeTable, "r") as file:
            reader = csv.reader(file)
            grade_table_values = [row[0] for row in reader if row]

        with open('Resources/grade_table_Pset1.csv', "r") as file:
            reader = csv.reader(file)
            grade_table_pset1_values = [row[0] for row in reader if row]

        self.assertEqual(grade_table_pset1_values, grade_table_values)

    def test_write_grade_table_values_successful(self):
        """
        Test if the correct value got inserted into the created table.
        Students who passed should obtain the value 1.
        """
        with open(self.grade_table_link, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Git_username"] in self.passing_students and row[
                    "Git_username"] not in self.plagiarising_students:
                    self.assertEqual(row[self.controller.ProblemSetName], "1")

    def test_write_grade_table_values_no_participation(self):
        """
        Test if the correct value got inserted into the created table.
        Students who did not participate should obtain the value 0.
        """
        with open(self.grade_table_link, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Git_username"] not in self.passing_students and row[
                    "Git_username"] not in self.plagiarising_students:
                    self.assertEqual(row[self.controller.ProblemSetName], "0")

    def test_write_grade_table_values_plagiarised(self):
        """
        Test if the correct value got inserted into the created table.
        Students who plagiarised should obtain their similarity score, provided by the plagiarism tool.
        """
        with open(self.grade_table_link, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Git_username"] in self.plagiarising_students:
                    self.assertEqual(row[self.controller.ProblemSetName], "Similarity_" + str(
                        self.student_results_final[row["Git_username"]]["PlagConfidence"]))


if __name__ == "__main__":
    unittest.main()
