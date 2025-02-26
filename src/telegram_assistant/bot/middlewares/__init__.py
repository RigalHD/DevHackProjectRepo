from .perms_check_middleware import router as permissions_router
from .register_check_middleware import router as register_router

routers = (register_router, permissions_router)
