import os

import django
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

application = ProtocolTypeRouter({
  "https": AsgiHandler(),
"websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
  # Just HTTP for now. (We can add other protocols later.)
})