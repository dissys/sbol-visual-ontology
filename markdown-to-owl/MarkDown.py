'''
Created on 29 Mar 2019

@author: gokselmisirli
'''

class MarkDown (object):
    PREFIX_TITLE="# "
    PREFIX_TERMS="## Associated"
    PREFIX_RECOMMENDED="## Recommended"
    PREFIX_EXAMPLE="## Prototypical"
    PREFIX_NOTES="## Notes"
    
    def parseMdFile(self):
        print ("Parsing " + self.filePath)
        blockData=""
        with open(self.filePath) as f: 
            for line in f: 
                #print(line)
                if line.startswith(MarkDown.PREFIX_TITLE):
                    self._title=line[len(MarkDown.PREFIX_TITLE):].rstrip()
                    blockData=""
                elif line.startswith(MarkDown.PREFIX_TERMS):
                    blockData=""
                elif line.startswith(MarkDown.PREFIX_RECOMMENDED):
                    self._terms=blockData
                    blockData=""    
                elif line.startswith(MarkDown.PREFIX_EXAMPLE):
                    self._glyphs=blockData
                    blockData=""
                elif line.startswith(MarkDown.PREFIX_NOTES):
                    self._example=blockData
                    blockData=""
                else: 
                    blockData= blockData + line#.rstrip()                    
                
                self._notes=blockData    
                                  
    def __init__(self, mainFolder, filePath):
        self.mainFolder = mainFolder
        self.filePath = filePath
        #self._title=""
        #self.fin = open(filePath, 'r')
        #self.parseMdFile
        
    def __iter__(self):
        return self
        
    def next(self):
        line = self.fin.readline()
        return line 
    
    def getTitle(self):
        return self._title
      
    @property
    def title(self):
        return self._title  
    
    @property
    def terms(self):
        return self._terms  
    
    @property
    def glyphs(self):
        return self._glyphs  
    
    @property
    def example(self):
        return self._example  
    
    @property
    def notes(self):
        return self._notes   