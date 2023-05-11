from csv import DictReader


class ResultsGenerator:
    def __init__(self):
        self.__submit50CsvDicts: list = []
        self.__studentResultsExtracted: dict = dict()
        self.__passingStudents: list = []
        self.__studentResultsFinal: dict = dict()
        self.__plagiarisingStudents: list = []

    @property
    def PlagiarisingStudents(self) -> list:
        return self.__plagiarisingStudents

    @property
    def PassingStudents(self):
        """

        :return: A list of all the students who pass the current problem set.
        """
        return self.__passingStudents

    @property
    def CS50FilesAsDict(self):
        return self.__submit50CsvDicts

    @property
    def StudentResultsPreliminary(self):
        return self.__studentResultsExtracted

    @property
    def StudentResultsFinal(self):
        return self.__studentResultsFinal

    def load_reformat_CS50_dicts(self, cs50CsvList) -> None:
        #TODO check if path exists
        for file in cs50CsvList:
            self.__read_CS50csv_into_dict(file)

    def __read_CS50csv_into_dict(self, path) -> None:
        with open(path) as f:
            reader = DictReader(f)
            submission_dict = dict()
            for row in reader:
                submission_dict[row["github_username"]] = row
            self.__submit50CsvDicts.append(submission_dict)

    def get_student_results(self, slugs, tasks, choices):
        self.__calculate_individual_task_results(slugs)
        self.__cumulate_tasks_into_full_results(tasks, choices)

    def __calculate_individual_task_results(self, slugs):
        for dictionary in self.CS50FilesAsDict:
            for student in dictionary:

                student_dict = dictionary[student]

                if student_dict["style50_score"] == '' or student_dict["style50_score"] == "ERROR":
                    style_score = 1
                else:
                    style_score = float(student_dict["style50_score"])

                if (float(student_dict["checks_passed"]) / float(student_dict["checks_run"])) < 0.8 \
                        or style_score < 0.8:
                    continue
                else:
                    if student in self.__studentResultsExtracted:
                        self.__studentResultsExtracted[student]["tasks"] += 1
                        self.__studentResultsExtracted[student][student_dict["slug"]] = student_dict["github_url"]
                        if "tasknames" in self.__studentResultsExtracted[student]:
                            self.__studentResultsExtracted[student]["tasknames"].append(student_dict["slug"].split('/')[-1].lower())
                        else:
                            self.__studentResultsExtracted[student]["tasknames"] = [student_dict["slug"].split('/')[-1].lower()]
                    else:
                        self.__studentResultsExtracted[student] = {"tasks": 1, student_dict["slug"]: student_dict["github_url"],
                                            "tasknames": [student_dict["slug"].split('/')[-1].lower()]}
                    if student_dict["slug"] not in slugs:
                        slugs.append(student_dict["slug"])

    def __cumulate_tasks_into_full_results(self, tasks, choices):
        for student in self.__studentResultsExtracted:
            choice_fulfilled = False
            if "tasknames" in self.__studentResultsExtracted[student]:
                if set(self.__studentResultsExtracted[student]["tasknames"]) >= set(tasks):
                    self.__passingStudents.append(student)
                elif len(choices) > 0:
                    choice_fulfilled = False
                    for choice in choices:
                        tmp = False
                        for task in choice:
                            if task in self.__studentResultsExtracted[student]["tasknames"]:
                                tmp = True
                                break
                        if not tmp:
                            choice_fulfilled = False
                            break
                        else:
                            choice_fulfilled = True
                else:
                    choice_fulfilled = True

                if choice_fulfilled:
                    self.__passingStudents.append(student)

    def update_student_results_plagiarism(self, result_dict_after_plagiarism):
        self.__studentResultsFinal = result_dict_after_plagiarism
        for student in self.__studentResultsFinal:
            if "IsPlag" in self.__studentResultsFinal[student] and self.__studentResultsFinal[student]["IsPlag"]:
                if student in self.__passingStudents:
                    self.__passingStudents.remove(student)
                self.__plagiarisingStudents.append(student)

    def update_results_no_plagiarism(self):
        self.__studentResultsFinal = self.__studentResultsExtracted

