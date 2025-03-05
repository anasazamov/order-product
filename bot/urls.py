from django.urls import path
from bot.views import BotAdminViewSet

urlpatterns = [
    path('', BotAdminViewSet.as_view())
]