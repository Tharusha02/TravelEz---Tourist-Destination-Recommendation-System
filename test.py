from rdflib import Graph, Namespace
from rdflib.plugins.sparql import prepareQuery
import re

# Load your RDF data from a file or URL
g = Graph()
g.parse("onto.rdf") 


# Define the namespace
ns = Namespace("http://example.com/LocationCity#")

# Define the SPARQL query
query = prepareQuery("""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX City: <http://example.com/LocationCity#>

    SELECT ?subclass ?label ?comment
    WHERE {
        ?subclass rdfs:subClassOf City:ColomboRestaurants;
                  rdfs:label ?label;
                  rdfs:comment ?comment.
    }
""")

count = 0

# Execute the query and iterate over the results
for row in g.query(query):
    if count >= 5:  # Check if the counter reaches 5
        break  # If so, break out of the loop
    uri = row[0]  # Get the URI from the result tuple
    name = uri.split("#")[-1]  # Split the URI by '#' and get the last part
    # Split the name into separate words by capitalization using regex
    words = re.findall('[A-Z][a-z]*', name)
    # Join the words into a single string separated by spaces
    formatted_name = ' '.join(words)
    comment = row[1]  # Get the comment from the result tuple
    # Split the comment into separate lines if it contains multiple comments
    comments = comment.split("\\n")
    # Print the name and comments
    print(f"Name: {formatted_name}")
    for c in comments:
        print(f"    Comment: {c}")
    count += 1