
#https://buildmedia.readthedocs.org/media/pdf/owlready2/latest/owlready2.pdf
from owlready2 import *
from Ontology import *
import types
import re
from RDFTypeChecker import RDFTypeChecker
from SBOLVisualMarkDown import SBOLVisualMarkDown 

onto = get_ontology("http://sbolstandard.org/visual#")
sbol = get_ontology("https://dissys.github.io/sbol-owl/sbol.rdf")
sbol2 = get_ontology("http://sbols.org/v2")
so = get_ontology("http://identifiers.org/so/")
biopax = get_ontology("http://www.biopax.org/release/biopax-level3.owl")
sbo = get_ontology("http://identifiers.org/sbo/")

img = get_ontology("https://github.com/SynBioDex/SBOL-visual/blob/master/Glyphs/")

onto.imported_ontologies.append(sbol)

sbol2ns = sbol2.get_namespace("http://sbols.org/v2")

SBO_BASE_IRI="http://biomodels.net/SBO/"
SBO_INTERACTION_PARENT_TERM=SBO_BASE_IRI + "SBO_0000231"
sboTypeChecker=RDFTypeChecker("sbo.owl")
        
class ComponentDefinition (Thing):
    namespace=sbol2

class Interaction (Thing):
    namespace=sbol2
    
class ImageFile (Thing):
    namespace=img 
    
class SO_0000110 (Thing):
    namespace=so  

class BioPAXPhysicalEntity(Thing):
    namespace=biopax

class SBO_0000000(Thing):
    namespace=sbo

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
    
class defaultGlyph(AnnotationProperty):
    domain:Glyph
    range: [str]
    namespace=onto  
    
class recommended(AnnotationProperty):
    domain:Glyph
    range: [bool]
    namespace=onto    
     
class isAlternativeOf(ObjectProperty):
    domain:Glyph
    range: Glyph
    namespace=onto    
    
class prototypicalExample(AnnotationProperty):
    domain:Glyph
    range: [str]
    namespace=onto
    
class notes(AnnotationProperty):
    domain:Glyph
    range: [str]
    namespace=onto    

def createOntologyClass(termName, baseClass, ns):
    sbolVisualTerm = types.new_class(termName, (baseClass,))
    #types.new_class("NewClassName", (onto["classname"],))
    sbolVisualTerm.namespace=ns
    sbolVisualTerm.label=termName 
    return sbolVisualTerm

def addImage(ontologyClass,image):
    #imgClass = createOntologyClass(image, img.ImageFile, img) 
    #ontologyClass.hasGlyph=imgClass
    ontologyClass.defaultGlyph=image
        
def createVisualTerm(sbolVisualMD,termName):
    sbolVisualTerm = createOntologyClass(termName, onto.Glyph, onto)
    sbolVisualTerm.comment=sbolVisualMD.getComment()  
    sbolVisualTerm.prototypicalExample=sbolVisualMD.getExample()
    sbolVisualTerm.notes=sbolVisualMD.getNotes()
    return sbolVisualTerm

def getOntologyTermsFromLabels(glyphTypes):
    allOntologyTerms=[]
    for terms in glyphTypes:
        ontologyTerms=getOntologyTermsFromLabelsForEachRow(terms)
        allOntologyTerms.append(ontologyTerms)
    return allOntologyTerms

def getOntologyTermsFromLabelsForEachRow(terms):
    ontologyTerms=[]
    for term in terms :
        if term.startswith("SO"):
            ontologyTerms.append(createOntologyClass(term, so.SO_0000110, so))    
        elif term.startswith(biopax.base_iri):
            term=term.replace(biopax.base_iri,"").replace("#","")
            ontologyTerms.append(createOntologyClass(term, biopax.BioPAXPhysicalEntity, biopax))
        elif term.startswith("SBO"):
            #sboUri=SBO_BASE_IRI + term.replace(":","_")
            #if sboTypeChecker.hasParent(sboUri, SBO_INTERACTION_PARENT_TERM): 
            ontologyTerms.append(createOntologyClass(term, sbo.SBO_0000000, sbo))
            #else:     
            #    print ("SBO:Not_Interaction----------------")
        else:
            print ("Not categorised")
        
    ontologyTerms
    return ontologyTerms

