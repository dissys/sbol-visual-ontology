'''
Created on 29 Mar 2019

@author: gokselmisirli
'''
#https://buildmedia.readthedocs.org/media/pdf/owlready2/latest/owlready2.pdf
from owlready2 import *
from ontology import *

import types
import re
from pip._vendor.webencodings import labels
from rdf import TypeChecker

print ("hello4")

onto = get_ontology("http://sbolstandard.org/visual#")
sbol = get_ontology("https://dissys.github.io/sbol-owl/sbol.rdf")
sbol2 = get_ontology("http://sbolstandard.org/v2")
so = get_ontology("http://identifiers.org/so/")
biopax = get_ontology("http://www.biopax.org/release/biopax-level3.owl")

img = get_ontology("https://github.com/SynBioDex/SBOL-visual/blob/master/Glyphs/")


onto.imported_ontologies.append(sbol)
GLYPH_START="!["

SBO_BASE_IRI="http://biomodels.net/SBO/"
SBO_INTERACTION_PARENT_TERM=SBO_BASE_IRI + "SBO_0000231"
sboTypeChecker=TypeChecker("sbo.owl")
        
     
class ComponentDefinition (Thing):
    namespace=sbol2

class ImageFile (Thing):
    namespace=img 
 
    
class SO_0000110 (Thing):
    namespace=so  

'''      
class SO_0000167 (Thing):
    namespace=so
'''
    
class BioPAXPhysicalEntity(Thing):
    namespace=biopax


class type(ObjectProperty):
    namespace=sbol2
    
class role(ObjectProperty):
    namespace=sbol2



 
class Glyph(Thing):
    namespace=onto

class isGlyphOf(ObjectProperty):
    range:Glyph
    namespace=onto

class hasGlyph(ObjectProperty):
    domain:Glyph
   # range: [uri]
    namespace=onto
    
class prototypicalExample(AnnotationProperty):
    domain:Glyph
    range: [str]
    namespace=onto
    
class notes(AnnotationProperty):
    domain:Glyph
    range: [str]
    namespace=onto    
    
    
'''
class InsulatorGlyph(Glyph):
    equivalent_to = [
        onto.Glyph & ( onto.isGlyphOf.some(sbol2.ComponentDefinition & (sbol2.role.some(so.SO_0000167))))
            ] 

InsulatorGlyph2 = types.new_class("InsulatorGlyph2", (onto.Glyph,))
InsulatorGlyph2.namespace=onto
   
InsulatorGlyph2.equivalent_to = [
        onto.Glyph & ( onto.isGlyphOf.some(sbol2.ComponentDefinition & (sbol2.role.some(so.SO_0000167))))
            ] 
 '''

def getComment(text):
    index=text.find(GLYPH_START)
    comment=text[0:index-1].rstrip()
    return comment

def getGlyps(text):
    images=[]
    items=re.findall('!\[(.*?)\]\((.*?)\)',text)
    for item in items:
        images.append(item[1])
    return images  

def getCommentAfterImage(text, image):
    index=text.find(image)
    index=index + len(image) + 1 #+1 for the ending paranthesis
    comment=text[index+1:].rstrip()
    comment=getComment(comment)
    return comment.lstrip().rstrip()
    
