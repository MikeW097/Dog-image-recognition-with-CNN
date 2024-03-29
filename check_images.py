#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# */AIPND/intropylab-classifying-images/check_images.py
#
# TODO: 0. Fill in your information in the programming header below
# PROGRAMMER: MikeW
# DATE CREATED: 02/09/2019
# REVISED DATE:             <=(Date Revised - if any)
# REVISED DATE: 05/14/2018 - added import statement that imports the print
#                           functions that can be used to check the lab
# PURPOSE: Check images & report results: read them in, predict their
#          content (classifier), compare prediction to actual value labels
#          and output results
#
# Use argparse Expected Call with <> indicating expected user input:
#      python check_images.py --dir <directory with images> --arch <model>
#             --dogfile <file that contains dognames>
#   Example call:
#    python check_images.py --dir pet_images/ --arch vgg --dogfile dognames.txt
##

# Imports python modules
import argparse
from time import time, sleep
from os import listdir
from classifier import classifier

# Imports classifier function for using CNN to classify images
#from classifier import classifier

# Imports print functions that check the lab
from print_functions_for_lab_checks import *

# Main program function defined below
def main():
    # TODO: 1. Define start_time to measure total program runtime by
    # collecting start time
    start_time = time()

    # TODO: 2. Define get_input_args() function to create & retrieve command
    in_args = get_input_args()
    print("Command Line Message:\n  Folder Direction:   " + in_args.dir\
     +"\nClassifier Method:  " + in_args.arch + "\nDognames: " + in_args.dogfile)

    # TODO: 3. Define get_pet_labels() function to create pet image labels by
    # creating a dictionary with key=filename and value=file label to be used
    # to check the accuracy of the classifier function
    answers_dic = get_pet_labels(in_args.dir)

    # TODO: 4. Define classify_images() function to create the classifier
    # labels with the classifier function using in_arg.arch, comparing the
    # labels, and creating a dictionary of results (result_dic)
    result_dic = classify_images(in_args.dir, answers_dic, in_args.arch)

    # TODO: 5. Define adjust_results4_isadog() function to adjust the results
    # dictionary(result_dic) to determine if classifier correctly classified
    # images as 'a dog' or 'not a dog'. This demonstrates if the model can
    # correctly classify dog images as dogs (regardless of breed)
    adjust_results4_isadog(result_dic, in_args.dogfile)

    n_match = 0
    n_nonmatch = 0

    print("\n       Matches:")
    for key, value in result_dic.items():
        if value[2] == 1:
            n_match += 1
            print("Real: %-26s     Classifier: %-30s      Petlabel: %1d \
                    classifierlabel: %1d"%(value[0], value[1], value[3], value[4]))
    print("\n       Nonmatches:")
    for key, value in result_dic.items():
        if value[2] == 0:
            n_nonmatch += 1
            print("Real: %-26s     Classifier: %-30s      Petlabel: %1d \
                    classifierlabel: %1d"%(value[0], value[1], value[3], value[4]))

    print("\nTotal matches: ", n_match, "\tTotal nonmatches: ", n_nonmatch, "\n")

    # TODO: 6. Define calculates_results_stats() function to calculate
    # results of run and puts statistics in a results statistics
    # dictionary (results_stats_dic)
    results_stats_dic = calculates_results_stats(result_dic)
    print('\npec_correct_dog:  ', results_stats_dic['pec_correct_dog'])
    print('pec_correct_nondog:  ', results_stats_dic['pec_correct_nondog'])
    print('pec_correct_breed:  ', results_stats_dic['pec_correct_breed'])
    print('pec_label_match:  ', results_stats_dic['pec_label_match'])

    # TODO: 7. Define print_results() function to print summary results,
    # incorrect classifications of dogs and breeds if requested.
    print_results()

    # TODO: 1. Define end_time to measure total program runtime
    # by collecting end time
    end_time = time()

    # TODO: 1. Define tot_time to computes overall runtime in
    # seconds & prints it in hh:mm:ss format
    tot_time = end_time - start_time
    print("\n** Total Elapsed Runtime:", int(tot_time // 3600), ":",
        int((tot_time % 3600) // 60), ":", int((tot_time % 3600) % 60))


# TODO: 2.-to-7. Define all the function below. Notice that the input
# parameters and return values have been left in the function's docstrings.
# This is to provide guidance for achieving a solution similar to the
# instructor provided solution. Feel free to ignore this guidance as long as
# you are able to achieve the desired outcomes with this lab.

def get_input_args():
    """
    Retrieves and parses the command line arguments created and defined using
    the argparse module. This function returns these arguments as an
    ArgumentParser object.
     3 command line arguments are created:
       dir - Path to the pet image files(default- 'pet_images/')
       arch - CNN model architecture to use for image classification(default-
              pick any of the following vgg, alexnet, resnet)
       dogfile - Text file that contains all labels associated to dogs(default-
                'dognames.txt'
    Parameters:
     None - simply using argparse module to create & store command line arguments
    Returns:
     parse_args() -data structure that stores the command line arguments object
    """
        # line arguments
    parser = argparse.ArgumentParser(description='AI classifier input programme')
    parser.add_argument('--dir', default='pet_images/', help='path to the folder')
    parser.add_argument('--arch', default='resnet', help='classifier type')
    parser.add_argument('--dogfile', default='dognames.txt', help='text storing dognames')
    return parser.parse_args()


def get_pet_labels(image_dir):
    """
    Creates a dictionary of pet labels based upon the filenames of the image
    files. Reads in pet filenames and extracts the pet image labels from the
    filenames and returns these labels as petlabel_dic. This is used to check
    the accuracy of the image classifier model.
    Parameters:
     image_dir - The (full) path to the folder of images that are to be
                 classified by pretrained CNN models (string)
    Returns:
     petlabels_dic - Dictionary storing image filename (as key) and Pet Image
                     Labels (as value)
    """
    filename = listdir(image_dir)
    petname = []

    for item in filename:
        temp_list = item.lower().split('_')
        temp_word = ''
        for word in temp_list:
            if word.isalpha():
                temp_word += word + ' '
        petname.append(temp_word.strip())

    petlabels_dic = dict(zip(filename, petname))

    return petlabels_dic


def classify_images(images_dir, petlabel_dic, model):
    """
    Creates classifier labels with classifier function, compares labels, and
    creates a dictionary containing both labels and comparison of them to be
    returned.
     PLEASE NOTE: This function uses the classifier() function defined in
     classifier.py within this function. The proper use of this function is
     in test_classifier.py Please refer to this program prior to using the
     classifier() function to classify images in this function.
     Parameters:
      images_dir - The (full) path to the folder of images that are to be
                   classified by pretrained CNN models (string)
      petlabel_dic - Dictionary that contains the pet image(true) labels
                     that classify what's in the image, where its key is the
                     pet image filename & its value is pet image label where
                     label is lowercase with space between each word in label
      model - pretrained CNN whose architecture is indicated by this parameter,
              values must be: resnet alexnet vgg (string)
     Returns:
      results_dic - Dictionary with key as image filename and value as a List
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)   where 1 = match between pet image and
                    classifer labels and 0 = no match between labels
    """
    results_dic = dict()
    for pic_name, pic_item in petlabel_dic.items():
        res_list = []
        res_list.insert(0, pic_item)
        classifier_item = classifier(images_dir+pic_name, model).lower().strip()
        res_list.insert(1, classifier_item)
        judge = 0
        if classifier_item.find(pic_item) >= 0:
            items = [item.strip() for item in list(classifier_item.split(','))]
            for word in items:
                if (word.find(pic_item) == 0 or word[word.find(pic_item)-1] == ' ')\
                and (word.find(pic_item)+len(pic_item) == len(word) or word[word.find(pic_item)+len(pic_item)] == ' '):
                        judge = 1
                        break
        res_list.insert(2, judge)
        results_dic[pic_name] = res_list
    return results_dic


def adjust_results4_isadog(result_dic, dogsfile):
    """
    Adjusts the results dictionary to determine if classifier correctly
    classified images 'as a dog' or 'not a dog' especially when not a match.
    Demonstrates if model architecture correctly classifies dog images even if
    it gets dog breed wrong (not a match).
    Parameters:
      results_dic - Dictionary with key as image filename and value as a List
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and
                            classifer labels and 0 = no match between labels
                    --- where idx 3 & idx 4 are added by this function ---
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and
                            0 = pet Image 'is-NOT-a' dog.
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image
                            'as-a' dog and 0 = Classifier classifies image
                            'as-NOT-a' dog.
     dogsfile - A text file that contains names of all dogs from ImageNet
                1000 labels (used by classifier model) and dog names from
                the pet image files. This file has one dog name per line.
                Dog names are all in lowercase with spaces separating the
                distinct words of the dogname. This file should have been
                passed in as a command line argument. (string - indicates
                text file's name)
    Returns:
           None - results_dic is mutable data type so no return needed.

    with open(dogsfile, 'r') as f:
        names = f.readlines()
        names = [name.rstrip() for name in names]
        """
    names = dict()
    with open(dogsfile, 'r') as f:
        name = f.readline()
        while name:
            name = name.rstrip()
            if name not in names:
                names[name] = 1
            else:
                print("# WARNING: This name has already in the list!")
            name = f.readline()

    for item in result_dic:
        if result_dic[item][0] in names:
            result_dic[item].insert(3, 1)
        else:
            result_dic[item].insert(3, 0)
        if result_dic[item][1] in names:
            result_dic[item].insert(4, 1)
        else:
            result_dic[item].insert(4, 0)



def calculates_results_stats(results_dic):
    """
    Calculates statistics of the results of the run using classifier's model
    architecture on classifying images. Then puts the results statistics in a
    dictionary (results_stats) so that it's returned for printing as to help
    the user to determine the 'best' model for classifying images. Note that
    the statistics calculated as the results are either percentages or counts.
    Parameters:
      results_dic - Dictionary with key as image filename and value as a List
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and
                            classifer labels and 0 = no match between labels
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and
                            0 = pet Image 'is-NOT-a' dog.
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image
                            'as-a' dog and 0 = Classifier classifies image
                            'as-NOT-a' dog.
    Returns:
     results_stats - Dictionary that contains the results statistics (either a
                     percentage or a count) where the key is the statistic's
                     name (starting with 'pct' for percentage or 'n' for count)
                     and the value is the statistic's value
    """
    Z = len(results_dic)
    A = B = C = D = E = Y = 0
    for key in results_dic:
        if results_dic[key][3] + results_dic[key][4] == 2:
            A += 1
        if results_dic[key][3] == 1:
            B += 1
            if results_dic[key][2] == 1:
                E += 1
        if results_dic[key][3] + results_dic[key][4] == 0:
            C += 1
        if results_dic[key][3] == 0:
            D += 1
        if results_dic[key][2] == 1:
            Y += 1
    results_stats = dict()
    results_stats['pec_correct_dog'] = A/B * 100
    results_stats['pec_correct_nondog'] = C/D * 100
    results_stats['pec_correct_breed'] = E/B * 100
    results_stats['pec_label_match'] = Y/Z * 100

    return results_stats


def print_results():
    """
    Prints summary results on the classification and then prints incorrectly
    classified dogs and incorrectly classified dog breeds if user indicates
    they want those printouts (use non-default values)
    Parameters:
      results_dic - Dictionary with key as image filename and value as a List
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and
                            classifer labels and 0 = no match between labels
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and
                            0 = pet Image 'is-NOT-a' dog.
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image
                            'as-a' dog and 0 = Classifier classifies image
                            'as-NOT-a' dog.
      results_stats - Dictionary that contains the results statistics (either a
                     percentage or a count) where the key is the statistic's
                     name (starting with 'pct' for percentage or 'n' for count)
                     and the value is the statistic's value
      model - pretrained CNN whose architecture is indicated by this parameter,
              values must be: resnet alexnet vgg (string)
      print_incorrect_dogs - True prints incorrectly classified dog images and
                             False doesn't print anything(default) (bool)
      print_incorrect_breed - True prints incorrectly classified dog breeds and
                              False doesn't print anything(default) (bool)
    Returns:
           None - simply printing results.
    """
    pass



# Call to main function to run the program
if __name__ == "__main__":
    main()