def hasNameSpace(ontologyTerms, ns):
    for term in ontologyTerms :
        if term.namespace==ns:
            return True
        return False
    
def createImageConstraints(sbolVisualTerm, allOntologyTerms):
    ontologyTerms=[]
    for terms in allOntologyTerms:
        for term in terms :
            ontologyTerms.append(term)        
    if allOntologyTerms:
        restrictionProperty=None
        entity=None
        if hasNameSpace(ontologyTerms, so):   
            restrictionProperty=sbol2.role
            entity=sbol2.ComponentDefinition   
        elif hasNameSpace(ontologyTerms, biopax):  
            restrictionProperty=sbol2.type
            entity=sbol2.ComponentDefinition 
        elif hasNameSpace(ontologyTerms, sbo):  
            sboUri=SBO_BASE_IRI + term.name.replace(":","_")
            if sboTypeChecker.hasParent(sboUri, SBO_INTERACTION_PARENT_TERM): 
                restrictionProperty=sbol2.type
                entity=sbol2.Interaction
            else:
                print("---Only SBO terms from" + SBO_INTERACTION_PARENT_TERM + "are allowed")
                 
        if restrictionProperty:
            if len(ontologyTerms)==1:
                sbolVisualTerm.equivalent_to = [onto.Glyph & ( onto.isGlyphOf.some(entity & (restrictionProperty.some(ontologyTerms[0]))))] 
            elif len(ontologyTerms)>1:  
                sbolVisualTerm.equivalent_to = [onto.Glyph & ( onto.isGlyphOf.some(entity & (restrictionProperty.some(Or(ontologyTerms)))))] 
        else:
            print("---Could not find an allowed namespace: SO, BioPAX, SBO") 

def getSubString(text, substring1, substring2):
    index1=text.find(substring1)
    index1=index1 + len(substring1)
    index2=text.find(substring2)
    commentRecommended=text[index1:index2]
    return commentRecommended.strip()

def createSubTerm(subTermName, baseTerm, comment, image):
    sbolVisualAlternateTerm = createOntologyClass(subTermName, baseTerm, onto)   
    sbolVisualAlternateTerm.comment=comment
    addImage(sbolVisualAlternateTerm, image)  
    return sbolVisualAlternateTerm
         
def getStringBetweenImages(sbolVisualMD, image1,image2):
    searchString1= sbolVisualMD.GLYPH_TEMPLATE.format(image1)
    searchString2= sbolVisualMD.GLYPH_TEMPLATE.format(image2)
    text=sbolVisualMD.getGlyphText()
    subString=getSubString(text,searchString1,searchString2)
    return subString

def getStringBetweenGlyphBlocks(sbolVisualMD, glyphBlocks, blockIndex1, blockIndex2):
    lenBlockImages=len(glyphBlocks[blockIndex1])
    comment=getStringBetweenImages(sbolVisualMD, glyphBlocks[blockIndex1][lenBlockImages-1], glyphBlocks[blockIndex2][0])
    return comment
    
def createRecommendedTerms(sbolVisualMD, baseTerm, glyphBlocks, blockIndex1, blockIndex2,glyphTypes):
    recommendedSubTerms=[]
    commentRecommended=getStringBetweenGlyphBlocks(sbolVisualMD, glyphBlocks, blockIndex1, blockIndex2)  
    subTypeList=getSubTypes(commentRecommended)
    index=0
    for subType in subTypeList:
        recommendedName=subType + baseTerm.label[0]
        recommendedSubTerm=createSubTerm(recommendedName, baseTerm, commentRecommended, glyphBlocks[1][index])
        recommendedSubTerm.recommended=True
        recommendedOntologyTerms=getOntologyTermsFromLabelsForEachRow(glyphTypes[index])
        createImageConstraints(recommendedSubTerm, [recommendedOntologyTerms])
        index=index+1
        recommendedSubTerms.append(recommendedSubTerm)          
    return recommendedSubTerms 

def getSubTypes(text):
    subTypeList=[]
    subTypes=getSubString(text, "in order:", "):")
    if subTypes:
        subTypeList=subTypes.split(",") 
    subTypeList = [x.replace(' ', '') for x in subTypeList]       
    return subTypeList

