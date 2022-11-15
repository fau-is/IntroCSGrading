import subprocess
import os
import shutil

from threading import Thread
from bs4 import BeautifulSoup


class Plagiarism:
    def __init__(self):
        self.__plagiarisingStudents: set = set()
        self.__resultPaths = []

    @property
    def ResultsPath(self):
        return self.__resultPaths

    @property
    def PlagiarisingStudents(self):
        return self.__plagiarisingStudents

    def __run_compare50(self, slug, sentimental, archive):
        flags = ["compare50", f"submissions/{slug.replace('/', '_')}/*"]
        # distribution flag if distribution exists
        if os.path.exists(os.path.join(os.getcwd(), f"submissions/distribution/{slug.split('/')[-1]}")):
            flags.append("-d")
            flags.append(f"submissions/distribution/{slug.split('/')[-1]}/*")

        # output_directory
        flags.append("-o")
        s = ''
        if sentimental:
            if not os.path.exists(os.path.join(os.getcwd(), "results/sentimental")):
                os.makedirs(os.path.join(os.getcwd(), "results/sentimental"))
            s = "sentimental/"
        path_to_results = f"results/{s}{slug.split('/')[-1]}"
        flags.append(path_to_results)

        # Git Solutions
        if archive:
            if sentimental and os.path.exists(f"archive/sentimental/{slug.split('/')[-1]}"):
                flags.append("-a")
                flags.append(f"archive/sentimental/{slug.split('/')[-1]}/*")
            elif os.path.exists(f"archive/{slug.split('/')[-1]}"):
                flags.append("-a")
                flags.append(f"archive/{slug.split('/')[-1]}/*")

        # Get Absolute path of results
        abs_result_path = os.path.join(os.getcwd(), path_to_results)
        if not os.path.exists(os.path.join(os.getcwd(), "results")):
            os.makedirs(os.path.join(os.getcwd(), "results"))
        if os.path.exists(abs_result_path):
            shutil.rmtree(os.path.join(abs_result_path))
        subprocess.run(flags)
        self.__resultPaths.append(abs_result_path)

    def __plagiarism_check(self, slugs, sentimental, archive):
        threads = []
        for slug in slugs:
            t = Thread(target=Plagiarism.__run_compare50, args=(slug, sentimental, archive))
            threads.append(t)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    def __get_plagiarism_results(self, result_dict):
        for abs_result_path in self.__resultPaths:
            for filename in os.listdir(abs_result_path):
                if not filename.startswith("match"):
                    continue
                if not filename.endswith(".html"):
                    continue
                with open(os.path.join(abs_result_path, filename)) as match:
                    soup = BeautifulSoup(match, 'html.parser')
                    for div in soup(id="structuresub_names"):
                        for student in div("h5"):
                            string = student.string
                            student_name = string.split(' ')[0].split('/')[-1]
                            similarity = int(string.split(' ')[-1].replace('(', '').replace(')', '').replace('%', ''))
                            if similarity > 85 and student_name in result_dict:
                                result_dict[student_name]["IsPlag"] = True
                                result_dict[student_name]["PlagConfidence"] = similarity
                                self.__plagiarisingStudents.add(student_name)
        return result_dict

    def run_plagiarism_check(self, slugs, sentimental, archive, results):
        self.__plagiarism_check(slugs, sentimental, archive)
        return self.__get_plagiarism_results(results)
