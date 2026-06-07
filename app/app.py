from fastapi import FastAPI , HTTPException
from app.schemas import CreatePost,PostResponse
from app.db_conn import Post , create_db_and_tables , get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app : FastAPI):
    await create_db_and_tables()
    yield
    
app = FastAPI(lifespan = lifespan)

@app.get("/posts")
def get_all_post(limit : int = None) -> list[PostResponse]:
    if limit and limit > len(text_posts) :
        raise HTTPException(status_code=500,detail=f"limit greater than the no of post !, give limit below {len(text_posts)}")
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts

@app.get("/post/{id}")
def get_post_by_id(id:int) -> PostResponse:
    if id not in text_posts :
        raise HTTPException(status_code=404,detail="post not found!")
    return text_posts.get(id)


@app.post("/post")
def create_post(post : CreatePost) -> PostResponse:
    new_index = len(text_posts)+1
    new_post = {   
        "title":post.title   ,
        "content":post.content
    }
    text_posts[new_index]=new_post
    return new_post


