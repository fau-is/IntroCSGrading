from .controller import Controller
from .downloader import Downloader
from .plagiarism import Plagiarism
from .results import ResultsGenerator
from .cmd_parser import parse_args


def main():
    args = parse_args()
    controller = Controller()
    controller.set_commandline_args(args)

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


if __name__ == "__main__":
    main()



