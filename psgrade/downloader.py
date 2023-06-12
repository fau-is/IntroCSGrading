"""
This module downloads submissions from GitHub via access_token
"""
import os
import zipfile
import getpass
import shutil
from pathlib import Path
from threading import Thread

import requests

from utils import thread_runner


class Downloader:
    """
    Class with functionality to download student submissions from GitHub
    """
    def __init__(self):
        """Constructor getting the Access-Token as a starred string"""
        self.__token = Downloader.__get_token_from_user()

    def submission_downloader(self, slugs:str, results:dict) -> None:
        """
        Parallelized download of submissions in different threads
        :param slugs: slugs for the url to be downloaded
        :param results: dictionary extracted from Submit50-csvs
        :return: None
        """
        if not Path("submissions").is_dir():
            os.mkdir("submissions")
        for slug in slugs:
            if not Path(f"submissions/{slug.replace('/', '_')}").is_dir():
                os.mkdir(f"submissions/{slug.replace('/', '_')}")
            threads = []
            for student in results:
                thread = Thread(target=self.__download_submission, args=(results, slug, student))
                threads.append(thread)
            thread_runner(threads)

    def __download_submission(self, result_dict, slug, student):
        """
        Downloads the submission
        :param result_dict: Dict that contains all student submissions
        :param slug: The slug for the task to be downloaded
        :param student: The student whose submission should be downloaded
        :return: None
        """
        if slug not in result_dict[student]:
            return
        student_path = f"submissions/{slug.replace('/', '_')}/{student}.zip"
        if os.path.exists(''.join(student_path.split('.')[:-1])):
            return
        url = f"https://github.com/me50/{student}" \
              f"/archive/{result_dict[student][slug].split('/')[-1]}.zip"
        headers = {'Authorization': f'token {self.__token}'}
        request = requests.get(url, stream=True, headers=headers, timeout=1000000)
        with open(student_path, "wb") as student_file:
            for chunk in request.iter_content(chunk_size=1024):
                student_file.write(chunk)
        with zipfile.ZipFile(student_path) as zip_file:
            zip_file.extractall(''.join(student_path.split('.')[:-1]))
        os.remove(student_path)
        Downloader.clean_dir(''.join(student_path.split('.')[:-1]))

    @staticmethod
    def distro_downloader(url):
        """
        Downloads the distribution code
        :param url: from this url
        :return: None
        """
        request = requests.get(url, stream=True, timeout=100000)
        distro_path = "submissions/distribution.zip"
        with open(distro_path, "wb") as distribution_file:
            for chunk in request.iter_content(chunk_size=1024):
                distribution_file.write(chunk)
        with zipfile.ZipFile(distro_path) as zip_file:
            zip_file.extractall(''.join(distro_path.split('.')[:-1]))
        os.remove(os.path.join(os.getcwd(), "submissions", "distribution.zip"))

    @staticmethod
    def clean_dir(student_path:str) -> None:
        """
        Deletes all files from a path
        :param student_path: Deletes the student file_path
        :return: None
        """
        student_path = os.path.join(os.getcwd(), student_path)
        for directory in os.listdir(student_path):
            if os.path.isdir(os.path.join(student_path, directory)):
                for file in os.listdir(os.path.join(student_path, directory)):
                    full_path = os.path.join(student_path, directory, file)
                    parent_of_full_path = os.path.join(student_path, file)
                    shutil.move(full_path, parent_of_full_path)
            if os.path.isdir(os.path.join(student_path, directory)):
                os.rmdir(os.path.join(student_path, directory))
            else:
                os.remove(os.path.join(student_path, directory))

    @staticmethod
    def __get_token_from_user():
        """
        Gets an access token from a user
        :return: returns the entered access token
        """
        return getpass.getpass("Enter GitHub Access Token")
