# from rdflib import Namespace, URIRef, Graph
# from rdflib.namespace import RDF

# data = Namespace('https://www.cp.eng.chula.ac.th/~peerapon/5555')

# g = Graph()
# g.bind('ESRA-KG', data)

# entities = [
#     (URIRef(data.Alice), RDF.type , data.Wikidata),
#     (URIRef(data.Alice), RDF.type , data.CSOTopic),
#     (URIRef(data.Bob), RDF.type , data.Wikidata),
# ]

# for i in entities:
#     g.add(i)
    
# g.add( (URIRef(data.Alice), data.MagPaper, URIRef(data.Bob)) )

# g.serialize(destination='output.txt', format='turtle')