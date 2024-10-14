# CRUD operations using fastapi

# Import statements 

```python
    import uvicorn
    from fastapi import FastAPI,HTTPException,status,Query,Response
    from fastapi.params import Body
    from pydantic import BaseModel
    from typing import Optional
    from random import randrange
```

# Post Details or table 

```python
    # to valid the post details
    class Post(BaseModel):
        title : str
        content : str
        published:bool = True
        rating:Optional[int] = None
```
# Array of data to perform CRUD operations

```python
    # array of data for CRUD operations
    my_list = [
        {"title":"title of post 1","content":"content for post 1","id":1},
        {"title":"title of post 2","content":"content for post 2","id":2},
        {"title":"title of post 3","content":"content for post 3","id":3}
    ]
```

# Retreving all the post

```python
    # to retrieve all the posts from the array 
    @app.get("/posts")
    def get_all_posts():
        return {"data":my_list}
```

# Creating a post

```python
    # to create a post
    @app.post("/posts")
    def create_post(post:Post):
        post_dict = post.dict()
        post_dict["id"] = randrange(1,10000)
        my_list.append(post_dict)
        return {"data":post_dict}
```

# To get the latest
```python
    # to get the latest post
    @app.get("/posts/latest")
    def get_latest_post():
        post = my_list[-1]
        return {"data":post}
```
# Helper function to find the post exist or not

```python
    # below function helps to find the post with the given id exist or not 
    def find_post(id):
        for p in my_list:
            if p["id"] == id:
                return p
```

# To get the single post data

```python
    # to get the post by id
    @app.get("/posts/{id}")
    def get_post_by_id(id:int):
        post = find_post(id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with ID {id} not found")
        return {"post_detail":post}
```

# Helper function to find the index of post by given id 

```python
    # finding the index of the post for given id
    def find_index_post(id):
        for i,p in enumerate(my_list):
            if p["id"] == id:
                return i
```

# To delete the post by id

```python
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
```

# To update the post using Put

```python
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
```

# Command to run the server

```python
    if __name__ == "__main__":
        uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)
```


[Code File](./main.py)
