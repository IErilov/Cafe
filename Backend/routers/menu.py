from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models.menu import MenuCategory, MenuItem
from sqlalchemy import select 

router = APIRouter(prefix="/menu", tags=['menu'])

@router.post("/create")
async def create_menu(name:str, slug:str, db: AsyncSession = Depends(get_db)):
    menu = MenuCategory(name=name, slug=slug)
    db.add(menu)
    await db.commit()
    await db.refresh(MenuCategory)

    return {"status": "success", "cafe": {"id": menu.id, "name": menu.name}}

@router.get("get/{name}")
async def get_cafe_by_name(name, db: AsyncSession = Depends(get_db)):
    query = select(MenuCategory).where(MenuCategory.name == name)
    result = await db.execute(query)
    menu = result.scalars().first()
    
    if not menu:
        raise HTTPException(status_code=404, detail="не найдено")
        
    return {"name": menu.name, "adress": menu.adress}

@router.get("/")
async def get_all_menu_by_cafe(cafe_id: int, db: AsyncSession = Depends(get_db)):
    query = select(MenuCategory)
    result = await db.execute(query)
    menus = result.scalars().all()
    
    return {"menus": menus}

@router.delete("/delete/{id}")
async def delete_menu_by_id(id:int, db: AsyncSession = Depends(get_db)):
    query = select(MenuCategory).where(MenuCategory.id == id)
    result = await db.execute(query)
    found_menu = result.scalars().first()
            
    if not found_menu:
        raise HTTPException(status_code=404, detail="не найдено")
    
    deleted_name = found_menu.name
    deleted_adress = found_menu.adress
    
    await db.delete(found_menu)
    await db.commit()
                
    return {"status": "deleted", "name": deleted_name, "adress": deleted_adress}