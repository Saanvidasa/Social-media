from pymongo import MongoClient
from cassandra.cluster import Cluster
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

# MongoDB
mongo_client = MongoClient(os.getenv("MONGO_URI"))
mongo_db = mongo_client[os.getenv("MONGO_DB")]
users_collection = mongo_db["users"]
posts_collection = mongo_db["posts"]

# Cassandra
cassandra_cluster = Cluster([os.getenv("CASSANDRA_HOST", "localhost")])
cassandra_session = cassandra_cluster.connect("social_analytics")

# Neo4j
neo4j_driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
)