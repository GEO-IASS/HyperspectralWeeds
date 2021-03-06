# Written by Andrew Donelick
# andrew.donelick@msu.montana.edu
# 23 March 2016
# Montana State University - Optical Remote Sensing Lab

"""
This script generates training and testing data for machine learning
and analysis from leaf CSV files. This script must be run before any 
machine learning model training can be done, and some analysis scripts
can be run.

Usage:

    python generateTrainingData.py [date] [-d] [-k keywords] [-p byLeaf] [-s saveProportion]

    date: Data collection date YYYY_MMDD
    -d: Determines whether or not to delete the existing
            training/testing data files
    keywords: Data filename keywords
    byLeaf: Should we separate the train/test data
            by leaf, or should we randomly separate
            the data according to a set proportion?
    saveProportion: Amount of each CSV file to save as training
                    and testing data.
"""

import argparse
import os
import sys
import numpy as np
import argparse

sys.path.append("..")
from common import FileIO
from common.Constants import *
from common import DataManipulation


def main(date, delete, keywords=[], byLeaf=True, saveProportion=0.5):
    """
    Generates ML training and testing data from extracted CSV files

    :param date: (string) Data collection date YYYY_MMDD
    :param delete: (boolean) Determines whether or not to delete the existing
                             training/testing data files
    :param keywords: (list of strings) Data filename keywords
    :param byLeaf: (boolean) Should we separate the train/test data
                             by leaf, or should we randomly separate
                             the data according to a set proportion?
    :param saveProportion: (float) Amount of each CSV file to save as training
                                   and testing data.

    :return: (None)
    """

    # Get the data files we will be looking at
    dataPath = DATA_DIRECTORIES[date]
    dataFilenames = FileIO.getDatafileNames(dataPath, keywords)

    # If desired, remove the old training data and start fresh
    if delete:

        mlDataPath = DATA_DIRECTORIES[date+"_ML"]
        trainingDataPath = os.path.join(mlDataPath, TRAINING_DATA_PATH)
        testingDataPath = os.path.join(mlDataPath, TESTING_DATA_PATH)
        sampleCountsPath = os.path.join(mlDataPath, SAMPLE_COUNTS_PATH)

        if os.path.exists(trainingDataPath):
            os.remove(trainingDataPath)

        if os.path.exists(testingDataPath):
            os.remove(testingDataPath)

        if os.path.exists(sampleCountsPath):
            os.remove(sampleCountsPath)

    # Consolidate the CSV files into training and testing data
    (train_X, train_y, test_X, test_y) = DataManipulation.separateTrainTest(dataPath, 
                                                                            dataFilenames, 
                                                                            byLeaf=byLeaf, 
                                                                            saveProportion=saveProportion)

    # Save the training and testing data in the proper spot
    FileIO.saveTrainingData(date, train_X, train_y)
    FileIO.saveTestingData(date, test_X, test_y)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate ML model training data from CSV files')
    parser.add_argument('date', type=str, nargs=1,
                         help='Data collection date YYYY_MMDD')
    parser.add_argument('-d', '--delete', default=False, action='store_true',
                         help="Delete previous training/testing data")
    parser.add_argument('-k', '--keywords', default=[], type=str, nargs='*',
                         help="Filename keywords to include in the data")
    parser.add_argument('-p', '--proportional', default=False, action='store_true',
                         help="Divide the training/testing data proportionally by spectra")
    parser.add_argument('-s', '--saveProportion', default=0.5, type=float, nargs='?',
                         help="How much of each CSV should we save in the training/testing set?")

    args = parser.parse_args()
    byLeaf = not args.proportional
    saveProportion = args.saveProportion
    main(args.date[0], args.delete, args.keywords, byLeaf, saveProportion)