def addOntologyTerms(mdContent):
    termName=mdContent.title.replace(" ","").replace("/","") + "Glyph"   
    sbolVisualTerm = types.new_class(termName, (onto.Glyph,))
    sbolVisualTerm.namespace=onto
    sbolVisualTerm.label=mdContent.title
    lineIndex=1
    glyphTypesTemp=mdContent.terms.rstrip().split("\n");
    glyphTypes=[]
    
    for glyphType in glyphTypesTemp:
        if glyphType:
            glyphTypes.append(glyphType)
    
    for line in glyphTypes:
        if len(line)>0:
            print ("line:" +  line)
            if lineIndex==1:
                terms=[]
                items=re.findall('[A-Z]+:[0-9]+', line)
                if not items:
                    #html url regex: http://www.noah.org/wiki/RegEx_Python
                    items=re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
                    
                if not items: 
                    print ("gmgmgm")   
                for term in items:
                    print ("Regex label:" + term)
                    if term.startswith("SO"):
                        termClass = types.new_class(term, (so.SO_0000110,))
                        termClass.namespace=so
                        terms.append(termClass)
                        if len(terms)==1:
                            sbolVisualTerm.equivalent_to = [onto.Glyph & ( onto.isGlyphOf.some(sbol2.ComponentDefinition & (sbol2.role.some(terms[0]))))] 
                        elif len(terms)>1:  
                            sbolVisualTerm.equivalent_to = [onto.Glyph & ( onto.isGlyphOf.only(sbol2.ComponentDefinition & (sbol2.role.some(Or(terms)))))] 
            
                    elif term.startswith(biopax.base_iri):
                        term=term.replace(biopax.base_iri,"")
                        term=term.replace("#","")
                        termClass = types.new_class(term, (biopax.BioPAXPhysicalEntity,))
                        termClass.namespace=biopax
                        terms.append(termClass) 
                        
                        if len(terms)==1:
                            sbolVisualTerm.equivalent_to = [onto.Glyph & ( onto.isGlyphOf.some(sbol2.ComponentDefinition & (sbol2.type.some(terms[0]))))] 
                        elif len(terms)>1:  
                            sbolVisualTerm.equivalent_to = [onto.Glyph & ( onto.isGlyphOf.only(sbol2.ComponentDefinition & (sbol2.type.some(Or(terms)))))] 
                     
                    elif term.startswith("SBO"):
                        sboUri=SBO_BASE_IRI + term.replace(":","_")
                        if sboTypeChecker.hasParent(sboUri, SBO_INTERACTION_PARENT_TERM): 
                            print ("SBO:Interaction----------------")
                        else:     
                            print ("SBO:Not_Interaction----------------")
                
                
                sbolVisualTerm.comment=getComment(mdContent.glyphs)   
                images=getGlyps(mdContent.glyphs)
                
                if len(glyphTypes)==1 and len(images)==1:
                    imgClass = types.new_class(images[0], (img.ImageFile,))
                    imgClass.namespace=img                
                    sbolVisualTerm.hasGlyph=imgClass
                elif len(glyphTypes)==1 and len(images)==2:
                    imgClass = types.new_class(images[0], (img.ImageFile,))
                    imgClass.namespace=img                
                    sbolVisualTerm.hasGlyph=imgClass
                    alternateTermName=termName + "Alternative"   
                    sbolVisualAlternateTerm = types.new_class(alternateTermName, (sbolVisualTerm,))
                    sbolVisualAlternateTerm.namespace=onto
                    sbolVisualAlternateTerm.label=mdContent.title
                    sbolVisualAlternateTerm.comment=getCommentAfterImage(mdContent.glyphs,images[0])  
                    imgClass = types.new_class(images[1], (img.ImageFile,))
                    imgClass.namespace=img                
                    sbolVisualAlternateTerm.hasGlyph=imgClass
                    
                sbolVisualTerm.prototypicalExample=mdContent.example.strip()
                sbolVisualTerm.notes=mdContent.notes.strip()
                    
                    
                
                
                
                 
                    
            '''    
            term=line.split(" ")[0]
            term=term[0:-1]
            term=term.replace(":","_")
            print ("Term:" + term)       
            '''
                    
        '''
            if len(terms)==1:
                sbolVisualTerm.equivalent_to = [
                onto.Glyph & ( onto.isGlyphOf.some(sbol2.ComponentDefinition & (sbol2.role.some(terms[0]))))
                    ] 
            elif len(terms)>1:  
                sbolVisualTerm.equivalent_to = [
                onto.Glyph & ( onto.isGlyphOf.only(sbol2.ComponentDefinition & (sbol2.role.some(Or(terms)))))]  
        '''
    
    #sbolVisualTerm.comment=   
         
        '''soClass = types.new_class(term, (so.SO_0000110,))
        soClass.namespace=so
        sbolVisualTerm.equivalent_to = [
        onto.Glyph & ( onto.isGlyphOf.some(sbol2.ComponentDefinition & (sbol2.role.some(soClass))))
            ] 
            '''
        '''
        soClass1 = types.new_class(term, (so.SO_0000110,))
        soClass1.namespace=so
        soClass2 = types.new_class(term + "_gm", (so.SO_0000110,))
        soClass2.namespace=so
        
        sbolVisualTerm.equivalent_to = [
        onto.Glyph & ( onto.isGlyphOf.some(sbol2.ComponentDefinition & (sbol2.role.some(soClass1 | soClass2))))
            ] 
            '''
        '''
        soClass1 = types.new_class(term, (so.SO_0000110,))
        soClass1.namespace=so
        soClass2 = types.new_class(term + "_gm2", (so.SO_0000110,))
        soClass2.namespace=so
        soClass3 = types.new_class(term + "_gm3", (so.SO_0000110,))
        soClass3.namespace=so
        
 
        sbolVisualTerm.equivalent_to = [
        onto.Glyph & ( onto.isGlyphOf.some(sbol2.ComponentDefinition & (sbol2.role.some(soClass1 | soClass2 | soClass3))))
            ] 
            '''
        '''
        soClass1 = types.new_class(term, (so.SO_0000110,))
        soClass1.namespace=so
        soClass2 = types.new_class(term + "_gm", (so.SO_0000110,))
        soClass2.namespace=so
        
        sbolVisualTerm.equivalent_to = [
        onto.Glyph & ( onto.isGlyphOf.only(sbol2.ComponentDefinition & (sbol2.role.some(Or([soClass1,soClass2])))))]
    '''

def saveOntology():
    onto.save(file = "sbolv.txt", format = "rdfxml")
    onto.save(file = "sbolv.owl", format = "owl")

        


'''
with onto:
    class Drug(Thing):
        pass
    class Ingredient(Thing):
       pass
    class has_for_ingredient(ObjectProperty):
       domain    = [Drug]
       range     = [Ingredient]
    class TestDrug(Drug):
         equivalent_to = [Drug & has_for_ingredient.some (Ingredient)]
         '''
         
'''        
class Drug(Thing):
    namespace=onto

class Ingredient(Thing):
    namespace=onto

class has_for_ingredient(ObjectProperty):
    namespace=onto
    domain    = [onto.Drug]
    range     = [onto.Ingredient]
    
class TestDrug(Drug):
    equivalent_to = [onto.Drug & onto.has_for_ingredient.some (onto.Ingredient)]
'''   