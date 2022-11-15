from csv import DictReader, DictWriter

from Input.cmd_parser import parse_args
from Results.results import ResultsGenerator
from Plagiarism.downloader import Downloader
from Plagiarism.plagiarism import Plagiarism


class Controller(object):

    def __init__(self):
        self.__slugs: list = []
        self.__resultPaths: list = []
        self.__plagiarismCheck: bool = False
        self.__sentimental: bool = False
        self.__archive: bool = False
        self.__inputFilesSubmit50: list = []
        self.__distributionCodeURL: list = []
        self.__gradeTable: str = ""
        self.__psetName = ""
        self.__tasks = []
        self.__choices = []

    @property
    def PlagiarismCheck(self) -> bool:
        return self.__plagiarismCheck

    @property
    def Choices(self) -> list:
        return self.__choices

    @property
    def Tasks(self) -> list:
        return self.__tasks

    @property
    def ProblemSetName(self) -> str:
        return self.__psetName

    @property
    def DistributionURL(self):
        return self.__distributionCodeURL

    @property
    def GradeTable(self) -> str or None:
        return self.__gradeTable

    @property
    def InputCS50Csv(self) -> [] or None:
        return self.__inputFilesSubmit50

    @property
    def Slugs(self) -> [] or None:
        return self.__slugs

    @property
    def ResultsPaths(self) -> [] or None:
        return self.__resultPaths

    @property
    def Sentimental(self) -> bool:
        return self.__sentimental

    @property
    def Archive(self) -> bool:
        return self.__archive

    def set_commandline_args(self):
        args = parse_args()
        self.__inputFilesSubmit50 = args.inputcsv
        self.__gradeTable = args.gradetable
        self.__distributionCodeURL = args.distribution_code
        self.__psetName = f"Pset{args.psetId}"
        self.__tasks = args.tasks
        self.__archive = args.archive
        self.__sentimental = args.sentimental
        self.__choices = []
        self.__plagiarismCheck = args.plag
        if args.choices:
            self.__choices = [choice.split("-") for choice in args.choices]

    def write_grade_table(self, results, passing_students, plagiarism=None):
        with open(self.__gradeTable) as fi:
            with open(''.join(self.__gradeTable.split('.')[:-1]) + "_" + self.__psetName + ".csv", 'w') as fo:
                reader = DictReader(fi)
                fieldnames = reader.fieldnames
                if self.__psetName not in fieldnames:
                    fieldnames = fieldnames + [self.__psetName]
                writer = DictWriter(fo, fieldnames)
                writer.writeheader()

                for row in reader:
                    if self.__psetName in row and row[self.__psetName] not in {'0', '1'}:
                        writer.writerow(row)
                        continue
                    elif row["Git_username"] in passing_students:
                        row[self.__psetName] = 1
                    elif len(plagiarism) > 0 and row["Git_username"] in plagiarism:
                        row[self.__psetName] = "Similarity_" + str(results[row["Git_username"]]["PlagConfidence"])
                    else:
                        row[self.__psetName] = 0

                    writer.writerow(row)


def main():
    controller = Controller()
    controller.set_commandline_args()

    results_generator = ResultsGenerator()
    results_generator.load_reformat_CS50_dicts(controller.InputCS50Csv)
    results_generator.get_student_results(controller.Slugs, controller.Tasks, controller.Choices)

    results = results_generator.StudentResultsPreliminary

    if controller.PlagiarismCheck:
        downloader = Downloader()

        downloader.submission_downloader(controller.Slugs, results)

        if controller.DistributionURL:
            for url in controller.DistributionURL:
                downloader.distro_downloader(url)

        plagiarism_checker = Plagiarism()
        results = plagiarism_checker.run_plagiarism_check(controller.Slugs, controller.Sentimental, controller.Archive, results)

        results_generator.update_student_results_plagiarism(results)
    else:
        results_generator.update_results_no_plagiarism()

    controller.write_grade_table(results_generator.StudentResultsFinal,
                                 results_generator.PassingStudents, results_generator.PlagiarisingStudents)


if __name__ == '__main__':
    main()








