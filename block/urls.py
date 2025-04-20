from django.urls import path
from .views import set_user_token,get_user_docs_by_token,check_user_token

urlpatterns = [
    path("token/user/generate/", set_user_token),
    path("user/<int:app_user_id>/documents/", get_user_docs_by_token),
    path('check-token/<int:app_user_id>/', check_user_token),
]

