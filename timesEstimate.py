#!/usr/bin/env python

import os
import re
import sys
import json
import argparse
import subprocess
import fnmatch
import time

#############0. METHODS ###################

def finder(pathSearch, extension):
    """ Find all files recursevely according to a given extension """
    ret = []
    for dirpath, dirnames, files in os.walk(pathSearch):
        for f in files:
            if f.endswith(extension):
                ret.append("%s/%s"%(dirpath,f))
    return ret


#########1. PROGRAM ARGUMENTS #############

#1.1 Create object for argument parsinng
parser = argparse.ArgumentParser(prog="timesEstimate.py",description="Makes an estimation of the maximum time to be configured per each pipeline job step.")  

input_group = parser.add_argument_group('Inputs')
input_group.add_argument('-t','--threads', dest="threads", type=int,metavar="THREADS",help='Threads to be used in the pipeline.', required=True)
input_group.add_argument('-f', '--fastq-dir', dest="fastq_dir", metavar="PATH", help='Directory where is located gzipped fastq input data.', required=True)
input_group.add_argument('-e', '--ext', dest="ext", metavar="EXT", help='File compression extension. For instance gz', required=True)

output_group = parser.add_argument_group('Output')
output_group.add_argument('-j','--json-config', dest="json_config", metavar="FILE", help='JSON Output configuration file.')

#1.3 Argument parsing
args = parser.parse_args()

###############2. CONSTANTS ###############
SECS_BYTE = 0.00000015 #Estimated maximum mapping time per byte

#########3. MAXIMUM FILE SIZE #############

list_file_sizes = []
listFastqFiles = finder(args.fastq_dir,args.ext )

for fileFastq in listFastqFiles:
    statInfo = os.stat(fileFastq)
    list_file_sizes.append(statInfo.st_size)

list_file_sizes = sorted(list_file_sizes, reverse=True)


#3.1.List files
if len(list_file_sizes) < 1:
    print "Sorry!! Not enough fastq files in path %s with extension %s." %(args.fastq_dir,args.ext)
    sys.exit()

max_bytes_file_one = list_file_sizes[0]
max_bytes_file_two = list_file_sizes[1]

#########4. ESTIMATING TIMES #############

max_mapping_time_secs = (float((24/args.threads))*SECS_BYTE) * (max_bytes_file_one + max_bytes_file_two)
max_merging_time_secs = 1.5 * max_mapping_time_secs
max_call_snps_time_secs = 1.2 * max_mapping_time_secs
max_concatenation_calls_time_secs = 7200
max_filter_calls_time_secs = 7200

max_mapping_time = time.strftime("%H:%M:%S", time.gmtime(max_mapping_time_secs))
max_merging_time = time.strftime("%H:%M:%S", time.gmtime(max_merging_time_secs))
max_call_snps_time = time.strftime("%H:%M:%S", time.gmtime(max_call_snps_time_secs))
max_concatenation_calls_time = time.strftime("%H:%M:%S", time.gmtime(max_concatenation_calls_time_secs))
max_filter_calls_time = time.strftime("%H:%M:%S", time.gmtime(max_filter_calls_time_secs))

#########5. SCRIPT OUTPUTS #############

timePredictions = {}
timePredictions["max_mapping_time"] = max_mapping_time
timePredictions["max_merging_time"] = max_merging_time
timePredictions["max_call_snps_time"] = max_call_snps_time
timePredictions["max_concatenation_calls_time"] = max_concatenation_calls_time
timePredictions["max_filter_calls_time"] = max_filter_calls_time

#5.1 Save JSON file
with open(args.json_config, 'w') as of:
    json.dump(timePredictions, of, indent=2)

#5.2 Stdout output
print "max_mapping_time: \t %s" %(max_mapping_time)
print "max_merging_time: \t %s" %(max_merging_time)
print "max_call_snps_time: \t %s" %(max_call_snps_time)
print "max_concatenation_calls_time: \t %s" %(max_concatenation_calls_time)
print "max_filter_calls_time: \t %s" %(max_filter_calls_time)





