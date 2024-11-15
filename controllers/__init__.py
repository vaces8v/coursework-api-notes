from .ping import router as ping_router
from .user import router as user_router
from .tag import router as tag_router
from .note import router as note_router

routers = [ping_router, user_router, tag_router, note_router]