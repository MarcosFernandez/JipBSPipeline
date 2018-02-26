#!/usr/bin/env python

import os
import re
import sys
import json
import argparse
import subprocess

#########0. DEFINE SERVER #############
HTTP_SERVER = "172.16.10.22"


#########1. PROGRAM ARGUMENTS #############

#1.1 Create object for argument parsinng
parser = argparse.ArgumentParser(prog="createBisulfitePipelineConfig",description="Create Bisulfite json configuration from Lims CNAG database.")     

#1.2 Definition of input parameters
input_group = parser.add_argument_group('Inputs')
input_group.add_argument('-s','--subproject', dest="subproject", metavar="SUBPROJECT",help='Lims CNAG subproject name.')
input_group.add_argument('-b','--barcodes', dest="barcode_list",nargs='*',metavar="BARCODE_LIST",help='List of sample barcodes to retrieve from a SUBPROJECT',required=False)


output_group = parser.add_argument_group('Output')
output_group.add_argument('-j','--json-config', dest="json_config", metavar="FILE", help='JSON Output configuration file.')


#1.3 Argument parsing
args = parser.parse_args()

#1.4 Argumet checking
if not args.subproject:
    print "Sorry!! No CNAG Lims subproject name. Specify it using -s argument."
    sys.exit()

if not args.json_config:
    print "Sorry!! No JSON configuration file found. Specify it using -j argument."
    sys.exit()


#########3. GET JSON FILE FROM LIMS #####
get_command = "http://%s/lims/api/seq/lims_query/?format=xls&limit=0&loadedwith__library__subprojects__subproject_name=%s" %(HTTP_SERVER,args.subproject)
json_wget = "%s.tmp" %(args.json_config)

command = ["wget","-q","-O",json_wget,"-",get_command]

process = subprocess.Popen(command)
    
process.wait() 

#########4. FILTERED JSON BY SAMPLE #####
if args.barcode_list:
    filteredSampleDirectory = {}
    filteredSampleDirectory["objects"] = []
    with open(json_wget) as jsonFile:
        sampleDirectory = json.load(jsonFile)
        vectorElements = sampleDirectory["objects"]
        for element in vectorElements:
            if element["sample_barcode"] in args.barcode_list:                
                filteredSampleDirectory["objects"].append(element)
                
    with open(json_wget, 'w') as of:
        json.dump(filteredSampleDirectory, of, indent=2)


#########5. FILTER LIMS JSON FILE #####
gemBS_command = ['gemBS','prepare-config','-l',json_wget,'-j', args.json_config]

process_gemBS = subprocess.Popen(gemBS_command)
    
if process_gemBS.wait() != 0:
    raise ValueError("Error while running %s"%(' '.join(gemBS_command)))

os.remove(json_wget)




