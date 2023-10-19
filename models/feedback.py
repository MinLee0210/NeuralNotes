from beanie import Document

class Rating(Document): 
    filename: str
    rating: str

    class Settings:
        name = 'user_rating'

class Comment(Document): 
    filename: str
    content: str
    class Settings:
        name = 'user_comment'


