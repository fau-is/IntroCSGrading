"""
Overall controller of other modules in the grading package
"""
from csv import DictReader, DictWriter


# pylint: disable=too-many-instance-attributes
class Controller:
    """
    Controller class which coordinates the execution of all
    modules.
    """

    def __init__(self):
        self.__plagiarism_check: bool = False
        self.__sentimental: bool = False
        self.__archive: bool = False

        self.__slugs: list = []
        self.__result_paths: list = []
        self.__input_files_submit50: list = []
        self.__distribution_code_url: list = []
        self.__grade_table: str = ""
        self.__problem_set_name = ""
        self.__tasks = []
        self.__choices = []

    @property
    def plagiarism_check(self) -> bool:
        """Returns the state of the plagiarism check attribute."""
        return self.__plagiarism_check

    @property
    def choices(self) -> list:
        """Returns the list of choice attribute."""
        return self.__choices

    @property
    def tasks(self) -> list:
        """Returns the list of task attribute."""
        return self.__tasks

    @property
    def problem_set_name(self) -> str:
        """Returns the problem set name attribute."""
        return self.__problem_set_name

    @property
    def distribution_url(self):
        """Returns the distribution code URL attribute."""
        return self.__distribution_code_url

    @property
    def grade_table(self) -> str or None:
        """Returns the grade table attribute."""
        return self.__grade_table

    @property
    def input_cs50_csv(self) -> [] or None:
        """Returns the input files for CS50 in CSV format attribute."""
        return self.__input_files_submit50

    @property
    def slugs(self) -> [] or None:
        """Returns the slugs attribute."""
        return self.__slugs

    @property
    def results_paths(self) -> [] or None:
        """Returns the result paths attribute."""
        return self.__result_paths

    @property
    def sentimental(self) -> bool:
        """Returns the state of the sentimental attribute."""
        return self.__sentimental

    @property
    def archive(self) -> bool:
        """Returns the state of the archive attribute."""
        return self.__archive

    def set_commandline_args(self, args) -> None:
        """
        Sets the attributes according to the command line arguments provided.
        :param args: args parsed by cmd parser
        :return: None
        """
        self.__input_files_submit50 = args.input_csv
        self.__grade_table = args.gradetable
        self.__distribution_code_url = args.distribution_code
        self.__problem_set_name = f"Pset{args.psetId}"
        self.__tasks = args.tasks
        self.__archive = args.archive
        self.__sentimental = args.sentimental
        self.__choices = []
        self.__plagiarism_check = args.plag
        if args.choices:
            self.__choices = [choice.split("-") for choice in args.choices]

    def write_grade_table(self, results: dict, passing_students: list, plagiarism=None) -> None:
        """
        This function writes the grade table.
        Passing students receive 1, failing students value 0 and
        students accused of plagiarism their similarity score.
        :param results: The results dict
        :param passing_students: The list of passing students
        :param plagiarism: The list of students who have plagiarized
        :return:
        """
        with open(self.__grade_table, encoding="UTF-8") as input_grade_table:
            with open(''.join(self.__grade_table.split('.')[:-1]) + "_"
                      + self.__problem_set_name + ".csv", 'w', encoding="UTF-8") as out_file:
                reader = DictReader(input_grade_table)
                fieldnames = reader.fieldnames
                if self.__problem_set_name not in fieldnames:
                    fieldnames = fieldnames + [self.__problem_set_name]
                writer = DictWriter(out_file, fieldnames)
                writer.writeheader()

                for row in reader:
                    if self.__problem_set_name in row and \
                            row[self.__problem_set_name] not in {'0', '1'}:
                        writer.writerow(row)
                        continue
                    if row["Git_username"] in passing_students:
                        row[self.__problem_set_name] = 1
                    elif len(plagiarism) > 0 and row["Git_username"] in plagiarism:
                        row[self.__problem_set_name] = "Similarity_" + str(
                            results[row["Git_username"]]["PlagConfidence"])
                    else:
                        row[self.__problem_set_name] = 0

                    writer.writerow(row)
