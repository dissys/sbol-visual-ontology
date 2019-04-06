'''
Created on 5 Apr 2019

@author: gokselmisirli
'''
import re
from ontology_backup2 import GLYPH_START
class SBOLVisualMD (object):
    
    GLYPH_START="!["  
    GLYPH_TEMPLATE="![glyph specification]({})"  
    def __init__(self, mdContent):
        self._mdContent = mdContent
        
    def getGlyphLabel(self):
        termName=self._mdContent.title.replace(" ","").replace("/","") + "Glyph"  
        return termName
    
    def getGlyphTypes(self):
        glyphTypesTemp=self._mdContent.terms.rstrip().split("\n");
        glyphTypes=[]
        
        for glyphType in glyphTypesTemp:
            if glyphType:
                glyphTypes.append(glyphType)
        allTerms=[]         
        for line in glyphTypes:
            if len(line)>0:
                #print ("line:" +  line)
                items=re.findall('[A-Z]+:[0-9]+', line)
                if not items:
                    #html url regex: http://www.noah.org/wiki/RegEx_Python
                    items=re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
                    
                if items: 
                    allTerms.append(items)
                else:
                    items=[]
                    allTerms.append(items)
                    print ("---No ontology term specified!")   
        return allTerms          
     
    def getCommentFromText(self,text):
        index=text.find(self.GLYPH_START)
        comment=text[0:index-1].rstrip()
        return comment 
    
    def getComment(self):
        text=self._mdContent.glyphs
        return self.getCommentFromText(text)  
    
          
    
    def getGlyphs(self):
        text=self._mdContent.glyphs
        images=[]
        items=re.findall('!\[(.*?)\]\((.*?)\)',text)
        for item in items:
            images.append(item[1])
        return images  
    
    def removeLineBreaks(self,text):
        return text.replace("\n","").replace("\r","")
        
    def getGlyphBlocks(self):
        blocks=[]
        text=self.removeLineBreaks(self._mdContent.glyphs)
        images=self.getGlyphs()
        
        if images:
            subBlock=[]
            i=0
            subBlock.append(images[0])
            while i<len(images)-1:    
                image1Text=self.GLYPH_TEMPLATE.format(images[i])
                image2Text=self.GLYPH_TEMPLATE.format(images[i+1])
                
                index1=text.find(image1Text)
                index2=text.find(image2Text)
                
                textBetweenImages=text[index1+len(image1Text):index2].replace(" ","")
                if not textBetweenImages:
                    subBlock.append(images[i+1])
                else:
                    blocks.append(subBlock)
                    subBlock=[]
                    subBlock.append(images[i+1])
                     
                i=i+1
            
            #Assign the last block after the loop ends as an item in the blocks or if the while loop does not run at all  
            blocks.append(subBlock)
            
        return blocks
                    
                   
            
            
            
            
            
            
    def getExample(self):
        return self._mdContent.example.strip()
     
    def getNotes(self):   
        return self._mdContent.notes.strip()

    def getCommentAfterImage(self,image):
        text=self._mdContent.glyphs
        index=text.find(image)
        index=index + len(image) + 1 #+1 for the ending paranthesis
        comment=text[index+1:].rstrip()
        comment=self.getCommentFromText(comment)
        return comment.lstrip().rstrip()