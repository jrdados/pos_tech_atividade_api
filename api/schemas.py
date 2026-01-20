from pydantic import BaseModel

class Book(BaseModel):
    title: str
    price: float
    rating: int
    availability: str
    category: str
    image_url: str
    book_url: str