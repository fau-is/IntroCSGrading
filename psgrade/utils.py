"""
Simple functions that simplify life
"""


def thread_runner(threads: []) -> None:
    """
    Runs and joins threads
    :param threads: list of threads to be executed
    :return: None
    """
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
