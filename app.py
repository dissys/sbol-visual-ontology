'''
Created on 29 Mar 2019

@author: gokselmisirli
'''
import types
from mdFile import  *
from ontology import  *

import os

sbolVisualDir= "../SBOL-visual/Glyphs"


def parseFile(filePath):
    #print("fileDir:" + filePath)
    dir=os.path.dirname(filePath)
    if dir.endswith("location"):      
        #if dir.endswith("stability-element"):      
        md=mdContent(sbolVisualDir,filePath) 
        md.parseMdFile() 
        addOntologyTerms(md)
    '''
    print(md.title)
    print(md.terms)
    print(md.glyphs)
    print(md.example)
    print ("done!")
    print ("----------------------------------------------------")
    '''
    #saveOntology()

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


