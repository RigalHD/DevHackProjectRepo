from .callbacks import routers as callbacks_routers
from .commands import routers as commands_routers
from .states import routers as states_routers

logic_routers = (*callbacks_routers, *states_routers, *commands_routers)
