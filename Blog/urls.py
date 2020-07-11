from django.contrib import admin
from django.urls import path, include
from main_blog_app.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_blog_app.urls'))
]
