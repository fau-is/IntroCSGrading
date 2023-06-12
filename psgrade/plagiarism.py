"""
Module to perform plagiarism check with compare50
"""
import subprocess
import os
import shutil

from threading import Thread
from bs4 import BeautifulSoup

from .utils import thread_runner

class Plagiarism:
    """
    Class to coordinate plagiarism check
    """
    def __init__(self):
        """
        Default constructor for creating the two required attributes
        """
        self.__plagiarising_students: set = set()
        self.__result_paths = []

    @property
    def results_path(self) -> list:
        """
        Property for result paths
        :return: list of result paths
        """
        return self.__result_paths

    @property
    def plagiarising_students(self) -> set:
        """
        Property for all students who plagiarized
        :return: Set of plagiarizing students
        """
        return self.__plagiarising_students

    def __run_compare50(self, slug, sentimental: bool = False, archive: bool = False) -> None:
        """
        This function is executed in multiple threads, i.e., in parallel
        Runs compare50 for
        :param slug: slug as a string
        :param sentimental: sentimental problem set (bool); false is default
        :param archive: check archive solutions (boo); false is default
        :return: None
        """
        flags = ["compare50", f"submissions/{slug.replace('/', '_')}/*"]
        # distribution flag if distribution exists
        if os.path.exists(os.path.join(os.getcwd(),
                                       f"submissions/distribution/{slug.split('/')[-1]}")):
            flags.append("-d")
            flags.append(f"submissions/distribution/{slug.split('/')[-1]}/*")

        # output_directory
        flags.append("-o")
        s_flag = ''
        if sentimental:
            if not os.path.exists(os.path.join(os.getcwd(), "plagiarism_results/sentimental")):
                os.makedirs(os.path.join(os.getcwd(), "plagiarism_results/sentimental"))
            s_flag = "sentimental/"
        path_to_results = f"plagiarism_results/{s_flag}{slug.split('/')[-1]}"
        flags.append(path_to_results)

        # Git Solutions
        if archive:
            if sentimental and os.path.exists(f"archive/sentimental/{slug.split('/')[-1]}"):
                flags.append("-a")
                flags.append(f"archive/sentimental/{slug.split('/')[-1]}/*")
            elif os.path.exists(f"archive/{slug.split('/')[-1]}"):
                flags.append("-a")
                flags.append(f"archive/{slug.split('/')[-1]}/*")

        # Get the absolute path of results
        abs_result_path = os.path.join(os.getcwd(), path_to_results)
        if not os.path.exists(os.path.join(os.getcwd(), "plagiarism_results")):
            os.makedirs(os.path.join(os.getcwd(), "plagiarism_results"))
        if os.path.exists(abs_result_path):
            shutil.rmtree(os.path.join(abs_result_path))
        subprocess.run(flags, check=True)
        self.__result_paths.append(abs_result_path)

    def __plagiarism_check(self, slugs: list, sentimental: bool, archive: bool) -> None:
        """
        Runs the plagiarism check in parallel
        :param slugs: for all slugs (list of str)
        :param sentimental: sentimental problem set (bool)
        :param archive: archive solutions (bool)
        :return: None
        """
        threads = []
        for slug in slugs:
            thread = Thread(target=Plagiarism.__run_compare50,
                            args=(self, slug, sentimental, archive,))
            threads.append(thread)
        thread_runner(threads)


    def __get_plagiarism_results(self, result_dict:dict) -> dict:
        """
        Retrieves the plagiarism results from all generated HTML files
        :param result_dict: Dict where students' results are stored
        :return: Dict annotated with plagiarism scores
        """
        for abs_result_path in self.__result_paths:
            for filename in os.listdir(abs_result_path):
                if not filename.startswith("match"):
                    continue
                if not filename.endswith(".html"):
                    continue
                with open(os.path.join(abs_result_path, filename), encoding="UTF-8") as match:
                    soup = BeautifulSoup(match, 'html.parser')
                    for div in soup(id="structuresub_names"):
                        for student in div("h5"):
                            similarity, student_name = self.__extract_student_similarity(student)
                            if similarity > 85 and student_name in result_dict:
                                result_dict[student_name]["IsPlag"] = True
                                result_dict[student_name]["PlagConfidence"] = similarity
                                self.__plagiarising_students.add(student_name)
        return result_dict

    def __extract_student_similarity(self, student):
        string = student.string
        student_name = string.split(' ')[0].split('/')[-1]
        similarity = string.split(' ')[-1]
        similarity = similarity.replace('(', '')
        similarity = similarity.replace(')', '')
        similarity = similarity.replace('%', '')
        similarity = int(similarity)
        return similarity, student_name

    def run_plagiarism_check(self, slugs:list, sentimental:bool,
                             archive:bool, results:dict) -> dict:
        """
        Runs the plagiarism check and annotates the results-dictionary
        :param slugs:
        :param sentimental:
        :param archive:
        :param results:
        :return:
        """
        self.__plagiarism_check(slugs, sentimental, archive)
        return self.__get_plagiarism_results(results)
