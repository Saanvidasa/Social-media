from fastapi import APIRouter
from repositories import cassandra_repo, neo4j_repo

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/trending")
def trending_posts():
    return cassandra_repo.get_trending_posts()

@router.get("/followers/{user_id}")
def get_followers(user_id: str):
    return neo4j_repo.get_followers(user_id)

@router.get("/following/{user_id}")
def get_following(user_id: str):
    return neo4j_repo.get_following(user_id)

@router.get("/suggestions/{user_id}")
def get_suggestions(user_id: str):
    return neo4j_repo.get_suggestions(user_id)