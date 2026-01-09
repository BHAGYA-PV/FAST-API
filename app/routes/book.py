from fastapi import APIRouter, Depends, HTTPException
from uuid import uuid4
from datetime import datetime
from app.models.book import BookCreate
from app.db.mongo import books_collection
from app.core.dependencies import get_current_user
from bson import ObjectId

router = APIRouter(prefix="/books", tags=["Books"])

def serialize_doc(doc: dict) -> dict:
    """Convert MongoDB ObjectId to string for JSON serialization."""
    doc = doc.copy()
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

@router.post("/")
async def create_book(book: BookCreate, user=Depends(get_current_user)):
    data = {
        "id": str(uuid4()),
        "title": book.title,
        "author": book.author,
        "genre": book.genre,
        "user_id": user["id"],
        "created_at": datetime.utcnow()
    }
    result = await books_collection.insert_one(data)
    data["_id"] = str(result.inserted_id) 
    return data


@router.get("/")
async def list_books(genre: str | None = None):
    query = {"genre": genre} if genre else {}
    books = await books_collection.find(query).to_list(100)
    return [serialize_doc(book) for book in books]


@router.get("/{book_id}")
async def get_book(book_id: str):
    book = await books_collection.find_one({"id": book_id})
    if not book:
        raise HTTPException(status_code=404)
    return serialize_doc(book)


@router.delete("/{book_id}")
async def delete_book(book_id: str, user=Depends(get_current_user)):
    book = await books_collection.find_one({"id": book_id})
    if not book:
        raise HTTPException(status_code=404)

    if book["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not allowed")

    await books_collection.delete_one({"id": book_id})
    return {"message": "Book deleted"}
