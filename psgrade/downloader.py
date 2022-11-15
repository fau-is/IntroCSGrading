import os
import requests
import zipfile
import getpass
import shutil

from pathlib import Path
from threading import Thread





class Downloader:
    def __init__(self):
        self.__token = Downloader.__get_token_from_user()

    def submission_downloader(self, slugs, results):
        if not Path("submissions").is_dir():
            os.mkdir("submissions")
        for slug in slugs:
            if not Path(f"submissions/{slug.replace('/', '_')}").is_dir():
                os.mkdir(f"submissions/{slug.replace('/', '_')}")
            threads = []
            for student in results:
                t = Thread(target=self.__download_submission, args=(results, slug, student))
                threads.append(t)
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

    def __download_submission(self, result_dict, slug, student):
        if slug not in result_dict[student]:
            return
        student_path = f"submissions/{slug.replace('/', '_')}/{student}.zip"
        if os.path.exists(''.join(student_path.split('.')[:-1])):
            return
        url = f"https://github.com/me50/{student}/archive/{result_dict[student][slug].split('/')[-1]}.zip"
        headers = {'Authorization': f'token {self.__token}'}
        r = requests.get(url, stream=True, headers=headers)
        with open(student_path, "wb") as fd:
            for chunk in r.iter_content(chunk_size=1024):
                fd.write(chunk)
        with zipfile.ZipFile(student_path) as zip_file:
            zip_file.extractall(''.join(student_path.split('.')[:-1]))
        os.remove(student_path)
        Downloader.clean_dir(''.join(student_path.split('.')[:-1]))

    @staticmethod
    def distro_downloader(url):
        r = requests.get(url, stream=True)
        distro_path = f"submissions/distribution.zip"
        with open(distro_path, "wb") as fd:
            for chunk in r.iter_content(chunk_size=1024):
                fd.write(chunk)
        with zipfile.ZipFile(distro_path) as zip_file:
            zip_file.extractall(''.join(distro_path.split('.')[:-1]))
        os.remove(os.path.join(os.getcwd(), "submissions", "distribution.zip"))

    @staticmethod
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

    @staticmethod
    def __get_token_from_user():
        return getpass.getpass("Enter GitHub Access Token")


