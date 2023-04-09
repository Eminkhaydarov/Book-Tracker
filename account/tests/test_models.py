from django.contrib.auth.models import User
from django.test import TestCase

from account.models import BookStatus, Book, UserBookList


class BookTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Book.objects.create(
            title='title',
            author='author',
            thumbnail="https://test.com",
            publishedDate=2023,
        )

    def test_title_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_title_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('title').max_length
        self.assertEquals(max_length, 255)

    def test_author_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('author').verbose_name
        self.assertEquals(field_label, 'author')

    def test_author_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('author').max_length
        self.assertEquals(max_length, 255)

    def test_thumbnail_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('thumbnail').verbose_name
        self.assertEquals(field_label, 'thumbnail')

    def test_publishedDate_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('publishedDate').verbose_name
        self.assertEquals(field_label, 'publishedDate')

    def test_slug_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, 'URL')

    def test_get_absolute_url(self):
        book = Book.objects.get(id=1)
        slug = book.slug
        self.assertEquals(book.get_absolute_url(), f'/book/{slug}/')


class BookStatusTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up object to be used by all test methods"""
        BookStatus.objects.create(
            status_name='To read',
            slug='to_read',
        )

        BookStatus.objects.create(
            status_name='Reading now',
            slug='reading_now',
        )
        BookStatus.objects.create(
            status_name='Have read',
            slug='have_read',
        )

    def test_status_name_label(self):
        book_status = BookStatus.objects.get(id=1)
        field_label = book_status._meta.get_field('status_name').verbose_name
        self.assertEquals(field_label, 'status name')

    def test_status_name_max_length(self):
        book_status = BookStatus.objects.get(id=1)
        max_length = book_status._meta.get_field('status_name').max_length
        self.assertEquals(max_length, 255)

    def test_slug_label(self):
        book_status = BookStatus.objects.get(id=1)
        field_label = book_status._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, 'URL')

    def test_slug_max_length(self):
        book_status = BookStatus.objects.get(id=1)
        max_length = book_status._meta.get_field('slug').max_length
        self.assertEquals(max_length, 255)

    def test_object_name(self):
        book_status = BookStatus.objects.get(id=1)
        self.assertEqual('To read', str(book_status))

    def test_get_absolute_url(self):
        book_status = BookStatus.objects.get(id=1)
        self.assertEquals(book_status.get_absolute_url(), '/status/to_read/')

    def test_create(self):
        '''Тест огрничения создания новых объектов модели Bookstatus'''
        BookStatus.objects.create(
            status_name='Some name',
            slug='some_slug',
        )
        book_status = BookStatus.objects.last()
        count = BookStatus.objects.count()
        self.assertEqual(count, 3)
        self.assertEqual('Have read', book_status.status_name)
        self.assertEqual('have_read', book_status.slug)


class UserBookListTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        book = Book.objects.create(
            title='title',
            author='author',
            thumbnail="https://test.com",
            publishedDate=2023,
        )
        status = BookStatus.objects.create(
            status_name='To read',
            slug='to_read',
        )
        UserBookList.objects.create(
            user=user,
            book=book,
            status=status,
            favorites=True,
            review='Some text'
        )

    def test_user_label(self):
        book_list = UserBookList.objects.get(id=1)
        field_label = book_list._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'user')

    def test_book_label(self):
        book_list = UserBookList.objects.get(id=1)
        field_label = book_list._meta.get_field('book').verbose_name
        self.assertEquals(field_label, 'book')

    def test_status_label(self):
        book_list = UserBookList.objects.get(id=1)
        field_label = book_list._meta.get_field('status').verbose_name
        self.assertEquals(field_label, 'status')

    def test_favorites_label(self):
        book_list = UserBookList.objects.get(id=1)
        field_label = book_list._meta.get_field('favorites').verbose_name
        self.assertEquals(field_label, 'favorites')

    def test_review_label(self):
        book_list = UserBookList.objects.get(id=1)
        field_label = book_list._meta.get_field('review').verbose_name
        self.assertEquals(field_label, 'review')
