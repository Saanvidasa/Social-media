from config.database import cassandra_session
from datetime import datetime
import uuid

def record_engagement(post_id: str, user_id: str, action_type: str):
    cassandra_session.execute("""
        INSERT INTO engagement_events (post_id, created_at, action_type, user_id)
        VALUES (%s, %s, %s, %s)
    """, (post_id, datetime.utcnow(), action_type, user_id))

    cassandra_session.execute(f"""
        UPDATE engagement_counts SET {action_type}s = {action_type}s + 1
        WHERE post_id = %s
    """, (post_id,))

def get_engagement_counts(post_id: str) -> dict:
    row = cassandra_session.execute("""
        SELECT likes, shares, views FROM engagement_counts WHERE post_id = %s
    """, (post_id,)).one()

    if not row:
        return {"post_id": post_id, "likes": 0, "shares": 0, "views": 0}

    return {
        "post_id": post_id,
        "likes": row.likes or 0,
        "shares": row.shares or 0,
        "views": row.views or 0
    }

def get_engagement_events(post_id: str) -> list:
    rows = cassandra_session.execute("""
        SELECT post_id, created_at, action_type, user_id
        FROM engagement_events WHERE post_id = %s
    """, (post_id,))

    return [{"post_id": r.post_id, "action_type": r.action_type,
             "user_id": r.user_id, "created_at": str(r.created_at)} for r in rows]

def get_trending_posts() -> list:
    rows = cassandra_session.execute("""
        SELECT post_id, likes, shares, views FROM engagement_counts
    """)

    posts = []
    for r in rows:
        likes  = r.likes  or 0
        shares = r.shares or 0
        views  = r.views  or 0
        score  = (likes * 1) + (shares * 3) + (views * 0.1)
        posts.append({
            "post_id": r.post_id,
            "likes": likes,
            "shares": shares,
            "views": views,
            "trending_score": round(score, 2)
        })

    return sorted(posts, key=lambda x: x["trending_score"], reverse=True)