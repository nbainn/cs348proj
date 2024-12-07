"""
URL configuration for hello_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from .views import sayHello
from . import views
urlpatterns = [
    #path('', sayHello, name='sayHello'),
    path('list/', views.list_library),
    path('insert_book/', views.insert_book_item, name='insert_book_item'),
    path('delete_book/<int:book_id>/', views.delete_book_item, name='delete_book_item'),
    path('update_book/<int:book_id>/', views.update_book_status, name='update_book_status'),
    path('filter_books_by_status/', views.filter_books_by_status, name='filter_books_by_status'),
]