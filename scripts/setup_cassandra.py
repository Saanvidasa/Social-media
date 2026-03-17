from cassandra.cluster import Cluster

def setup():
    cluster = Cluster(['localhost'])
    session = cluster.connect()

    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS social_analytics
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
    """)

    session.set_keyspace('social_analytics')

    session.execute("""
        CREATE TABLE IF NOT EXISTS engagement_events (
            post_id     TEXT,
            created_at  TIMESTAMP,
            action_type TEXT,
            user_id     TEXT,
            PRIMARY KEY (post_id, created_at)
        ) WITH CLUSTERING ORDER BY (created_at DESC)
    """)

    session.execute("""
        CREATE TABLE IF NOT EXISTS engagement_counts (
            post_id TEXT PRIMARY KEY,
            likes   COUNTER,
            shares  COUNTER,
            views   COUNTER
        )
    """)

    print("✅ Cassandra keyspace and tables created!")
    cluster.shutdown()

if __name__ == "__main__":
    setup()