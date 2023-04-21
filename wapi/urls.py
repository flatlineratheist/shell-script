"""analytica URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path,include
from .views import *

urlpatterns = [
    # Game URL
    # #####################
    path('',indexHomePlayGame,name='indexHomePlayGame'),  # only required for API Framework
    path('winner',winner,name='winner'),  # only required for API Framework
    path('correct',correct,name='correct'),  # only required for API Framework
    path('wrong',wrong,name='wrong'),  # only required for API Framework
    path('quiz',quiz,name='quiz'),  # only required for API Framework

    # Game URL
    # #####################
    # path('indexBingo',indexBingo,name='indexBingo'),  # only required for API Framework
    # path('indexBingo2',indexBingo2,name='indexBingo2'),  # only required for API Framework
    # path('indexBingo3',indexBingo3,name='indexBingo3'),  # only required for API Framework
    # path('indexBingobingoWrong',indexBingobingoWrong,name='indexBingobingoWrong'),  # only required for API Framework
    # path('indexBingobingoCorrect',indexBingobingoCorrect,name='indexBingobingoCorrect'),  # only required for API Framework


    # Auth URL URL
    # #####################
    # path('registration',registration,name='registration'),
    path('question',redirectQuestion,name='redirectQuestion'),
    path('send_intro_msg',send_intro_msg,name='send_intro_msg'),

    


    path('send_template_message',send_template_message,name='send_template_message'),  # only required for API Framework
    path('webhook',webhook_whatsapp,name='webhook_whatsapp'),  # only required for API Framework
    
]
