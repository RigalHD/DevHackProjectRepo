from .admin_commands import router as admin_router
from .start_commands import router as start_router

routers = (start_router, admin_router)
