from rdflib import Graph, Namespace, RDF, RDFS

# Create a new RDF graph
# g = Graph()

# Define namespaces URIs
EX = Namespace("http://example.org/sdm-kg#")

def bind_namespaces(g : Graph):
    g.bind("", EX)
    g.bind("rdf", RDF)
    g.bind("rdfs", RDFS)

def add_schema(g : Graph):
    # Adding classes
    for c in [EX.Drug, EX.Disease, EX.AntiInflammatoryDrug, EX.AntibioticDrug, EX.InfectiousDisease, EX.InflammatoryDisease]:
        g.add((c, RDF.type, RDFS.Class))

    # Creating subclass relationships
    g.add((EX.AntiInflammatoryDrug, RDFS.subClassOf, EX.Drug))
    g.add((EX.AntibioticDrug, RDFS.subClassOf, EX.Drug))
    g.add((EX.InfectiousDisease, RDFS.subClassOf, EX.Disease))
    g.add((EX.InflammatoryDisease, RDFS.subClassOf, EX.Disease))

    # Adding properties
    for p in [EX.affects, EX.treats, EX.relieves, EX.worsens]:
        g.add((p, RDF.type, RDF.Property))

    # Creating subproperty relationships
    g.add((EX.treats, RDFS.subPropertyOf, EX.affects))
    g.add((EX.relieves, RDFS.subPropertyOf, EX.affects))
    g.add((EX.worsens, RDFS.subPropertyOf, EX.affects))

    # Adding domain/range for affects
    g.add((EX.affects, RDFS.domain, EX.Drug))
    g.add((EX.affects, RDFS.range, EX.Disease))

def add_data(g : Graph):
    # Adding instances from task
    g.add((EX.Ibuprofen, RDF.type, EX.AntiInflammatoryDrug))
    g.add((EX.Amoxicillin, RDF.type, EX.AntibioticDrug))
    g.add((EX.BacterialInfection, RDF.type, EX.InfectiousDisease))
    g.add((EX.Arthritis, RDF.type, EX.InflammatoryDisease))
    g.add((EX.GastricUlcer, RDF.type, EX.Disease))

    # Adding relationships
    g.add((EX.Amoxicillin, EX.treats, EX.BacterialInfection))
    g.add((EX.Ibuprofen, EX.relieves, EX.Arthritis))
    g.add((EX.Ibuprofen, EX.worsens, EX.GastricUlcer))

def main():
    g = Graph()
    bind_namespaces(g)
    add_schema(g)
    add_data(g)

    # Serialize the graph to a file
    g.serialize(destination="G11J-LinNystad.ttl", format="turtle")

if __name__ == "__main__":
    main()
