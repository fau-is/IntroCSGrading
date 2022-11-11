import shutil
import zipfile
from csv import DictReader, DictWriter
from cmd_parser import parse_args
from pathlib import Path
from bs4 import BeautifulSoup
import os
import requests
import subprocess
from threading import Thread


slugs = []

result_paths = []

sentimental = False
archive = False


def read_csv_into_dict(path):
    with open(path) as f:
        reader = DictReader(f)
        submission_dict = {}
        for row in reader:
            submission_dict[row["github_username"]] = row
        return submission_dict


def get_student_results(infiles_as_dicts):
    result_dict = {}

    for dictionary in infiles_as_dicts:
        for student in dictionary:

            tmp_dict = dictionary[student]

            if tmp_dict["style50_score"] == '' or tmp_dict["style50_score"] == "ERROR":
                style_score = 1
            else:
                style_score = float(tmp_dict["style50_score"])

            if (float(tmp_dict["checks_passed"]) / float(tmp_dict["checks_run"])) < 0.8 \
                    or style_score < 0.8:
                continue
            else:
                if student in result_dict:
                    result_dict[student]["tasks"] += 1
                    result_dict[student][tmp_dict["slug"]] = tmp_dict["github_url"]
                    if "tasknames" in result_dict[student]:
                        result_dict[student]["tasknames"].append(tmp_dict["slug"].split('/')[-1].lower())
                    else:
                        result_dict[student]["tasknames"] = [tmp_dict["slug"].split('/')[-1].lower()]
                else:
                    result_dict[student] = {"tasks": 1, tmp_dict["slug"]: tmp_dict["github_url"],
                                        "tasknames": [tmp_dict["slug"].split('/')[-1].lower()]}
                if tmp_dict["slug"] not in slugs:
                    slugs.append(tmp_dict["slug"])

    return result_dict


# Press the green button in the gutter to run the script.
def plagiarism_check(result_dict):
    threads = []
    for slug in slugs:
        t = Thread(target=run_compare50, args=(slug,))
        threads.append(t)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    for abs_result_path in result_paths:
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
    return result_dict


def run_compare50(slug):
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
    result_paths.append(abs_result_path)


def clean_dir(student_path):
    student_path = os.path.join(os.getcwd(), student_path)
    for directory in os.listdir(student_path):
        if os.path.isdir(os.path.join(student_path, directory)):
            for f in os.listdir(os.path.join(student_path, directory)):
                shutil.move(os.path.join(student_path, directory, f), os.path.join(student_path, f))
        if os.path.isdir(os.path.join(student_path, directory)):
            os.rmdir(os.path.join(student_path, directory))
        else:
            os.remove(os.path.join(student_path, directory))


def download_submission(result_dict, slug, student):
    if slug not in result_dict[student]:
        return
    student_path = f"submissions/{slug.replace('/', '_')}/{student}.zip"
    if os.path.exists(''.join(student_path.split('.')[:-1])):
        return
    # TODO Add a way for getting token
    token = None # Change this line to your personal access token.
    url = f"https://github.com/me50/{student}/archive/{result_dict[student][slug].split('/')[-1]}.zip"
    headers = {'Authorization': f'token {token}'}
    r = requests.get(url, stream=True, headers=headers)
    with open(student_path, "wb") as fd:
        for chunk in r.iter_content(chunk_size=1024):
            fd.write(chunk)
    with zipfile.ZipFile(student_path) as zip_file:
        zip_file.extractall(''.join(student_path.split('.')[:-1]))
    os.remove(student_path)
    clean_dir(''.join(student_path.split('.')[:-1]))


def submission_downloader(result_dict):
    if not Path("submissions").is_dir():
        os.mkdir("submissions")
    for slug in slugs:
        if not Path(f"submissions/{slug.replace('/','_')}").is_dir():
            os.mkdir(f"submissions/{slug.replace('/','_')}")
        threads = []
        for student in result_dict:
            t = Thread(target=download_submission, args=(result_dict, slug, student))
            threads.append(t)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()



def distro_downloader(url):
    r = requests.get(url, stream=True)
    distro_path = f"submissions/distribution.zip"
    with open(distro_path, "wb") as fd:
        for chunk in r.iter_content(chunk_size=1024):
            fd.write(chunk)
    with zipfile.ZipFile(distro_path) as zip_file:
        zip_file.extractall(''.join(distro_path.split('.')[:-1]))
    os.remove(os.path.join(os.getcwd(), "submissions", "distribution.zip"))


def append_grade_table(gradetable, results, pset_name, passing_students, plagiarism=None):
    with open(gradetable) as fi:
        with open(''.join(gradetable.split('.')[:-1]) + "_" + pset_name + ".csv" , 'w') as fo:
            reader = DictReader(fi)
            fieldnames = reader.fieldnames
            if pset_name not in fieldnames:
                fieldnames = fieldnames + [pset_name]
            writer = DictWriter(fo, fieldnames)
            writer.writeheader()

            for row in reader:
                if pset_name in row and row[pset_name] not in {'0', '1'}:
                    writer.writerow(row)
                    continue
                elif row["Git_username"] in passing_students:
                    row[pset_name] = 1
                elif row["Git_username"] in plagiarism:
                    row[pset_name] = "Similarity_" + str(results[row["Git_username"]]["PlagConfidence"])
                else:
                    row[pset_name] = 0

                writer.writerow(row)


if __name__ == '__main__':

    args = parse_args()
    infiles = args.inputcsv
    gradetable = args.gradetable
    distro = args.distribution_code
    pset_name = "Pset" + args.psetId
    tasks = args.tasks
    archive = args.archive
    sentimental = args.sentimental
    choices = []
    if args.choices is not None:
        for choice in args.choices:
            tmp = choice.split("-")
            choices.append(tmp)

    infiles_as_dicts = []
    for file in infiles:
        infiles_as_dicts.append(read_csv_into_dict(file))

    results = get_student_results(infiles_as_dicts)

    passing_students = []
    for student in results:
        if "tasknames" in results[student] and set(tasks) <= set(results[student]["tasknames"]):
            if len(choices) > 0:
                choice_fulfilled = False
                for choice in choices:
                    tmp = False
                    for task in choice:
                        if task in results[student]["tasknames"]:
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
                passing_students.append(student)

    submission_downloader(results)

    if distro:
        for url in distro:
            distro_downloader(url)

    plagiarism = []
    if args.plag:
        results = plagiarism_check(results)

        for student in results:
            if "IsPlag" in results[student] and results[student]["IsPlag"]:
                if student in passing_students:
                    passing_students.remove(student)
                plagiarism.append(student)

    append_grade_table(gradetable, results, pset_name, passing_students, plagiarism)








