
#https://buildmedia.readthedocs.org/media/pdf/owlready2/latest/owlready2.pdf
from owlready2 import *
from Ontology import *
import types
import re
from RDFTypeChecker import RDFTypeChecker
from SBOLVisualMarkDown import SBOLVisualMarkDown 

onto = get_ontology("http://sbols.org/visual/v2")
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
SBO_MATERIAL_ENTITY_TERM = SBO_BASE_IRI + "SBO_0000240"
sboTypeChecker=RDFTypeChecker("../sbo.owl")
        
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
    label ="Glyph"

with onto:    
    class InteractionGlyph(Glyph):
        namespace=onto
        label ="InteractionGlyph"
        
    class InteractionNodeGlyph(Glyph):
        namespace=onto
        label ="InteractionNodeGlyph" 
    
    class MolecularSpeciesGlyph(Glyph):
        namespace=onto
        label ="MolecularSpeciesGlyph"      
        
    class SequenceFeatureGlyph(Glyph):
        namespace=onto
        label ="SequenceFeatureGlyph"      

with onto:
    AllDisjoint([InteractionGlyph, InteractionNodeGlyph,MolecularSpeciesGlyph, SequenceFeatureGlyph])
    

onto2 = get_ontology("http://test.org/onto.owl")
with onto2:
    class Drug(Thing):
        pass
    class ActivePrinciple(Thing):
        pass
    AllDisjoint([Drug, ActivePrinciple])
    
    
#, MolecularSpeciesGlyph, SequenceFeatureGlyph)     

class isGlyphOf(ObjectProperty):
    range:Glyph
    namespace=onto
    label ="isGlyphOf"

class hasGlyph(ObjectProperty):
    domain:Glyph
   # range: [uri]
    namespace=onto
    label ="hasGlyph"
    
class hasHead(ObjectProperty):
    domain:Glyph
    namespace=onto
    label ="hasHead"
    
class hasTail(ObjectProperty):
    domain:Glyph
    namespace=onto
    label ="hasTail"
    
class hasIncoming(ObjectProperty):
    domain:Glyph
    namespace=onto
    label ="hasIncoming"
    
class hasOutgoing(ObjectProperty):
    domain:Glyph
    namespace=onto
    label ="hasOutgoing"
    
class defaultGlyph(AnnotationProperty):
    domain:Glyph
    range: [str]
    namespace=onto 
    label ="defaultGlyph" 
    
class glyphDirectory(AnnotationProperty):
    domain:Glyph
    range: [str]
    namespace=onto 
    label ="glyphDirectory" 
    
class recommended(AnnotationProperty):
    domain:Glyph
    range: [bool]
    namespace=onto  
    label ="recommended"   
     
class isAlternativeOf(ObjectProperty):
    domain:Glyph
    range: Glyph
    namespace=onto    
    label ="isAlternativeOf"   
    
class prototypicalExample(AnnotationProperty):
    domain:Glyph
    range: [str]
    namespace=onto
    label ="prototypicalExample"
    
class notes(AnnotationProperty):
    domain:Glyph
    range: [str]
    namespace=onto  
    label ="notes"  

def getCategoryGlyph(sbolVisualMD):
    if "/Interactions/" in sbolVisualMD.getDirectory():
        return InteractionGlyph
    elif "/InteractionNodes/" in sbolVisualMD.getDirectory():
        return InteractionNodeGlyph
    elif "/FunctionalComponents/" in sbolVisualMD.getDirectory():
        return MolecularSpeciesGlyph
    else: 
        return SequenceFeatureGlyph
    

def createOntologyClass(termName, baseClass, ns):
    sbolVisualTerm = types.new_class(termName, (baseClass,))
    #types.new_class("NewClassName", (onto["classname"],))
    sbolVisualTerm.namespace=ns
    sbolVisualTerm.label=termName 
    return sbolVisualTerm

def addImage(ontologyClass,imageDirectory, image):
    #imgClass = createOntologyClass(image, img.ImageFile, img) 
    #ontologyClass.hasGlyph=imgClass
    ontologyClass.defaultGlyph=image
    ontologyClass.glyphDirectory=imageDirectory
    
        
def createVisualTermORG_Del(sbolVisualMD,termName):
    sbolVisualTerm = createOntologyClass(termName, onto.Glyph, onto)
    categoryGlyph=getCategoryGlyph(sbolVisualMD)
    sbolVisualTerm.is_a.append(categoryGlyph)
    sbolVisualTerm.comment=sbolVisualMD.getComment()  
    sbolVisualTerm.prototypicalExample=sbolVisualMD.getExample()
    sbolVisualTerm.notes=sbolVisualMD.getNotes()
    return sbolVisualTerm

