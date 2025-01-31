from pydantic import BaseModel

class SHotelsInfo(BaseModel):
    rooms_left: int

class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: list[str]
    rooms_quantity: int
    image_id: int