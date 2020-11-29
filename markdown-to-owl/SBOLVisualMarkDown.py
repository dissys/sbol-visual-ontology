'''
Created on 5 Apr 2019

@author: gokselmisirli
'''
import re
import os
class SBOLVisualMarkDown (object):
    
    GLYPH_START="!["  
    GLYPH_TEMPLATE="![glyph specification]({})"  
    def __init__(self, mdContent):
        self._mdContent = mdContent
        
    def getGlyphLabel(self):
        termName=self._mdContent.title.replace(" ","").replace("/","") + "Glyph"  
        return termName
    
    def getGlyphTypesORG_Del(self):
        glyphTypesTemp=self._mdContent.terms.rstrip().split("\n")
        glyphTypes=[]
        
        for glyphType in glyphTypesTemp:
            if glyphType.strip():
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
                    print ("---No Ontology term specified!")   
        return allTerms   
    
    def getGlyphTypesFromString(self,glyphTypeContent):
        glyphTypesTemp=glyphTypeContent.rstrip().split("\n")
        glyphTypes=[]
        
        for glyphType in glyphTypesTemp:
            if glyphType.strip():
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
                    print ("---No Ontology term specified!")   
        return allTerms   
    
    ''' Associated SBO term(s)
    SBO:0000169 Inhibition
    Head: SBO:0000642 Inhibited 
    Tail: SBO:0000020 Inhibitor
    '''
    def getGlyphTypes(self):
        text=self._mdContent.terms.rstrip()
        #If Head information is included, terms are until Head.
        index=text.find("Head:")
        if index==-1:
            index=text.find("Incoming:")
        
        if index>-1:
            text=text[0:index]
        return self.getGlyphTypesFromString(text) 
    
    def getTextBetween(self, text, startString,endString):
        text=text.rstrip()
        indexHead=text.find(startString)
        indexTail=text.find(endString)
        #If Head information is included terms are until Head.
        if indexHead>0:
            if indexTail>0:
                text=text[indexHead:indexTail]
            else:    
                text=text[indexHead:]
            text=text.rstrip()
            return text
        else:
            return None
    
    def getTextAfter(self, text, startString):
        text=text.rstrip()
        indexTail=text.find(startString)
        #If Head information is included terms are until Head.
        if indexTail>0:
            text=text[indexTail:]
            text=text.rstrip()
            return text  
        else:
            return None
         
    def getIncomingTypes(self):
        text=self.getTextBetween(self._mdContent.terms, "Incoming:", "Outgoing:")
        if text:
            return self.getGlyphTypesFromString(text)  
        else:
            return None
        
    def getOutgoingTypes(self):
        text=self.getTextAfter(self._mdContent.terms, "Outgoing:")
        if text:
            return self.getGlyphTypesFromString(text)  
        else:
            return None
           
    def getHeadTypes(self):
        text=self.getTextBetween(self._mdContent.terms, "Head:", "Tail:")
        if text:
            return self.getGlyphTypesFromString(text)  
        else:
            return None
        
    def getTailTypes(self):
        text=self.getTextAfter(self._mdContent.terms, "Tail:")
        if text:
            return self.getGlyphTypesFromString(text)  
        else:
            return None
        
  
    def getCommentFromText(self,text):
        index=text.find(self.GLYPH_START)
        comment=text[0:index-1].rstrip()
        return comment 
    
    def getGlyphText(self):
        return self._mdContent.glyphs.strip()
      
    def getComment(self):
        text=self._mdContent.glyphs
        return self.getCommentFromText(text)  
     
    def getGlyphs(self):
        text=self._mdContent.glyphs
        images=[]
        items=re.findall('!\[(.*?)\]\((.*?)\)',text)
        for item in items:
            if item[0].find("glyph specification")>-1:
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
    
    def getDirectory(self):   
        filePath=self._mdContent.filePath # ../SBOL-visual/Glyphs/Interactions/inhibition/README.md
        dir = os.path.dirname(filePath) # ../SBOL-visual/Glyphs/Interactions/inhibition
        index=dir.index(os.path.sep,len("../")) 
        dir=dir[index+1:] #Glyphs/Interactions/inhibition
        #dir="https://github.com/SynBioDex/SBOL-visual/blob/master/" + dir
        return dir

    def getCommentAfterImage(self,image):
        text=self._mdContent.glyphs
        index=text.find(image)
        index=index + len(image) + 1 #+1 for the ending paranthesis
        comment=text[index+1:].rstrip()
        comment=self.getCommentFromText(comment)
        return comment.lstrip().rstrip()