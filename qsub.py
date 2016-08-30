#!/usr/bin/python
# Example PBS cluster job submission in Python

from popen2 import popen2
import time

# If you want to be emailed by the system, include these in job_string:
# PBS -M your_email@address
# PBS -m abe  # (a = abort, b = begin, e = end)

# Loop over your jobs
import os.path
import fnmatch
import argparse
import re
import os
import random

def getFiles(directory, extension):
    """
    Gets a list of bngl files that could be correctly translated in a given 'directory'

    Keyword arguments:
    directory -- The directory we will recurseviley get files from
    extension -- A file extension filter
    """
    matches = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, '*.{0}'.format(extension)):
            filepath = os.path.abspath(os.path.join(root, filename))
            matches.append(
                [filepath, os.path.getsize(os.path.join(root, filename))])

    # sort by size
    #matches.sort(key=lambda filename: filename[1], reverse=False)

    matches = [x[0] for x in matches]

    return matches

queue_list = {'noc_64_core': 64, 'serial_queue': 1, 'dept_24_core':
              24, 'dmz_core36': 36, 'bahar_64_core': 64, 'bahar_12_core': 12}
import progressbar
import tempfile
import yaml


def start_queue(test, queue, batchSize, repetitions):
    """
    sends a batch job with the qsub queue and executes a command over it.
    using PBS commands

    Keyword arguments:
    test -- the folder with mdl files
    queue -- The queue we will send the job to. It has to make reference to an entry in queue_list
    batchsize -- The total number of jobs per batch job. (in other words, the number of nodes we will be using is <fileNameSet>/<batchSize>. Typically you want this to be a multiple of the number of cores per node.)
    """
    progress = progressbar.ProgressBar()
    for idx in progress(range(0,repetitions)):

        # Open a pipe to the qsub command.
        output, input = popen2('qsub')

        # Customize your options here
        job_name = "jjtv_{0}".format(idx)
        walltime = "10:00:00"
        currentdirectory = os.getcwd()
        processors = "nodes={1}:ppn={0}".format(
            batchSize, nodes)

        job_string = """#!/bin/bash
        #PBS -N %s
        #PBS -l walltime=%s
        #PBS -l %s
        #$ -cwd
        #PBS -q %s

        echo Running on `hostname`
        echo workdir $PBS_O_WORKDIR

        ##PBS -M jjtapia@gmail.com
        ##PBS -m abe  # (a = abort, b = begin, e = end)
        PYTHONPATH=$PYTHONPATH:./:./SBMLparser
        PATH=/usr/local/anaconda/bin:$PATH
        SCRDIR=/scr/%s/$PBS_JOBID

        #if the scratch drive doesn't exist (it shouldn't) make it.
        if [[ ! -e $SCRDIR ]]; then
                mkdir $SCRDIR
        fi

        cd $PBS_O_WORKDIR
        echo scratch drive ${SCRDIR}


        python analyzeModelSet.py -t MCellRuns/%s/mcell -r %s -w ${SCRDIR}
       
        """ % (job_name, walltime, processors, queue, test, test, batchsize)

        # Send job_string to qsub
        input.write(job_string)
        input.close()

        # Print your job and the system response to the screen as it's submitted
        # print(output.read())

        time.sleep(0.05)


def restart(targetset, comparisonset, targetExtension):
    """
    This function is used to restart from a previouly incomplete run
    """
    targetFolder = '/'.join(targetset[0].split('/')[:-1]) + '/'

    existingset = [
        targetFolder + '.'.join(x.split('/')[-1].split('.')[:-1]) + targetExtension for x in comparisonset]
    filenameset = [x for x in targetset if x not in existingset]
    return filenameset


def defineConsole():
    parser = argparse.ArgumentParser(description='Devin-Jose modeling pipeline')
    parser.add_argument('-q', '--queue', type=str, help='queue to run in')
    parser.add_argument('-b', '--batch', type=int, help='batch size')
    parser.add_argument('-t', '--test', type=str)
    parser.add_argument('-r', '--repetitions', type=int)
    return parser


if __name__ == "__main__":
    parser = defineConsole()
    namespace = parser.parse_args()
    test = namespace.test
    queue = namespace.queue
    batchsize = namespace.batch
    repetitions = namespace.repetitions

    # print len(finalfiles)

    start_queue(test, queue, batchsize, repetitions)
    