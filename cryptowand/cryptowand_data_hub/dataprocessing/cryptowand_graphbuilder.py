from arango import ArangoClient
import json
import time
import requests

json_categories_file_name = "../output/CryptoWand-Categories.json"

with open(json_categories_file_name, 'r') as my_c_file:
    data_c = my_c_file.read()
data_c_dict = json.loads(data_c)

def get_api_response(url):
    try:
        content = requests.get(url)
        return json.loads(content.content)
    except:
        return 'Error Fetching API Response'

def build_cryptowand_graph (graph_name,data_c_dict) :
    # Initialize the client for ArangoDB.
    client = ArangoClient(hosts="http://localhost:8529")

    # Connect to "test" database as root user.
    db = client.db("cryptodata", username="rsenthilk", password="myPass00")

    if db.has_graph(graph_name):
        graph = db.graph(graph_name)
    else:
        graph = db.create_graph(graph_name)

    # Create vertex collections for the graph.
    coins = graph.create_vertex_collection("coins")
    categories = graph.create_vertex_collection("categories")

    edges = graph.create_edge_definition(
        edge_collection="belongsto",
        from_vertex_collections=["coins"],
        to_vertex_collections=["categories"]
    )
    n=0
    for category in data_c_dict:
        cat_id = category['id']
        cgecko_cat_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&category=" + \
            cat_id+"&order=market_cap_desc&per_page=100&page=1&sparkline=false"
        categories.insert({"_key": cat_id, "name" : cat_id})
        print('Added Category ' + cat_id)
        cat_coins = get_api_response(cgecko_cat_url)
        print(" n " + str(n)) 
        for coin in cat_coins:
            try:
                n=n+1
                coin = coin['symbol']
                coins.insert({"_key" : str(n), "name" : coin })
                print('Added Coin ' + coin)
                edge_from = "coins/" + str(n)
                edge_to = "categories/" + cat_id
                edges.insert({"_from": edge_from, "_to": edge_to})
                print('Added Relation ' + cat_id + ' : ' + coin)
            except:
                pass

    # Traverse the graph in outbound direction, breadth-first.
    result = graph.traverse(
        start_vertex="coins/1",
        direction="outbound",
        strategy="breadthfirst"
    )

    print(result)

graph_name="CryptoWandGraph"
build_cryptowand_graph (graph_name,data_c_dict)
print("Built  " + graph_name + " Successfully")

