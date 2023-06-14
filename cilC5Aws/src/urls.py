from django.urls import path
from .views import IndexView, DeleteBucket

app_name = "src"

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('delete/', DeleteBucket.as_view(), name='delete'),
]