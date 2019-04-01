'''
Created on 29 Mar 2019

@author: gokselmisirli
'''
#https://buildmedia.readthedocs.org/media/pdf/owlready2/latest/owlready2.pdf
from owlready2 import *
from ontology import *

import types

print ("hello")

onto = get_ontology("http://sbolstandard.org/visual#")
sbol = get_ontology("https://dissys.github.io/sbol-owl/sbol.rdf")
sbol2 = get_ontology("http://sbolstandard.org/v2")
so = get_ontology("http://identifiers.org/so/")

onto.imported_ontologies.append(sbol)

     
class ComponentDefinition (Thing):
    namespace=sbol2

class SO_0000110 (Thing):
    namespace=so  
      
class SO_0000167 (Thing):
    namespace=so

class role(ObjectProperty):
    namespace=sbol2

 
class Glyph(Thing):
    namespace=onto

class isGlyphOf(ObjectProperty):
    range:Glyph
    namespace=onto

class InsulatorGlyph(Glyph):
    equivalent_to = [
        onto.Glyph & ( onto.isGlyphOf.some(sbol2.ComponentDefinition & (sbol2.role.some(so.SO_0000167))))
            ] 

InsulatorGlyph2 = types.new_class("InsulatorGlyph2", (onto.Glyph,))
InsulatorGlyph2.namespace=onto
   
InsulatorGlyph2.equivalent_to = [
        onto.Glyph & ( onto.isGlyphOf.some(sbol2.ComponentDefinition & (sbol2.role.some(so.SO_0000167))))
            ] 
 

def addOntologyTerms(mdContent):
    termName=mdContent.title + "Glyph"   
    sbolVisualTerm = types.new_class(termName, (onto.Glyph,))
    sbolVisualTerm.namespace=onto
    for line in mdContent.terms.split("\n"):
        term=line.split(" ")[0]
        term=term[0:-1]
        term=term.replace(":","_")
        print ("Term:" + term)
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
        soClass1 = types.new_class(term, (so.SO_0000110,))
        soClass1.namespace=so
        soClass2 = types.new_class(term + "_gm", (so.SO_0000110,))
        soClass2.namespace=so
        
        sbolVisualTerm.equivalent_to = [
        onto.Glyph & ( onto.isGlyphOf.only(sbol2.ComponentDefinition & (sbol2.role.some(Or([soClass1,soClass2])))))]

    

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