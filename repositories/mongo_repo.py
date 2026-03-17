from config.database import users_collection, posts_collection
from datetime import datetime
import uuid

# ─────────────────────────────────────────────
# Utility: Remove MongoDB _id field
# ─────────────────────────────────────────────
def clean(doc):
    if doc and "_id" in doc:
        doc.pop("_id")
    return doc


# ─────────────────────────────────────────────
# USER OPERATIONS
# ─────────────────────────────────────────────

def create_user(username: str, email: str, bio: str = "") -> dict:
    user = {
        "user_id": str(uuid.uuid4()),
        "username": username,
        "email": email,
        "bio": bio,
        "created_at": datetime.utcnow()
    }

    users_collection.insert_one(user)
    return clean(user)


def get_user_by_id(user_id: str) -> dict:
    return users_collection.find_one({"user_id": user_id}, {"_id": 0})


def get_user_by_username(username: str) -> dict:
    return users_collection.find_one({"username": username}, {"_id": 0})


def get_all_users() -> list:
    return list(users_collection.find({}, {"_id": 0}))


def update_user(user_id: str, updates: dict) -> bool:
    result = users_collection.update_one(
        {"user_id": user_id},
        {"$set": updates}
    )
    return result.modified_count > 0


def delete_user(user_id: str) -> bool:
    result = users_collection.delete_one({"user_id": user_id})
    return result.deleted_count > 0


# ─────────────────────────────────────────────
# POST OPERATIONS
# ─────────────────────────────────────────────

def create_post(user_id: str, content: str, hashtags=None) -> dict:
    if hashtags is None:
        hashtags = []

    post = {
        "post_id": str(uuid.uuid4()),
        "user_id": user_id,
        "content": content,
        "hashtags": hashtags,
        "comments": [],
        "created_at": datetime.utcnow()
    }

    posts_collection.insert_one(post)
    return clean(post)


def get_post_by_id(post_id: str) -> dict:
    return posts_collection.find_one({"post_id": post_id}, {"_id": 0})


def get_posts_by_user(user_id: str) -> list:
    return list(posts_collection.find({"user_id": user_id}, {"_id": 0}))


def get_all_posts() -> list:
    return list(posts_collection.find({}, {"_id": 0}))


def add_comment(post_id: str, user_id: str, text: str) -> bool:
    comment = {
        "user_id": user_id,
        "text": text,
        "created_at": datetime.utcnow()
    }

    result = posts_collection.update_one(
        {"post_id": post_id},
        {"$push": {"comments": comment}}
    )

    return result.modified_count > 0


def get_posts_by_hashtag(hashtag: str) -> list:
    return list(posts_collection.find({"hashtags": hashtag}, {"_id": 0}))


def delete_post(post_id: str) -> bool:
    result = posts_collection.delete_one({"post_id": post_id})
    return result.deleted_count > 0