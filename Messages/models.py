from pydantic import BaseModel
from typing import List, Optional

# Message output model

class MessageOutputDB( BaseModel ):
    id: int
    usr_id: int
    text: Optional[str]
    media: Optional[List[str]]
    link: Optional[str]
    likes: Optional[List[int]]

# Message input model

class MessageInput( BaseModel ):
    text: Optional[str]
    media: Optional[List[str]]
    link: Optional[str]

# Message update model

class MessageUpdate( BaseModel ):
    text: Optional[str]
    media: Optional[List[str]]
    link: Optional[str]

# Link output model

class Link(BaseModel):
    title: Optional[str]
    description: Optional[str]
    image: Optional[str]

# Message info model

class MessageInfo(BaseModel):
    id: int
    usr_id: int
    text: Optional[str]
    media: Optional[List[str]]
    link: Optional[Link]
    likes: Optional[List[int]]