'''
Created on 4 Apr 2019

@author: gokselmisirli
'''
import rdflib
from rdflib.plugins.sparql import prepareQuery

class RDFTypeChecker (object):
    def __init__(self, owlFile):
        self._g = g=rdflib.Graph()
        g.load(owlFile)

    
    def hasParent(self, childUri, parentUri):
        queryString= "select ?o where {<" + childUri + "> rdfs:subClassOf* ?o .}"
        for row in self._g.query(queryString):
            if str(row.o)==parentUri:
                return True
        return False      
'''
    q= prepareQuery(
        'select ?o where {sbo:SBO_0000177 rdfs:subClassOf* ?o .}',
        initNs = { "sbo": "http://biomodels.net/SBO/" })  
   ''' 
'''    
for row in g.query(
    'select ?o where { sbo:SBO_0000177 rdfs:subClassOf ?o .}'):
    print(row.s)
'''