def createVisualTerm(sbolVisualMD,termName):
    sbolVisualTerm = createOntologyClass(termName, onto.Glyph, onto)
    categoryGlyph=getCategoryGlyph(sbolVisualMD)
    if categoryGlyph==InteractionGlyph:
        createInteractionEdgeConstraints(sbolVisualTerm, sbolVisualMD)
    if categoryGlyph==InteractionNodeGlyph:
        createInteractionNodeConstraints (sbolVisualTerm, sbolVisualMD)
    sbolVisualTerm.is_a.append(categoryGlyph)
    sbolVisualTerm.comment=sbolVisualMD.getComment()  
    sbolVisualTerm.prototypicalExample=sbolVisualMD.getExample()
    sbolVisualTerm.notes=sbolVisualMD.getNotes()
    return sbolVisualTerm

''' GM: 20200902- Commented the previous working copy
def createVisualTerm(sbolVisualMD,termName):
    sbolVisualTerm = createOntologyClass(termName, onto.Glyph, onto)
    sbolVisualTerm.comment=sbolVisualMD.getComment()  
    sbolVisualTerm.prototypicalExample=sbolVisualMD.getExample()
    sbolVisualTerm.notes=sbolVisualMD.getNotes()
    return sbolVisualTerm
'''

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

def toOneDimensional(allOntologyTerms):
    ontologyTerms=[]
    for terms in allOntologyTerms:
        for term in terms :
            ontologyTerms.append(term) 
    return ontologyTerms

     
def createInteractionEdgeConstraints(sbolVisualTerm, sbolVisualMD):
    headTerms=sbolVisualMD.getHeadTypes()
    if headTerms:
        allOntologyTerms= getOntologyTermsFromLabels(headTerms)
        ontologyTerms=toOneDimensional(allOntologyTerms)
        if ontologyTerms:
            for ontologyTerm in ontologyTerms :
                #Use append rather than assigning to avoid overriding the previous subclass relationships.
                sbolVisualTerm.hasHead.append(sbol2.role.some(ontologyTerm))
            
    tailTerms=sbolVisualMD.getTailTypes()
    if tailTerms:
        allOntologyTerms= getOntologyTermsFromLabels(tailTerms)
        ontologyTerms=toOneDimensional(allOntologyTerms)
        if ontologyTerms:
            for ontologyTerm in ontologyTerms :
                #Use append rather than assigning to avoid overriding the previous subclass relationships.
                sbolVisualTerm.hasTail.append(sbol2.role.some(ontologyTerm))       
 
def createInteractionNodeConstraints(sbolVisualTerm, sbolVisualMD):
    headTerms=sbolVisualMD.getIncomingTypes()
    if headTerms:
        allOntologyTerms= getOntologyTermsFromLabels(headTerms)
        ontologyTerms=toOneDimensional(allOntologyTerms)
        if ontologyTerms:
            for ontologyTerm in ontologyTerms :
                #Use append rather than assigning to avoid overriding the previous subclass relationships.
                sbolVisualTerm.hasIncoming.append(sbol2.role.some(ontologyTerm))
            
    tailTerms=sbolVisualMD.getOutgoingTypes()
    if tailTerms:
        allOntologyTerms= getOntologyTermsFromLabels(tailTerms)
        ontologyTerms=toOneDimensional(allOntologyTerms)
        if ontologyTerms:
            for ontologyTerm in ontologyTerms :
                #Use append rather than assigning to avoid overriding the previous subclass relationships.
                sbolVisualTerm.hasOutgoing.append(sbol2.role.some(ontologyTerm))     
               
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
            elif sboTypeChecker.hasParent(sboUri, SBO_MATERIAL_ENTITY_TERM): 
                restrictionProperty=sbol2.type
                entity=sbol2.ComponentDefinition    
            else:
                print("---Only SBO terms from" + SBO_INTERACTION_PARENT_TERM + " and " + SBO_MATERIAL_ENTITY_TERM + " are allowed!")
                
        
        if restrictionProperty:
            sbolVisualTerm.isGlyphOf=entity #GMGMGM
            for ontologyTerm in ontologyTerms :
                #Use append rather than assigning to isGlyphOf to avoid overriding the previous subclass relationships.
                sbolVisualTerm.isGlyphOf.append(restrictionProperty.some(ontologyTerm))
                # This would be correct and a better way but would introduce RDF collection entities, which are not effective for SPARQL queries.
                #sbolVisualTerm.isGlyphOf=entity & restrictionProperty.some(ontologyTerm)
                
            '''
            This code works and was initially used to create subclass definitions as a single equivalentclass. However, SPARQL queries become difficult to write
            due to introducing collectins. Hence, we adopt the approach above using subClassOf restrictions.
            if len(ontologyTerms)==1:
                sbolVisualTerm.equivalent_to = [onto.Glyph & ( onto.isGlyphOf.some(entity & (restrictionProperty.some(ontologyTerms[0]))))] 
            elif len(ontologyTerms)>1:  
                sbolVisualTerm.equivalent_to = [onto.Glyph & ( onto.isGlyphOf.some(entity & (restrictionProperty.some(Or(ontologyTerms)))))] 
            '''
        else:
            print("---Could not find an allowed namespace: SO, BioPAX, SBO") 

