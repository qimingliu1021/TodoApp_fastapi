# from typing import Annotated

# from pydantic import BaseModel, Field
# from sqlalchemy.orm import Session
# from fastapi import APIRouter, Depends, status, Path
# from fastapi.exceptions import HTTPException
# # from starlette import status

# from ..models import Todos
# from ..database import SessionLocal
# from .auth import get_current_user

# router = APIRouter()

# # Only be run when "todos.db" does not exist. There is a way to enhance DB without deleting each time
# # These two lines are no longer needed since the todos is moved from "main.py" to "/routers/todos.py"
# # models.Base.metadata.create_all(bind=engine)
# # app.include_router(auth.router)


# def get_db():
#     db = SessionLocal()
#     try:
#         # only the code prior to and include in the yield statement is executed before sending a response
#         yield db       
#     finally:
#         # will be executed after the response is delivered;
#         # The whole process: Fetch info from database, return it to the client, close the connection to database after
#         db.close()


# db_dependency = Annotated[Session, Depends(get_db)]
# user_dependency = Annotated[dict, Depends(get_current_user)]


# class TodoRequest(BaseModel): 
#     title: str = Field(min_length=3)
#     description: str = Field(min_length=3, max_length=100)
#     # gt <==> greater than
#     priority: int = Field(gt=0, lt=6)
#     complete: bool


# # db_dependency = Annotated[Session, Depends(get_db)] Dependency Injection can also be written here instead of in signature
# # Then the signature will be like: async def read_all(db: db_dependency):
# # It's an asynchronic API endpoint
# @router.get("/", status_code=status.HTTP_200_OK)
# async def read_all(user: user_dependency, db: Annotated[Session, Depends(get_db)]): # Depends - Dependency injection: do something before executing what will be executed
#     if user is None: 
#         raise HTTPException(status_code=401, detail='Authentication Failed')
#     return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()       # For example, this function depends on opening db, fetching info, then close; 


# # /{todo_id} is a path parameter
# @router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
# async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
#     if user is None: 
#         raise HTTPException(status_code=401, detail='Authentication Failed')
#     # Adding ".first()" saves times, bc the code doesn't know how many items are with "todo_id"
#     # Thus it will look through every row but actually is not necessary
#     todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
#     if todo_model is not None: 
#         return todo_model
#     raise HTTPException(status_code=404, detail='Todo not found.')


# # Create a new Todo, and save it to the database
# @router.post("/todo", status_code=status.HTTP_201_CREATED)
# async def create_todo(user: user_dependency, db: db_dependency, 
#                     todo_request: TodoRequest):
#     if user is None: 
#         raise HTTPException(status_code=401, detail='Authentication Failed')
#     # **todo_request.dict() -- conversion from dictionary key and value as parameters. But it does not have id
#     todo_model = Todos(**todo_request.dict(), owner_id=user.get('id'))

#     db.add(todo_model)
#     db.commit()


# @router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def update_todo(user: user_dependency, db: db_dependency,
#                     todo_request: TodoRequest, # NOTE: "TodoRequest" should be always above anything with "Path"
#                     todo_id: int = Path(gt=0)):
#     if user is None: 
#         raise HTTPException(status_code=401, detail='Authentication Failed')                
#     todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
#     if todo_model is None: 
#         raise HTTPException(status_code=404, detail='Todo not found.')

#     todo_model.title = todo_request.title
#     todo_model.description = todo_request.description
#     todo_model.priority = todo_request.priority
#     todo_model.complete = todo_request.complete

#     db.add(todo_model)
#     db.commit()


# @router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
#     if user is None: 
#         raise HTTPException(status_code=401, detail='Authentication Failed') 

#     todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
#     if todo_model is None: 
#         raise HTTPException(status_code=404, detail='Todo not found.')

#     db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()

#     db.commit()


from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from ..models import Todos
from ..database import SessionLocal
from .auth import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found.')


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency,
                      todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get('id'))

    db.add(todo_model)
    db.commit()


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency,
                      todo_request: TodoRequest,
                      todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()

    db.commit()


