from typing import Optional
from pydantic import BaseModel

class SRoom(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: Optional[str]
    services: list[str]
    price: int
    quantity: int
    image_id: int

class SRoomInfo(SRoom):
    total_coast: int
    rooms_left: int



