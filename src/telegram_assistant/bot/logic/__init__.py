from .callbacks import routers as callbacks_routers
from .commands import routers as commands_routers

logic_routers = (*callbacks_routers, *commands_routers)
