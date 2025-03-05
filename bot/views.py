from django.shortcuts import render
from rest_framework.views import APIView
from telegram import Update


# Create your views here.

class BotAdminViewSet(viewsets.ModelViewSet):
     def get(request):
        return render(request, 'bot/index.html', {})
