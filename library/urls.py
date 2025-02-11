from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, BookViewSet
from .views import RegisterView, LoginView
from .views import BookViewSet, FavoritesViewSet
router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
# router.register(r'books', BookViewSet)
router.register(r'books', BookViewSet, basename='book')
router.register(r'favorites', FavoritesViewSet, basename='favorite')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('books/recommend/', BookViewSet.as_view({'get': 'recommend'}), name='book-recommend'),
    
]
