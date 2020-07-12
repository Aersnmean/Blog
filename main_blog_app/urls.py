from django.urls import path
from .views import *

app_name = 'blog'
urlpatterns = [
    path('', index),
    path('page/<str:page_name>/', render_page, name='page'),
    path('log/', Login.as_view()),
    path('validate_tel/', ValidateTel.as_view()),
    path('reg/', Register.as_view()),
    path('logout/', logout, name='logout'),
]
