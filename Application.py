'''
Created on 29 Mar 2019

@author: gokselmisirli
'''
import types
from MarkDown import  *
from Ontology import  *

import os

sbolVisualDir= "../SBOL-visual/Glyphs"

def parseFile(filePath):
    dir=os.path.dirname(filePath)
    md=MarkDown(sbolVisualDir,filePath) 
    md.parseMdFile() 
    addOntologyTerms(md)

def parseFiles(directory):
    files=os.listdir(directory)
   
    for file in files :
        filePath=directory + "/" + file
        if os.path.isdir(filePath):
            #print ("dir:" + filePath)
            parseFiles(filePath)
        elif file=="README.md":
            parseFile(filePath)
                       
parseFiles(sbolVisualDir)
saveOntology()
print ("done!")