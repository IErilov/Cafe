from fastapi import FastAPI, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import engine, Base, get_db
from models.base import VisitLog
from network import Network
from routers.cafe import router as cafe_router 
from sqladmin import Admin
from sqladmin_inline import setup_inline_routes
from admin.auth import AdminAuth
from admin.interface import CafeAdmin, MenuCategoryAdmin, MenuItemAdmin, ComboAdmin, ComboItemAdmin, UserAdmin
import os

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-prod")

app = FastAPI(title="ACP")
network_handler = Network()

app.include_router(cafe_router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def main(request: Request, db: AsyncSession = Depends(get_db)):
    ip = await network_handler.get_ip(request)
    new_log = VisitLog(ip_address=ip)
    db.add(new_log)
    await db.commit()
    
    return {"message": f"hello {ip}", "status": "saved_to_db"}

admin = Admin(
    app, 
    engine, 
    authentication_backend=AdminAuth(secret_key=SECRET_KEY),
    title="Admin panel",
    )

setup_inline_routes(admin)
admin.add_view(CafeAdmin)
admin.add_view(MenuCategoryAdmin)
admin.add_view(MenuItemAdmin)
admin.add_view(ComboAdmin)
admin.add_view(ComboItemAdmin)
admin.add_view(UserAdmin)