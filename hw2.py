'''
Created on 29 Mar 2019

@author: gokselmisirli
'''
from owlready2 import *
import types

print ("hello2")

onto = get_ontology("http://sbolstandard.org/visual#")
sbol = get_ontology("https://dissys.github.io/sbol-owl/sbol.rdf")
sbol2 = get_ontology("http://sbolstandard.org/v2")
so = get_ontology("http://identifiers.org/so/")

onto.imported_ontologies.append(sbol)

     
class ComponentDefinition (Thing):
    namespace=sbol2
    
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
 
          
onto.save(file = "sbolvisual.txt", format = "rdfxml")
onto.save(file = "sbolvisual.omn", format = "omn")

        


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