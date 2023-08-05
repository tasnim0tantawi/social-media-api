from fastapi import FastAPI
from . import models
from . database import engine
from . routers import post, user, authentication, reaction


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# The function root gets called when the user visits the root of the API.
@app.get("/")
def root():
    return {"message": "Hi Tasnim!"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(reaction.router)



