import uvicorn
from fastapi import FastAPI,HTTPException,status,Query,Response
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
app = FastAPI()

# to valid the post details
class Post(BaseModel):
    title : str
    content : str
    published:bool = True
    rating:Optional[int] = None

# array of data for CRUD operations
my_list = [
    {"title":"title of post 1","content":"content for post 1","id":1},
    {"title":"title of post 2","content":"content for post 2","id":2},
    {"title":"title of post 3","content":"content for post 3","id":3}
]


@app.get('/')
def root():
    return {"message" : "simple api using fastapi"}


# to retrieve all the posts from the array 
@app.get("/posts")
def get_all_posts():
    return {"data":my_list}

# to create a post
@app.post("/posts")
def create_post(post:Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(1,10000)
    my_list.append(post_dict)
    return {"data":post_dict}

# to get the latest post
@app.get("/posts/latest")
def get_latest_post():
    post = my_list[-1]
    return {"data":post}

# below function helps to find the post with the given id exist or not 
def find_post(id):
    for p in my_list:
        if p["id"] == id:
            return p
# to get the post by id
@app.get("/posts/{id}")
def get_post_by_id(id:int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with ID {id} not found")
    return {"post_detail":post}


# finding the index of the post for given id
def find_index_post(id):
    for i,p in enumerate(my_list):
        if p["id"] == id:
            return i
# to delete post 
@app.delete("/posts/{id}" )
def delete_post(id:int):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="post with ID {id} is not found"
        )
    my_list.pop(index)
    return {"message":f"Post with ID {id} successfully deleted"}


# updating the post with the given id
@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with ID {id} doesn't exist")
    post_dict = post.dict()
    post_dict["id"] = id
    my_list[index] = post_dict
    return {"message":f"Post with ID {id} updated successfully"}

if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)