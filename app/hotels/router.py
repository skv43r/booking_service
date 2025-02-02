import asyncio
from datetime import date
from typing import Optional
from fastapi import APIRouter
from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotelsInfo, SHotel
from fastapi_cache.decorator import cache

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels and Rooms"]
)

@router.get("/{location}")
@cache(expire=30)
async def get_hotels(location: str, date_from: date, date_to: date) -> list[SHotelsInfo]:
    await asyncio.sleep(3)
    return await HotelsDAO.find_all(location, date_from, date_to)

@router.get("/{hotel_id}")
async def get_hotel_by_id(hotel_id: int) -> Optional[SHotel]:
    return await HotelsDAO.find_by_id(hotel_id)
