from arango import ArangoClient

# Initialize the client for ArangoDB.
client = ArangoClient(hosts="http://localhost:8529")

# Connect to "test" database as root user.
db = client.db("cryptodata", username="rsenthilk", password="myPass00")

# Create a new graph named "school".
graph = db.create_graph("CryptoGraph")

# Create vertex collections for the graph.
coins = graph.create_vertex_collection("coins")
categories = graph.create_vertex_collection("categories")

# Create an edge definition (relation) for the graph.
edges = graph.create_edge_definition(
    edge_collection="isapartof",
    from_vertex_collections=["coins"],
    to_vertex_collections=["categories"]
)


# Insert vertex documents into "students" (from) vertex collection.
coins.insert({"_key": "01", "coin_slug": "tether"})
coins.insert({"_key": "02", "coin_slug": "binance usd"})
coins.insert({"_key": "03", "coin_slug": "DAI"})
coins.insert({"_key": "04", "coin_slug": "polkadot"})
coins.insert({"_key": "05", "coin_slug": "chainlink"})
coins.insert({"_key": "06", "coin_slug": "kusama"})
coins.insert({"_key": "07", "coin_slug": "theta"})
coins.insert({"_key": "08", "coin_slug": "chiliz"})
coins.insert({"_key": "09", "coin_slug": "enjin"})


# Insert vertex documents into "lectures" (to) vertex collection.
categories.insert({"_key": "stablecoins", "category-name": "stablecoins"})
categories.insert({"_key": "polkadot", "category-name": "polkadot"})
categories.insert({"_key": "solana", "category-name": "solana"})

# Insert edge documents into "register" edge collection.
edges.insert({"_from": "coins/01", "_to": "categories/stablecoins"})
edges.insert({"_from": "coins/02", "_to": "categories/stablecoins"})
edges.insert({"_from": "coins/03", "_to": "categories/stablecoins"})
edges.insert({"_from": "coins/04", "_to": "categories/polkadot"})
edges.insert({"_from": "coins/05", "_to": "categories/polkadot"})
edges.insert({"_from": "coins/06", "_to": "categories/polkadot"})
edges.insert({"_from": "coins/07", "_to": "categories/solana"})
edges.insert({"_from": "coins/08", "_to": "categories/solana"})
edges.insert({"_from": "coins/09", "_to": "categories/solana"})

# Traverse the graph in outbound direction, breadth-first.
