# coding=utf-8
"""Contains methods for command line interaction"""
import argparse


def parse_args():
    """
    Creates the argument parser for the command line
    :return: the args that were parsed from the command line
    """
    # This file contains the commandline tools for the current tool
    parser = argparse.ArgumentParser(prog='psgrade')
    parser.add_argument('--inputcsv', nargs='*', help='The input csv', required=True)
    parser.add_argument('--gradetable', help='The grade table to ba amended', required=True)
    parser.add_argument('--plag', default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument('--distribution_code', nargs='*')
    parser.add_argument('--psetId', type=str, required=True)
    parser.add_argument('--tasks', nargs='*', type=str.lower)
    parser.add_argument('--choices', nargs='*', type=str.lower, help="e.g.: task1-task2 task3-task4-task5")
    parser.add_argument("--archive",  default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument("--sentimental",  default=False, action=argparse.BooleanOptionalAction)

    return parser.parse_args()
