from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.user import UserCreate
from repositories import mongo_repo, neo4j_repo

router = APIRouter(prefix="/users", tags=["Users"])

class FollowAction(BaseModel):
    follower_id: str
    followee_id: str

@router.post("/")
def create_user(user: UserCreate):
    existing = mongo_repo.get_user_by_username(user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = mongo_repo.create_user(user.username, user.email, user.bio)
    neo4j_repo.create_user_node(new_user["user_id"], new_user["username"])
    return new_user

@router.get("/")
def get_all_users():
    return mongo_repo.get_all_users()

@router.get("/{user_id}")
def get_user(user_id: str):
    user = mongo_repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}")
def update_user(user_id: str, updates: dict):
    updated = mongo_repo.update_user(user_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated successfully"}

@router.delete("/{user_id}")
def delete_user(user_id: str):
    deleted = mongo_repo.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}

@router.post("/follow")
def follow_user(action: FollowAction):
    neo4j_repo.follow_user(action.follower_id, action.followee_id)
    return {"message": f"{action.follower_id} now follows {action.followee_id}"}

@router.post("/unfollow")
def unfollow_user(action: FollowAction):
    neo4j_repo.unfollow_user(action.follower_id, action.followee_id)
    return {"message": f"{action.follower_id} unfollowed {action.followee_id}"}