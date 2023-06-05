from csv import DictReader, DictWriter

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
        """Returns the state of the plagiarism check attribute."""
        return self.__plagiarismCheck

    @property
    def Choices(self) -> list:
        """Returns the list of choices attribute."""
        return self.__choices

    @property
    def Tasks(self) -> list:
        """Returns the list of tasks attribute."""
        return self.__tasks

    @property
    def ProblemSetName(self) -> str:
        """Returns the problem set name attribute."""
        return self.__psetName

    @property
    def DistributionURL(self):
        """Returns the distribution code URL attribute."""
        return self.__distributionCodeURL

    @property
    def GradeTable(self) -> str or None:
        """Returns the grade table attribute."""
        return self.__gradeTable

    @property
    def InputCS50Csv(self) -> [] or None:
        """Returns the input files for CS50 in CSV format attribute."""
        return self.__inputFilesSubmit50

    @property
    def Slugs(self) -> [] or None:
        """Returns the slugs attribute."""
        return self.__slugs

    @property
    def ResultsPaths(self) -> [] or None:
        """Returns the results paths attribute."""
        return self.__resultPaths

    @property
    def Sentimental(self) -> bool:
        """Returns the state of the sentimental attribute."""
        return self.__sentimental

    @property
    def Archive(self) -> bool:
        """Returns the state of the archive attribute."""
        return self.__archive

    def set_commandline_args(self, args):
        """Sets the attributes according to the command line arguments provided."""
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
        """
        Writes the grade table based on the results, the list of passing students and the list of students
        who have plagiarized. Passing students receive the value 1, failing students the value 0 and
        plagiarising students the value of the similiarty score.
        """
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
