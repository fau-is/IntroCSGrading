"""
Main function for running the check
"""
from .controller import Controller
from .downloader import Downloader
from .plagiarism import Plagiarism
from .results import ResultsGenerator
from .cmd_parser import parse_args


def main():
    """
    Main function
    :return: None
    """
    args = parse_args()
    controller = Controller()
    controller.set_commandline_args(args)

    results_generator = ResultsGenerator()
    results_generator.load_reformat_cs50_dicts(controller.input_cs50_csv)
    results_generator.get_student_results(controller.slugs, controller.tasks, controller.choices)

    results = results_generator.student_results_preliminary

    if controller.plagiarism_check:
        downloader = Downloader()

        downloader.submission_downloader(controller.slugs, results)

        if controller.distribution_url:
            for url in controller.distribution_url:
                downloader.distro_downloader(url)

        plagiarism_checker = Plagiarism()
        results = plagiarism_checker.run_plagiarism_check(
            controller.slugs, controller.sentimental, controller.archive, results)

        results_generator.update_student_results_plagiarism(results)
    else:
        results_generator.update_results_no_plagiarism()

    controller.write_grade_table(
        results_generator.student_results_final, results_generator.passing_students,
        results_generator.plagiarising_students)


if __name__ == "__main__":
    main()
