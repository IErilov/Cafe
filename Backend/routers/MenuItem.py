from fastapi import APIRouter
from models.menu import MenuItem
from sqlalchemy import select 
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db

app = APIRouter(prefix="/menu/item", tags="item")

@app.post("/ctreate")
async def create_menu_item(title:str, order:str, category_id:int, db: AsyncSession = Depends(get_db)):
    Item = MenuItem(title=title, order=order, category_id=category_id)
    db.add(Item)
    await db.commit()
    await db.refresh(Item)

@app.delete("/delete/{id}")
async def delete_menu_item_by_id(id:int, db: AsyncSession = Depends(get_db)):
    query = select(MenuItem).where(MenuItem.id == id)
    result = await db.execute(query)
    found_item = result.scalars().first()
            
    if not id:
        raise HTTPException(status_code=404, detail="не найдено")
    
    await db.delete(found_item)
    await db.commit()