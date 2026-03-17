from config.database import neo4j_driver

def create_user_node(user_id: str, username: str):
    with neo4j_driver.session() as session:
        session.run("""
            MERGE (u:User {user_id: $user_id})
            SET u.username = $username
        """, user_id=user_id, username=username)

def follow_user(follower_id: str, followee_id: str):
    with neo4j_driver.session() as session:
        session.run("""
            MATCH (a:User {user_id: $follower_id})
            MATCH (b:User {user_id: $followee_id})
            MERGE (a)-[:FOLLOWS]->(b)
        """, follower_id=follower_id, followee_id=followee_id)

def unfollow_user(follower_id: str, followee_id: str):
    with neo4j_driver.session() as session:
        session.run("""
            MATCH (a:User {user_id: $follower_id})-[r:FOLLOWS]->(b:User {user_id: $followee_id})
            DELETE r
        """, follower_id=follower_id, followee_id=followee_id)

def get_followers(user_id: str) -> list:
    with neo4j_driver.session() as session:
        result = session.run("""
            MATCH (follower:User)-[:FOLLOWS]->(u:User {user_id: $user_id})
            RETURN follower.user_id AS user_id, follower.username AS username
        """, user_id=user_id)
        return [{"user_id": r["user_id"], "username": r["username"]} for r in result]

def get_following(user_id: str) -> list:
    with neo4j_driver.session() as session:
        result = session.run("""
            MATCH (u:User {user_id: $user_id})-[:FOLLOWS]->(following:User)
            RETURN following.user_id AS user_id, following.username AS username
        """, user_id=user_id)
        return [{"user_id": r["user_id"], "username": r["username"]} for r in result]

def get_suggestions(user_id: str) -> list:
    with neo4j_driver.session() as session:
        result = session.run("""
            MATCH (u:User {user_id: $user_id})-[:FOLLOWS]->()-[:FOLLOWS]->(suggested:User)
            WHERE suggested.user_id <> $user_id
            AND NOT (u)-[:FOLLOWS]->(suggested)
            RETURN DISTINCT suggested.user_id AS user_id, suggested.username AS username
        """, user_id=user_id)
        return [{"user_id": r["user_id"], "username": r["username"]} for r in result]