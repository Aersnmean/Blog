from django.urls import path
from .views import *

app_name = 'blog'
urlpatterns = [
    path('', LPost.as_view(), name='index'),
    path('page/<str:page_name>/', render_page, name='page'),
    path('log/', Login.as_view()),
    path('validate_tel/', ValidateTel.as_view()),
    path('reg/', Register.as_view()),
    path('logout/', logout, name='logout'),
    path('c_post/', CPost.as_view()),
    path('single/<str:id>/', RUDPost.as_view(), name='single'),
    path('cl_review/<str:id>/', CReview.as_view()),
    # path('rud_post/', RUDPost.as_view()),
]
