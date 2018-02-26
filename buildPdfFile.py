#!/usr/bin/env python

import os
import re
import sys
import argparse
import subprocess
import fnmatch
import glob

#########0. FIND PDF FILE #############

def finder(pathSearch, extension):
    """ Find all files recursevely according to a given extension """
    ret = []
    for dirpath, dirnames, files in os.walk(pathSearch):
        for f in fnmatch.filter(files, extension):
            ret.append("%s/%s"%(dirpath,f))
    return ret  



#########1. PROGRAM ARGUMENTS #############

#1.1 Create object for argument parsinng
parser = argparse.ArgumentParser(prog="buildPdfFile.py",description="Build PDF file. Transforms sphinx code, to latex to create pdf file.")  

input_group = parser.add_argument_group('Inputs')
input_group.add_argument('-s','--sphinx', dest="SPHINX_DIR", metavar="SPHINX_DIR",help='Sphinx directory.', required=True)

#1.3 Argument parsing
args = parser.parse_args()

#########2. RUN LATEXPDF FILE #####
command = ["make","-C","%s" %(args.SPHINX_DIR),"latexpdf"]

process = subprocess.Popen(command)
    
process.wait() 

#########3. SHOW PDF FILE #####

pdfFiles = finder('%s/build/latex/' %args.SPHINX_DIR, '*pdf') 

for pdfFile in pdfFiles:
    print "PDF File generated: [%s]" %(pdfFile) 
