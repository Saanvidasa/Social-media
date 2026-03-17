from fastapi import FastAPI
from api.routes import users, posts, engagement, analytics

app = FastAPI(
    title="Social Media Analytics Platform",
    description="Multi-database social media platform using MongoDB, Cassandra, and Neo4j",
    version="1.0.0"
)

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(engagement.router)
app.include_router(analytics.router)

@app.get("/")
def root():
    return {"message": "Social Media Analytics API is running!"}