def getSubString(text, substring1, substring2):
    index1=text.find(substring1)
    result=""
    if index1>-1:
        index1=index1 + len(substring1)
        index2=text.find(substring2)
        commentRecommended=text[index1:index2]
        result= commentRecommended.strip()
    return result

def createSubTerm(subTermName, baseTerm, comment, imageDirectory, image):
    sbolVisualAlternateTerm = createOntologyClass(subTermName, baseTerm, onto)   
    sbolVisualAlternateTerm.comment=comment
    addImage(sbolVisualAlternateTerm, imageDirectory, image)  
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
    
def createRecommendedTerms(sbolVisualMD, baseTerm, glyphBlocks, blockIndex,glyphTypes,imageDirectory):
    recommendedSubTerms=[]
    commentRecommended=""
    if blockIndex==0: # If the recommended term is in the first block than use the same comment for both the generic and recommended terms.
        commentRecommended=baseTerm.comment[0]
    else:
        commentRecommended=getStringBetweenGlyphBlocks(sbolVisualMD, glyphBlocks, blockIndex-1, blockIndex)  
    subTypeList=getSubTypes(commentRecommended)
    index=0
    for subType in subTypeList:
        recommendedName=subType + baseTerm.label[0]
        recommendedSubTerm=createSubTerm(recommendedName, baseTerm, commentRecommended,imageDirectory, glyphBlocks[blockIndex][index])
        recommendedSubTerm.recommended=True
        if len(glyphTypes)>1:
            recommendedOntologyTerms=getOntologyTermsFromLabelsForEachRow(glyphTypes[index])
            createImageConstraints(recommendedSubTerm, [recommendedOntologyTerms])
            
        else:
            test=""
            test=test + "sdf"
        recommendedSubTerms.append(recommendedSubTerm)   
        index=index+1
    #If there is only one glyph type included, then there is no need to copy it to all recommended terms. These recommended terms 
    # should inherit the type from the base term. i.e. "complex"
    if len(glyphTypes)==1:
        recommendedOntologyTerms=getOntologyTermsFromLabelsForEachRow(glyphTypes[0])
        createImageConstraints(baseTerm, [recommendedOntologyTerms])
        
    if  len(recommendedSubTerms)==0:
        print("---" + "Could not create the recommended terms for " + baseTerm.label[0])      
    return recommendedSubTerms 


def getSubTypes(text):
    subTypeList=[]
    subTypes=getSubString(text, "in order:", "):")
    if subTypes:
        subTypeList=subTypes.split(",") 
        #subTypeList = [x.replace(' ', '') for x in subTypeList]       
        subTypeList = [capitalise(x) for x in subTypeList]       
    return subTypeList

def capitalise (text):
    wordList = re.split(" |-",text)
    wordList = [x.capitalize() for x in wordList]
    text="".join(wordList)
    text = text.replace(' ', '')
    return text
    

def createAlternativeTerms(sbolVisualMD, glyphBlocks, blockIndex,recommendedSubTerms, glyphTypes, imageDirectory):
    commentAlternative=getStringBetweenGlyphBlocks(sbolVisualMD, glyphBlocks, blockIndex-1, blockIndex)  
    alternativeTerms=[]
    index=0
    for recommendedSubTerm in recommendedSubTerms:
        subTermName=recommendedSubTerm.label[0] + "Alternative"
        subTerm=createSubTerm(subTermName, recommendedSubTerms[index], commentAlternative, imageDirectory, glyphBlocks[blockIndex][index])
        subTerm.isAlternativeOf=recommendedSubTerm
        alternativeTerms.append(subTerm)
        #ontologyTermsForSubTerm=getOntologyTermsFromLabelsForEachRow(glyphTypes[index])
        #createImageConstraints(subTerm, [ontologyTermsForSubTerm])
        index=index+1
    return alternativeTerms


                                                                
