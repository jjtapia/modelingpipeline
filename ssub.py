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


def start_queue(test, batchSize, repetitions):

    project = 'bi4s88p'
    job_string = """#!/bin/csh
#!/bin/csh
#SBATCH -N 1
#SBATCH -p RM
#SBATCH -t 48:00:00
#SBATCH --array=1-{0}
#SBATCH --job-name={1}

#SBATCH --mail-type=ALL
#SBATCH --mail-user=jjtapia@gmail.com

set echo

cd /pylon2/{3}/tapiava/workspace/modelingpipeline
python analyzeModelSet.py -t MCellRuns/{1}/mcell -r {2} -w /pylon1/{3}/tapiava
#python mergeDataFrame.py -w /pylon1/{3}/tapiava/{1}/partial -o {1}.h5
    
    """.format(batchSize, test, repetitions,project)

    with open('pybatch.sub', 'w') as f:
        f.write(job_string)


    subprocess.call(['sbatch','pybatch.sub'])




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
    