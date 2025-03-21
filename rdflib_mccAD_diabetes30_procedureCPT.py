from rdflib import Graph, Namespace, RDF, RDFS, OWL, BNode, Literal

# Load the RDF graph from the uploaded file
g = Graph()
g.parse("MCC_RDF_R_30", format="xml")

# Define namespace
NS = Namespace("https://github.com/Tao-AI-group/MCContology#")

# Define the existing Diabetes and Procedure classes
diabetes_class = NS.Diabetes
procedure_superclass = NS.Procedure

# List of new procedures to add
procedures = [
    "Insulin_Administration",
    "Glucose_Monitoring",
    "Hemoglobin_A1C_Test",
    "Medical_Nutrition_Therapy"
]

# Add new procedure subclasses and restrictions
for procedure in procedures:
    procedure_class = NS[procedure]
    g.add((procedure_class, RDF.type, OWL.Class))
    g.add((procedure_class, RDFS.label, Literal(procedure)))
    g.add((procedure_class, RDFS.subClassOf, procedure_superclass))
    
    # Create restriction
    restriction = BNode()
    g.add((restriction, RDF.type, OWL.Restriction))
    g.add((restriction, OWL.onProperty, NS.has_procedure))
    g.add((restriction, OWL.someValuesFrom, procedure_class))
    
    # Link restriction to existing Diabetes class
    g.add((diabetes_class, RDFS.subClassOf, restriction))

# Save updated RDF
updated_file = "MCC_RDF_R_30_updated.owl"
g.serialize(destination=updated_file, format="xml")

print(f"Updated RDF saved to {updated_file}")