def addOntologyTerms(mdContent,termName):
    sbolVisualMD=SBOLVisualMarkDown(mdContent)
    #termName2=sbolVisualMD.getGlyphLabel() 
    
    sbolVisualTerm=createVisualTerm(sbolVisualMD,termName)
    imageDirectory= sbolVisualMD.getDirectory()
    images=sbolVisualMD.getGlyphs()
    
    glyphTypes=sbolVisualMD.getGlyphTypes()
    
    allOntologyTerms=getOntologyTermsFromLabels(glyphTypes)
    
    createImageConstraints(sbolVisualTerm, allOntologyTerms)
    
    glyphBlocks=sbolVisualMD.getGlyphBlocks()
    numberOfGlyphBlocks=len(glyphBlocks)
        
    if len(images)==1:
        addImage(sbolVisualTerm,imageDirectory, images[0])
        sbolVisualTerm.recommended=True
    elif len(glyphTypes)==1 and len(images)==2:
        addImage(sbolVisualTerm, imageDirectory, images[0])
        sbolVisualTerm.recommended=True
        alternateTermName=sbolVisualTerm.label[0]+ "Alternative" 
        alternativeTerm=createSubTerm(alternateTermName, sbolVisualTerm, sbolVisualMD.getCommentAfterImage(images[0]), imageDirectory, images[1])  
        #createImageConstraints(alternativeTerm, allOntologyTerms)
        alternativeTerm.isAlternativeOf=sbolVisualTerm
    elif (numberOfGlyphBlocks==2):
        if len(images)==(len(glyphTypes)+1):
        #There are n glyph types (row with ontology terms.)
        # The first one is the base term
        # The second glyph block includes recommended images. One image per row 
            if len(glyphBlocks[0])==1 and len(glyphBlocks[1])==len(glyphTypes):
                addImage(sbolVisualTerm, imageDirectory, images[0])
                createRecommendedTerms(sbolVisualMD, sbolVisualTerm, glyphBlocks, 1, glyphTypes, imageDirectory)  
        
        elif (len(glyphTypes) * 2 == len(images)):
        #The number of image types times 2 is equal to the number of images. For each type there are two images! E.g. Overhang
        # There is no image for the base term
            recommendedSubTerms=createRecommendedTerms(sbolVisualMD, sbolVisualTerm, glyphBlocks, 0, glyphTypes, imageDirectory)
            createAlternativeTerms(sbolVisualMD, glyphBlocks, 1, recommendedSubTerms, glyphTypes, imageDirectory) 
        
        elif (len(glyphBlocks[1])==1):
        #There are only two blocks and the there is only one image in the second block
            recommendedSubTerms=createRecommendedTerms(sbolVisualMD, sbolVisualTerm, glyphBlocks, 0, glyphTypes, imageDirectory)
            alternateTermName=sbolVisualTerm.label[0] + "Alternative" 
            commentAlternative=getStringBetweenGlyphBlocks(sbolVisualMD, glyphBlocks, 0, 1)  
            alternativeTerm=createSubTerm(alternateTermName, sbolVisualTerm, commentAlternative, imageDirectory, glyphBlocks[1][0]) 
            for recommendedTerm in recommendedSubTerms:
                alternativeTerm.is_a.append(recommendedTerm)
                                   
    elif (numberOfGlyphBlocks==3):
        if len(glyphBlocks[0])==1 and len(glyphBlocks[1])==len(glyphTypes) and len(glyphBlocks[2])==len(glyphTypes):
            #There are n glyph types (row with ontology terms.)
            # The first one is the base term
            # The second glyph block includes recommended images. One image per row
            # The third glyph block includes the images for the alternatives. One image per row.
            addImage(sbolVisualTerm, imageDirectory, images[0])
            recommendedSubTerms=createRecommendedTerms(sbolVisualMD, sbolVisualTerm, glyphBlocks, 1, glyphTypes, imageDirectory)
            createAlternativeTerms(sbolVisualMD, glyphBlocks, 2, recommendedSubTerms, glyphTypes, imageDirectory)          
    else:
        print("---Number of glyph types:" + str(len(glyphTypes)) + " , Number of images:" + str(len(images)))  
        blocks= sbolVisualMD.getGlyphBlocks()
        for block in blocks:
            print("---Block")
            for image in block:
                print ("------" + image)
                                                      
def saveOntology():
    onto.save(file = "../sbol-vo.txt", format = "rdfxml")
    onto.save(file = "../sbol-vo.rdf", format = "rdfxml")
      
    # isGlyphOf some  (role some SO:0000167)
    
    
    