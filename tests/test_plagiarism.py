"""
Tests for the plagiarism.py module
"""

import os
from unittest import TestCase
from psgrade.plagiarism import Plagiarism


class TestPlagiarism(TestCase):
    """
    Test Case for Plagiarism
    """
    def setUp(self) -> None:
        """
        You can define variables or constants for a test case here.
        Don't forget to assign them to 'self'
        :return: None
        """
        self.plagiarism = Plagiarism
        self.results = {
            'student1': {'IsPlag': False, 'PlagConfidence': 0},
            'student2': {'IsPlag': False, 'PlagConfidence': 0},
            'student3': {'IsPlag': False, 'PlagConfidence': 0},
            'student4': {'IsPlag': False, 'PlagConfidence': 0}
        }
        self.ctrl_results = {
            'student1': {'IsPlag': True, 'PlagConfidence': 100},
            'student2': {'IsPlag': True, 'PlagConfidence': 100},
            'student3': {'IsPlag': False, 'PlagConfidence': 0},
            'student4': {'IsPlag': False, 'PlagConfidence': 0}
        }

    def test_constructor(self):
        """
        Tests the constructor
        :return:
        """
        self.plagiarism = Plagiarism()
        self.assertIsInstance(self.plagiarism, Plagiarism)
        self.assertEqual(self.plagiarism.plagiarising_students, set())
        self.assertEqual(self.plagiarism.results_path, [])

    def test_run_plagiarism_check(self):
        """
        Run plagiarism check
        :return:
        """
        self.plagiarism = Plagiarism
        plagiarism_instance = self.plagiarism()

        slugs = ['slug1', 'slug2']
        sentimental = False
        archive = False

        # Run the plagiarism check
        plag_results = plagiarism_instance.run_plagiarism_check(
            slugs=slugs, sentimental=sentimental, archive=archive, results=self.results
        )
        self.assertEqual(
            plagiarism_instance.results_path,
            [os.path.dirname(__file__) + '/plagiarism_results/slug1']
        )
        self.assertEqual(plagiarism_instance.plagiarising_students, {'student2', 'student1'})
        self.assertEqual(plag_results, self.ctrl_results)
