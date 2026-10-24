from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models.cafe import Cafe
from sqlalchemy import select 

router = APIRouter(prefix="/cafe", tags=["Cafes"])

@router.post("/create_cafe")
async def create_cafe(name: str, adress: str, db: AsyncSession = Depends(get_db)):
    cafe = Cafe(name=name, adress=adress)
    db.add(cafe)
    await db.commit()
    await db.refresh(cafe)

    return {"status": "success", "cafe": {"id": cafe.id, "name": cafe.name}}

@router.get("/get_cafe/{name}")
async def get_cafe_by_name(name, db: AsyncSession = Depends(get_db)):
    query = select(Cafe).where(Cafe.name == name)
    result = await db.execute(query)
    cafe = result.scalars().first()
    
    if not cafe:
        raise HTTPException(status_code=404, detail="Кафе не найдено")
        
    return {"name": cafe.name, "adress": cafe.adress}

@router.delete("/delete_cafe/{id}")
async def delete_cafe_by_id(id, db: AsyncSession = Depends(get_db)):
    query = select(Cafe).where(Cafe.id == id)
    result = await db.execute(query)
    found_cafe = result.scalars().first()
        
    if not id:
        raise HTTPException(status_code=404, detail="Кафе не найдено")

    deleted_name = found_cafe.name
    deleted_adress = found_cafe.adress

    await db.delete(found_cafe)
    await db.commit()
            
    return {"status": "deleted", "name": deleted_name, "adress": deleted_adress}