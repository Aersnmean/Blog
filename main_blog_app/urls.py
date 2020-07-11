from django.urls import path
from .views import *

app_name = 'blog'
urlpatterns = [
    path('', index),
    path('page/<str:page_name>/', render_page, name='page'),
    path('reg/', Register.as_view()),
    path('log/', Login.as_view()),
    path('logout/', logout),
]
