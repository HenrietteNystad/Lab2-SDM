import random
from rdflib import Graph, Namespace, RDF, RDFS, Literal

# Define namespaces URIs
EX = Namespace("http://example.org/sdm-kg#")


def bind_namespaces(g: Graph):
    g.bind("", EX)
    g.bind("rdf", RDF)
    g.bind("rdfs", RDFS)


# Subclasses from the task and additional ones to make the schema more complete
drug_types = [EX.AntiInflammatoryDrug, EX.AntibioticDrug,
              EX.AntiviralDrug, EX.AnalgesicDrug]
disease_types = [EX.InfectiousDisease, EX.InflammatoryDisease,
                 EX.RespiratoryDisease, EX.GastrointestinalDisease]


def add_schema(g: Graph):
    # Base classes
    g.add((EX.Drug, RDF.type, RDFS.Class))
    g.add((EX.Disease, RDF.type, RDFS.Class))

    # Subclasses
    for c in drug_types:
        g.add((c, RDF.type, RDFS.Class))
        g.add((c, RDFS.subClassOf, EX.Drug))

    for c in disease_types:
        g.add((c, RDF.type, RDFS.Class))
        g.add((c, RDFS.subClassOf, EX.Disease))

    # Properties
    for p in [EX.affects, EX.treats, EX.relieves, EX.worsens]:
        g.add((p, RDF.type, RDF.Property))

    # Creating subproperty relationships
    g.add((EX.treats, RDFS.subPropertyOf, EX.affects))
    g.add((EX.relieves, RDFS.subPropertyOf, EX.affects))
    g.add((EX.worsens, RDFS.subPropertyOf, EX.affects))

    # Adding domain/range for affects
    g.add((EX.affects, RDFS.domain, EX.Drug))
    g.add((EX.affects, RDFS.range, EX.Disease))


def add_data(g: Graph, n_drugs=50, n_diseases=50, seed=42):
    random.seed(seed)

    # Adding core instances from the task description
    g.add((EX.Ibuprofen, RDF.type, EX.AntiInflammatoryDrug))
    g.add((EX.Amoxicillin, RDF.type, EX.AntibioticDrug))
    g.add((EX.BacterialInfection, RDF.type, EX.InfectiousDisease))
    g.add((EX.Arthritis, RDF.type, EX.InflammatoryDisease))
    g.add((EX.GastricUlcer, RDF.type, EX.Disease))

    # Adding relationships from the task description
    g.add((EX.Amoxicillin, EX.treats, EX.BacterialInfection))
    g.add((EX.Ibuprofen, EX.relieves, EX.Arthritis))
    g.add((EX.Ibuprofen, EX.worsens, EX.GastricUlcer))

    # Create additional random instances and relationships
    relationships = [EX.treats, EX.relieves, EX.worsens]

    drugs = []
    diseases = []

    # Create drug instances
    for i in range(n_drugs):
        d = EX[f"Drug_{i:03d}"]
        g.add((d, RDF.type, random.choice(drug_types)))
        g.add((d, RDFS.label, Literal(f"Drug {i:03d}", lang="en")))
        drugs.append(d)

    # Create disease instances
    for i in range(n_diseases):
        dis = EX[f"Disease_{i:03d}"]
        g.add((dis, RDF.type, random.choice(disease_types)))
        g.add((dis, RDFS.label, Literal(f"Disease {i:03d}", lang="en")))
        diseases.append(dis)

    # Create random relationships
    for d in drugs:
        for i in range(random.randint(1, 3)):
            rel = random.choice(relationships)
            dis = random.choice(diseases)
            g.add((d, rel, dis))


def main():
    g = Graph()
    bind_namespaces(g)
    add_schema(g)
    add_data(g, n_drugs=50, n_diseases=50, seed=42)

    # Serialize the graph to a file
    g.serialize(destination="G11J-LinNystad.ttl", format="turtle")


if __name__ == "__main__":
    main()
