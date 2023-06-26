"""
Generates the result dictionaries which are later
used to grade the student's submission for one week.
"""
from os.path import exists
from csv import DictReader


class ResultsGenerator:
    """
    Generates the result dictionaries which are later
    used to grade the student's submission for one week.
    """
    def __init__(self):
        self.__submit50_csv_dicts: [] = []
        self.__student_results_extracted: {} = {}
        self.__passing_students: [] = []
        self.__student_results_final: {} = {}
        self.__plagiarising_students: [] = []

    @property
    def plagiarising_students(self) -> list:
        """
        returns a list of all plagiarizing students
        :return: List of plagiarizing students
        """
        return self.__plagiarising_students

    @property
    def passing_students(self):
        """
        :return: A list of all the students who pass the current problem set.
        """
        return self.__passing_students

    @property
    def cs50_files_as_dict(self):
        """
        stores the files from submit50 as dict
        :return: dictionary of all submit50
        """
        return self.__submit50_csv_dicts

    @property
    def student_results_preliminary(self):
        """
        Student results extracted but not double-checked
        :return: results dict after extraction from files
        """
        return self.__student_results_extracted

    @property
    def student_results_final(self):
        """

        :return:
        """
        return self.__student_results_final

    def load_reformat_cs50_dicts(self, cs50_csv_list:list) -> None:
        """
        Reads submit50 dicts and loads them into a property
        :param cs50_csv_list: list of the paths to the csv files
        :return: None
        """
        for file in cs50_csv_list:
            if not exists(file):
                continue
            self.__read_cs50csv_into_dict(file)

    def __read_cs50csv_into_dict(self, path) -> None:
        with open(path, encoding="UTF-8") as submit50_file:
            reader = DictReader(submit50_file)
            submission_dict = {}
            for row in reader:
                submission_dict[row["github_username"]] = row
            self.__submit50_csv_dicts.append(submission_dict)

    def get_student_results(self, slugs, tasks, choices) -> None:
        """
        Calculates student results for all tasks based on a slug.
        The method also takes choices into account (e.g. less-more)
        :param slugs: slug list
        :param tasks: task list
        :param choices: choice list
        :return: None
        """
        self.__calculate_individual_task_results(slugs)
        self.__cumulate_tasks_into_full_results(tasks, choices)

    def __calculate_individual_task_results(self, slugs):
        """
        Calculates the results for all students for all slugs individually
        :param slugs: list of the slugs to be checked
        :return: None
        """
        for dictionary in self.cs50_files_as_dict:
            for student in dictionary:

                student_dict = dictionary[student]
                style50_score, checks_score = extract_scores(student_dict)

                if style50_score in ['', "ERROR"]:
                    style_score = 1
                else:
                    style_score = float(style50_score)

                if checks_score < 0.8 or style_score < 0.8:
                    # Student did not pass
                    continue

                if student in self.__student_results_extracted:
                    self.__student_results_extracted[student]["tasks"] += 1
                    self.__student_results_extracted[student][student_dict["slug"]] = \
                        student_dict["github_url"]
                    if "tasknames" in self.__student_results_extracted[student]:
                        self.__student_results_extracted[student]["tasknames"]\
                            .append(student_dict["slug"].split('/')[-1].lower())
                else:
                    self.__student_results_extracted[student] = \
                        {"tasks": 1, student_dict["slug"]: student_dict["github_url"],
                         "tasknames": [student_dict["slug"].split('/')[-1].lower()]}
                if student_dict["slug"] not in slugs:
                    slugs.append(student_dict["slug"])

    def __cumulate_tasks_into_full_results(self, tasks, choices) -> None:
        """
        Sums up all task results
        :param tasks: tasks to be done in the week
        :param choices: choices which can be made this week
        :return: None
        """
        for student_name, results in self.__student_results_extracted.items():
            choice_fulfilled = False
            if 'tasknames' in results and set(results['tasknames']) >= set(tasks):
                self.__passing_students.append(student_name)
            elif len(choices) > 0:
                choice_fulfilled = True
                for choice in choices:
                    if len(set(choice).intersection(
                            set(results['tasknames']))) < 1:
                        choice_fulfilled = False
                        break
                if choice_fulfilled:
                    self.__passing_students.append(student_name)

    def update_student_results_plagiarism(self, result_dict_after_plagiarism: {}) -> None:
        """
        If students plagiarize the list of passing and plagiarizing students
        is updated
        :param result_dict_after_plagiarism: dict containing the plagiarism check results
        :return: None
        """
        self.__student_results_final = result_dict_after_plagiarism
        for student in self.__student_results_final:
            if self.__student_results_final[student].get("IsPlag") is not None:
                if student in self.__passing_students:
                    self.__passing_students.remove(student)
                self.__plagiarising_students.append(student)

    def update_results_no_plagiarism(self):
        """
        Updates the final result list used for grading
        :return:
        """
        self.__student_results_final = self.__student_results_extracted


def extract_scores(student_dict):
    """
    Function to extract some scores from an HTML
    :param student_dict:  dict of the student (HTML)
    :return: style50_score and checks_score
    """
    style50_score = student_dict["style50_score"]
    checks_passed = float(student_dict["checks_passed"])
    checks_run = float(student_dict["checks_run"])
    checks_score = checks_passed / checks_run
    return style50_score, checks_score