def createAlternativeTerms(sbolVisualMD, glyphBlocks, blockIndex1, blockIndex2,recommendedSubTerms,glyphTypes):
    commentAlternative=getStringBetweenGlyphBlocks(sbolVisualMD, glyphBlocks, blockIndex1, blockIndex2)  
    alternativeTerms=[]
    index=0
    for recommendedSubTerm in recommendedSubTerms:
        subTermName=recommendedSubTerm.label[0] + "Alternative"
        subTerm=createSubTerm(subTermName, recommendedSubTerms[index], commentAlternative, glyphBlocks[2][index])
        subTerm.isAlternativeOf=recommendedSubTerm
        alternativeTerms.append(subTerm)
        #ontologyTermsForSubTerm=getOntologyTermsFromLabelsForEachRow(glyphTypes[index])
        #createImageConstraints(subTerm, [ontologyTermsForSubTerm])
        index=index+1
    return alternativeTerms
                                                            
def addOntologyTerms(mdContent):
    sbolVisualMD=SBOLVisualMarkDown(mdContent)
    termName=sbolVisualMD.getGlyphLabel() 
    sbolVisualTerm=createVisualTerm(sbolVisualMD,termName)
     
    images=sbolVisualMD.getGlyphs()
    
    glyphTypes=sbolVisualMD.getGlyphTypes()
    
    allOntologyTerms=getOntologyTermsFromLabels(glyphTypes)
    
    createImageConstraints(sbolVisualTerm, allOntologyTerms)
    
    glyphBlocks=sbolVisualMD.getGlyphBlocks()
    numberOfGlyphBlocks=len(glyphBlocks)
        
    if len(images)==1:
        addImage(sbolVisualTerm, images[0])
        sbolVisualTerm.recommended=True
    elif len(glyphTypes)==1 and len(images)==2:
        addImage(sbolVisualTerm, images[0])
        sbolVisualTerm.recommended=True
        alternateTermName=termName + "Alternative" 
        alternativeTerm=createSubTerm(alternateTermName, sbolVisualTerm, sbolVisualMD.getCommentAfterImage(images[0]), images[1])  
        #createImageConstraints(alternativeTerm, allOntologyTerms)
        alternativeTerm.isAlternativeOf=sbolVisualTerm
    elif len(images)==(len(glyphTypes)+1):
        #There are n glyph types (row with ontology terms.)
        # The first one is the base term
        # The second glyph block includes recommended images. One image per row 
        if (numberOfGlyphBlocks==2):
            if len(glyphBlocks[0])==1 and len(glyphBlocks[1])==len(glyphTypes):
                addImage(sbolVisualTerm, images[0])
                createRecommendedTerms(sbolVisualMD, sbolVisualTerm, glyphBlocks, 0, 1, glyphTypes)                     
    elif (numberOfGlyphBlocks==3):
        if len(glyphBlocks[0])==1 and len(glyphBlocks[1])==len(glyphTypes) and len(glyphBlocks[2])==len(glyphTypes):
            #There are n glyph types (row with ontology terms.)
            # The first one is the base term
            # The second glyph block includes recommended images. One image per row
            # The third glyph block includes the images for the alternatives. One image per row.
            addImage(sbolVisualTerm, images[0])
            recommendedSubTerms=createRecommendedTerms(sbolVisualMD, sbolVisualTerm, glyphBlocks, 0, 1, glyphTypes)
            createAlternativeTerms(sbolVisualMD, glyphBlocks, 1, 2, recommendedSubTerms,glyphTypes)          
    else:
        print("---Number of glyph types:" + str(len(glyphTypes)) + " , Number of images:" + str(len(images)))  
        blocks= sbolVisualMD.getGlyphBlocks()
        for block in blocks:
            print("---Block")
            for image in block:
                print ("------" + image)
                                                      
def saveOntology():
    onto.save(file = "sbolv.txt", format = "rdfxml")
    onto.save(file = "sbolv.rdf", format = "rdfxml")
      
    # isGlyphOf some  (role some SO:0000167)