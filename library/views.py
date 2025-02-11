from rest_framework import viewsets, status
from .models import Author, Book, Favorite
from .serializers import AuthorSerializer, BookSerializer, FavoriteSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination


class HundredItemsPagination(PageNumberPagination):
    page_size = 100  # Limit to 100 items per page
    page_size_query_param = 'page_size'  # Allow clients to override the page size
    max_page_size = 100  # Maximum limit of 100 items per page


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HundredItemsPagination  # Apply pagination


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'author__name']
    pagination_class = HundredItemsPagination  # Apply pagination

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def recommend(self, request):
        user = request.user
        favorites = Favorite.objects.filter(user=user).values_list('book__author_id', flat=True)

        if not favorites:
            return Response({"message": "No favorites found. Add some books to get recommendations."})

        # Find books by the same authors as the user's favorites
        recommended_books = Book.objects.filter(author_id__in=favorites).exclude(favorites__user=user)

        # Paginate the results
        page = self.paginate_queryset(recommended_books)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recommended_books, many=True)
        return Response(serializer.data)


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Use a more efficient query
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class FavoritesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.select_related('book', 'book__author').filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        book_id = request.data.get('book_id')

        # Check if the book exists
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user already has the book in favorites
        if Favorite.objects.filter(user=user, book=book).exists():
            return Response({"error": "Book already in favorites"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user has reached the maximum number of favorites
        if Favorite.objects.filter(user=user).count() >= 20:
            return Response({"error": "Maximum of 20 favorites reached"}, status=status.HTTP_400_BAD_REQUEST)

        # Add the book to favorites
        Favorite.objects.create(user=user, book=book)
        return Response({"message": "Book added to favorites"}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        book_id = kwargs.get('pk')

        # Check if the book exists in favorites
        try:
            favorite = Favorite.objects.get(user=user, book_id=book_id)
        except Favorite.DoesNotExist:
            return Response({"error": "Book not in favorites"}, status=status.HTTP_404_NOT_FOUND)

        # Remove the book from favorites
        favorite.delete()
        return Response({"message": "Book removed from favorites"}, status=status.HTTP_204_NO_CONTENT)