from datetime import date
from typing import Optional
from fastapi import APIRouter
from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotelsInfo, SHotel

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels and Rooms"]
)

@router.get("/{location}")
async def get_hotels(location: str, date_from: date, date_to: date) -> list[SHotelsInfo]:
    return await HotelsDAO.find_all(location, date_from, date_to)

@router.get("/{hotel_id}")
async def get_hotel_by_id(hotel_id: int) -> Optional[SHotel]:
    return await HotelsDAO.find_by_id(hotel_id)
