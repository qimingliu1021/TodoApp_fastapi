from fastapi import FastAPI
from .models import Base
from .database import engine
from .routers import auth, todos, admin, users

app = FastAPI()

# Only be run when "todos.db" does not exist. There is a way to enhance DB without deleting each time
Base.metadata.create_all(bind=engine)

@app.get("/healthy")
def health_check():
  return {'status': 'Healthy'}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

