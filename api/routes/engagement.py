from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from repositories import cassandra_repo, mongo_repo

router = APIRouter(prefix="/engagement", tags=["Engagement"])

class EngagementAction(BaseModel):
    user_id: str
    action_type: str  # like, share, view

@router.post("/{post_id}")
def record_engagement(post_id: str, action: EngagementAction):
    if action.action_type not in ["like", "share", "view"]:
        raise HTTPException(status_code=400, detail="action_type must be like, share, or view")
    post = mongo_repo.get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    cassandra_repo.record_engagement(post_id, action.user_id, action.action_type)
    return {"message": f"{action.action_type} recorded for post {post_id}"}

@router.get("/{post_id}/counts")
def get_counts(post_id: str):
    return cassandra_repo.get_engagement_counts(post_id)

@router.get("/{post_id}/events")
def get_events(post_id: str):
    return cassandra_repo.get_engagement_events(post_id)

@router.get("/trending/posts")
def get_trending():
    return cassandra_repo.get_trending_posts()