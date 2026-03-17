from fastapi import APIRouter, HTTPException
from models.post import PostCreate, Comment
from repositories import mongo_repo

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/")
def create_post(post: PostCreate):
    user = mongo_repo.get_user_by_id(post.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return mongo_repo.create_post(post.user_id, post.content, post.hashtags)

@router.get("/")
def get_all_posts():
    return mongo_repo.get_all_posts()

@router.get("/{post_id}")
def get_post(post_id: str):
    post = mongo_repo.get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.get("/user/{user_id}")
def get_posts_by_user(user_id: str):
    return mongo_repo.get_posts_by_user(user_id)

@router.get("/hashtag/{hashtag}")
def get_posts_by_hashtag(hashtag: str):
    return mongo_repo.get_posts_by_hashtag(hashtag)

@router.post("/{post_id}/comments")
def add_comment(post_id: str, comment: Comment):
    success = mongo_repo.add_comment(post_id, comment.user_id, comment.text)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Comment added"}

@router.delete("/{post_id}")
def delete_post(post_id: str):
    deleted = mongo_repo.delete_post(post_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted"}