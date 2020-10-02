# SBOL Visual Ontology (SBOL-VO)
The SBOL Visual Ontology (SBOL-VO) provides a set of controlled terms to describe visual glyphs for genetic circuit designs.  The terms are organised based on their descriptions in community-edited [Markdown](https://github.com/SynBioDex/SBOL-visual/tree/master/Glyphs) files. Terms are defined for recommended and alternative glyphs in addition to terms to represent generic glyphs. SBOL-VO consists of the following items.

* **A base term**. The base term in the ontology is called "Glyph".
* **Terms for glyphs**. Examples include "AptamerGlyph", "AssemblyScarGlyph" and "AssemblyScarGlyphAlternative".
* **Properties**. SBOL-VO includes object properties such as "hasGlyph" and "isAlternativeOf" to define the relationships between different terms.
* **Annotations**. Terms are annotated using properties such as "defaultGlyph" and "recommended".

## Browse
[Browse the SBOL-VO terms via an HTML page.](https://dissys.github.io/sbol-visual-ontology/sbol-vo.html)

The ontology can also be viewed after downloading and opening in an ontology editor, such as Protege.

## Download
SBOL-VO is available as an RDF file. [Click here](http://dissys.github.io/sbol-visual-ontology/sbol-vo.rdf) to download the ontology. 

## Development
The Python code to generate the ontology is maintained by [Goksel Misirli](mailto:g.misirli@keele.ac.uk) and is available at the [sbol-visual-ontology](https://github.com/dissys/sbol-visual-ontology) GitHub repository.

If you are interested in contributing, please see below.
### Prerequisites
* Make sure you have git and python3 installed. Then install owlready2 and rdflib python libraries. 
```
pip3 install owlready2
pip3 install rdflib
```
* Download SBOL-Visual project.
```
git clone https://github.com/SynBioDex/SBOL-visual.git
```
 and place it at the same level with the SBOL-Visual-Ontology folder. The parent working folder should look like below:
```
- Parent working folder
  - SBOL-visual
  - sbol-visual-ontology
```

