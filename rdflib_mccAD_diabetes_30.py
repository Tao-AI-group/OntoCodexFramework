from rdflib import Graph, Namespace, BNode, Literal
from rdflib.namespace import RDF, RDFS, OWL

# Load the RDF graph
g = Graph()
g.parse("MCC_RDF_R_30", format="application/rdf+xml")

# Define namespaces
MC = Namespace("https://github.com/Tao-AI-group/MCContology#")

# Define Medications
medications = [
    (MC.Insulin, "Insulin"),
    (MC.Metformin, "Metformin"),
    (MC.GLP1ReceptorAgonist, "GLP-1_Receptor_Agonist"),
    (MC.SGLT2Inhibitor, "SGLT2_Inhibitor"),
    (MC.Sulfonylurea, "Sulfonylurea")
]

# Create Medication Subclasses
medication_class = MC.Medication
for med_uri, med_label in medications:
    if (med_uri, RDF.type, OWL.Class) not in g:
        g.add((med_uri, RDF.type, OWL.Class))
    g.add((med_uri, RDFS.subClassOf, medication_class))
    g.add((med_uri, RDFS.label, Literal(med_label, lang="en")))

# Add Restrictions to Diabetes Class
diabetes_class = MC.Diabetes
for med_uri, _ in medications:
    restriction_bnode = BNode()
    g.add((diabetes_class, RDFS.subClassOf, restriction_bnode))
    g.add((restriction_bnode, RDF.type, OWL.Restriction))
    g.add((restriction_bnode, OWL.onProperty, MC.has_medication))
    g.add((restriction_bnode, OWL.someValuesFrom, med_uri))

# Serialize updated graph
g.serialize("MCC_RDF_R_29_updated.owl", format="application/rdf+xml")

print("Medication subclasses and Diabetes medication restrictions added and saved to MCC_RDF_R_29_updated.owl")
