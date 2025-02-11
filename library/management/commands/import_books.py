# import jsonlines
# from django.core.management.base import BaseCommand
# from library.models import Book, Author

# class Command(BaseCommand):
#     help = 'Import books and authors from a JSON file'

#     def handle(self, *args, **kwargs):
#         # Open the JSON file
#         with jsonlines.open('C:/Users/Mohamed-sidi/Downloads/books.json/books.json') as reader:
#             for book_data in reader:
#                 # Clean the num_pages field
#                 num_pages = book_data.get('num_pages')
#                 if num_pages == '' or num_pages is None:
#                     num_pages = None  # Set to None if empty or invalid
#                 else:
#                     try:
#                         num_pages = int(num_pages)  # Convert to integer
#                     except (ValueError, TypeError):
#                         num_pages = None  # Set to None if conversion fails

#                 # Create or update the book
#                 book, created = Book.objects.update_or_create(
#                     id=book_data['id'],
#                     defaults={
#                         'title': book_data['title'],
#                         'isbn': book_data.get('isbn'),
#                         'isbn13': book_data.get('isbn13'),
#                         'language': book_data.get('language'),
#                         'average_rating': book_data.get('average_rating'),
#                         'ratings_count': book_data.get('ratings_count'),
#                         'text_reviews_count': book_data.get('text_reviews_count'),
#                         'publication_date': book_data.get('publication_date'),
#                         'publisher': book_data.get('publisher'),
#                         'num_pages': num_pages,  # Use the cleaned value
#                         'image_url': book_data.get('image_url'),
#                     }
#                 )

#                 # Add authors to the book
#                 for author_data in book_data.get('authors', []):
#                     author, created = Author.objects.update_or_create(
#                         id=author_data['id'],
#                         defaults={
#                             'name': author_data['name'],
#                             'role': author_data.get('role', ''),
#                         }
#                     )
#                     book.authors.add(author)

#                 self.stdout.write(self.style.SUCCESS(f'Successfully imported book: {book.title}'))





import jsonlines
from django.core.management.base import BaseCommand
from library.models import Author

class Command(BaseCommand):
    help = 'Import authors from a JSON file'

    def handle(self, *args, **kwargs):
        # Open the JSON file
        with jsonlines.open('C:/Users/Mohamed-sidi/Downloads/authors.json') as reader:
            for author_data in reader:
                # Create or update the author
                author, created = Author.objects.update_or_create(
                    id=author_data['id'],
                    defaults={
                        'name': author_data['name'],
                        'gender': author_data.get('gender', ''),
                        'image_url': author_data.get('image_url', ''),
                        'about': author_data.get('about', ''),
                        'fans_count': author_data.get('fans_count', 0),
                        'ratings_count': author_data.get('ratings_count', 0),
                        'average_rating': author_data.get('average_rating', 0.0),
                        'text_reviews_count': author_data.get('text_reviews_count', 0),
                    }
                )

                self.stdout.write(self.style.SUCCESS(f'Successfully imported author: {author.name}'))