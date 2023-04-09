from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from account.models import BookStatus, Book, UserBookList


class MyBookTest(TestCase):
    def setUp(self):
        number_of_book = 6
        user = User.objects.create_user('testuser1', 'testuser1@test.com', '12345')
        user.save()
        for book_num in range(number_of_book):
            Book.objects.create(
                title='title %s' % book_num,
                author='author %s' % book_num,
                thumbnail='https://test.com',
                publishedDate=book_num
            )

    # Проверка редиректа если пользователь не залогинился

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, '/login/?next=/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='12345')
        response = self.client.get(reverse('home'))

        # Проверка что пользователь залогинился
        self.assertEqual(str(response.context['user']), 'testuser1')

        # Проверка ответа на запрос
        self.assertEqual(response.status_code, 200)

        # Проверка того, что мы используем правильный шаблон
        self.assertTemplateUsed(response, 'account/my_book.html')

    def test_no_user_book_in_list(self):
        login = self.client.login(username='testuser1', password='12345')
        response = self.client.get(reverse('home'))

        # Проверка, что пользователь залогинился
        self.assertEqual(str(response.context['user']), 'testuser1')

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Проверка что в шаблон передаеться Заголовок и Сайдбар
        self.assertTrue('title' in response.context)
        self.assertTrue('side_bar' in response.context)

        # Проверка что изночально нет книг в списке
        self.assertTrue('to_read' in response.context)
        self.assertEqual(len(response.context['to_read']), 0)
        self.assertTrue('have_read' in response.context)
        self.assertEqual(len(response.context['have_read']), 0)
        self.assertTrue('reading_now' in response.context)
        self.assertEqual(len(response.context['reading_now']), 0)
        self.assertTrue('favorites' in response.context)
        self.assertEqual(len(response.context['favorites']), 0)

    def test_have_read_book_in_list(self):
        login = self.client.login(username='testuser1', password='12345')
        response = self.client.get(reverse('home'))

        # Проверка, что пользователь залогинился
        self.assertEqual(str(response.context['user']), 'testuser1')

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        all_book = Book.objects.all()
        status = BookStatus.objects.create(
            status_name='Have read',
            slug='have_read',
        )
        user = User.objects.get(username='testuser1')
        for book in all_book:
            UserBookList.objects.create(
                user=user,
                book=book,
                status=status
            )
        response = self.client.get(reverse('home'))

        # Проверка того что книги с статусом Have read в списке и их не отображается больше 4х,
        # а также что остальные статусы пусты

        self.assertTrue('have_read' in response.context)
        self.assertEqual(len(response.context['have_read']), 4)
        self.assertTrue('favorites' in response.context)
        self.assertEqual(len(response.context['favorites']), 0)
        self.assertTrue('reading_now' in response.context)
        self.assertEqual(len(response.context['reading_now']), 0)
        self.assertTrue('to_read' in response.context)
        self.assertEqual(len(response.context['to_read']), 0)

    def test_reading_now_book_in_list(self):
        login = self.client.login(username='testuser1', password='12345')
        response = self.client.get(reverse('home'))

        # Проверка, что пользователь залогинился
        self.assertEqual(str(response.context['user']), 'testuser1')

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Проверка того что книги с статусом Have read в списке и их не отображается больше 4х,
        # а также что остальные статусы пусты

        all_book = Book.objects.all()
        status = BookStatus.objects.create(
            status_name='Reading now',
            slug='reading_now',
        )
        user = User.objects.get(username='testuser1')
        for book in all_book:
            UserBookList.objects.create(
                user=user,
                book=book,
                status=status
            )

        response = self.client.get(reverse('home'))

        # Проверка того что книги с статусом Reading now в списке и их не отображается больше 4х,
        # а также что остальные статусы пусты

        self.assertTrue('have_read' in response.context)
        self.assertEqual(len(response.context['have_read']), 0)
        self.assertTrue('favorites' in response.context)
        self.assertEqual(len(response.context['favorites']), 0)
        self.assertTrue('reading_now' in response.context)
        self.assertEqual(len(response.context['reading_now']), 4)
        self.assertTrue('to_read' in response.context)
        self.assertEqual(len(response.context['to_read']), 0)

    def test_to_read_book_in_list(self):
        login = self.client.login(username='testuser1', password='12345')
        response = self.client.get(reverse('home'))

        # Проверка, что пользователь залогинился
        self.assertEqual(str(response.context['user']), 'testuser1')

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Проверка того что книги с статусом Have read в списке и их не отображается больше 4х,
        # а также что остальные статусы пусты

        all_book = Book.objects.all()
        status = BookStatus.objects.create(
            status_name='To read',
            slug='to_read',
        )
        user = User.objects.get(username='testuser1')
        for book in all_book:
            UserBookList.objects.create(
                user=user,
                book=book,
                status=status
            )

        response = self.client.get(reverse('home'))

        # Проверка того что книги с статусом To read в списке и их не отображается больше 4х,
        # а также что остальные статусы пусты

        self.assertTrue('have_read' in response.context)
        self.assertEqual(len(response.context['have_read']), 0)
        self.assertTrue('favorites' in response.context)
        self.assertEqual(len(response.context['favorites']), 0)
        self.assertTrue('reading_now' in response.context)
        self.assertEqual(len(response.context['reading_now']), 0)
        self.assertTrue('to_read' in response.context)
        self.assertEqual(len(response.context['to_read']), 4)

    def test_to_read_book_in_list(self):
        login = self.client.login(username='testuser1', password='12345')
        response = self.client.get(reverse('home'))

        # Проверка, что пользователь залогинился
        self.assertEqual(str(response.context['user']), 'testuser1')

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Проверка того что книги с статусом Have read в списке и их не отображается больше 4х,
        # а также что остальные статусы пусты

        all_book = Book.objects.all()
        status = BookStatus.objects.create(
            status_name='To read',
            slug='to_read',
        )
        user = User.objects.get(username='testuser1')
        for book in all_book:
            UserBookList.objects.create(
                user=user,
                book=book,
                status=status,
                favorites=True,
            )

        response = self.client.get(reverse('home'))

        # Проверка того что Книги отображаются в списке Favorites и их не выдаеться больше 4х
        # , и при этом отображаются в списке со стасусом книги

        self.assertTrue('have_read' in response.context)
        self.assertEqual(len(response.context['have_read']), 0)
        self.assertTrue('favorites' in response.context)
        self.assertEqual(len(response.context['favorites']), 4)
        self.assertTrue('reading_now' in response.context)
        self.assertEqual(len(response.context['reading_now']), 0)
        self.assertTrue('to_read' in response.context)
        self.assertEqual(len(response.context['to_read']), 4)


class FavoritesBookViewTest(TestCase):
    def setUp(self):
        number_of_book = 6
        user = User.objects.create_user('testuser1', 'testuser1@test.com', '12345')
        user.save()
        for book_num in range(number_of_book):
            Book.objects.create(
                title='title %s' % book_num,
                author='author %s' % book_num,
                thumbnail='https://test.com',
                publishedDate=book_num
            )

    # Проверка редиректа если пользователь не залогинился

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('favorites'))
        self.assertRedirects(response, '/login/?next=/status/favorites')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='12345')
        response = self.client.get(reverse('favorites'))

        # Проверка что пользователь залогинился
        self.assertEqual(str(response.context['user']), 'testuser1')

        # Проверка ответа на запрос
        self.assertEqual(response.status_code, 200)

        # Проверка того, что мы используем правильный шаблон
        self.assertTemplateUsed(response, 'account/sorted_book.html')

        # Проверка что в шаблон передаеться Заголовок и Сайдбар
        self.assertTrue('title' in response.context)
        self.assertTrue('side_bar' in response.context)

    def test_favorites_book_in_list(self):
        login = self.client.login(username='testuser1', password='12345')
        response = self.client.get(reverse('favorites'))

        # Проверка, что пользователь залогинился
        self.assertEqual(str(response.context['user']), 'testuser1')

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Проверка что изночально нет книг в списке
        self.assertTrue('sorted_book' in response.context)
        self.assertEqual(len(response.context['sorted_book']), 0)

        all_book = Book.objects.all()
        status = BookStatus.objects.create(
            status_name='Have read',
            slug='have_read',
        )
        user = User.objects.get(username='testuser1')
        for book in all_book:
            UserBookList.objects.create(
                user=user,
                book=book,
                status=status,
                favorites=True
            )
        response = self.client.get(reverse('favorites'))

        # Проверка того что книги с статусом favorites в списке

        self.assertTrue('sorted_book' in response.context)
        self.assertEqual(len(response.context['sorted_book']), 6)


class SortedBookViewTest(TestCase):
    def setUp(self):
        number_of_book = 6
        self.user = User.objects.create_user('testuser1', 'testuser1@test.com', '12345')
        self.user.save()
        for book_num in range(number_of_book):
            Book.objects.create(
                title='title %s' % book_num,
                author='author %s' % book_num,
                thumbnail='https://test.com',
                publishedDate=book_num
            )
        self.status = BookStatus.objects.create(
            status_name='Have read',
            slug='have_read',
        )

    # Проверка редиректа если пользователь не залогинился
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('status', kwargs={'status_slug': self.status.slug}))
        self.assertRedirects(response, '/login/?next=/status/have_read/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='12345')
        response = self.client.get(reverse('status', kwargs={'status_slug': self.status.slug}))

        # Проверка что пользователь залогинился
        self.assertEqual(str(response.context['user']), 'testuser1')

        # Проверка ответа на запрос
        self.assertEqual(response.status_code, 200)

        # Проверка того, что мы используем правильный шаблон
        self.assertTemplateUsed(response, 'account/sorted_book.html')

        # Проверка что в шаблон передаеться Заголовок и Сайдбар
        self.assertTrue('title' in response.context)
        self.assertTrue('side_bar' in response.context)

    def test_sorted_book_in_list(self):
        login = self.client.login(username='testuser1', password='12345')
        response = self.client.get(reverse('status', kwargs={'status_slug': self.status.slug}))

        # Проверка, что пользователь залогинился
        self.assertEqual(str(response.context['user']), 'testuser1')

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Проверка что изночально нет книг в списке
        self.assertTrue('sorted_book' in response.context)
        self.assertEqual(len(response.context['sorted_book']), 0)

        all_book = Book.objects.all()

        for book in all_book:
            UserBookList.objects.create(
                user=self.user,
                book=book,
                status=self.status,
            )
        response = self.client.get(reverse('status', kwargs={'status_slug': self.status.slug}))

        # Проверка того что книги с статусом Have read в списке
        self.assertTrue('sorted_book' in response.context)
        self.assertEqual(len(response.context['sorted_book']), 6)


class AddBookViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser1', 'testuser1@test.com', '12345')
        self.user.save()
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

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('add_book'))
        self.assertRedirects(response, '/login/?next=/add_book')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='12345')
        response = self.client.get(reverse('add_book'))

        # Проверка что пользователь залогинился
        self.assertEqual(str(response.context['user']), 'testuser1')

        # Проверка ответа на запрос
        self.assertEqual(response.status_code, 200)

        # Проверка того, что мы используем правильный шаблон
        self.assertTemplateUsed(response, 'account/addbook.html')

        # Проверка что в шаблон передаеться Заголовок и Сайдбар
        self.assertTrue('title' in response.context)
        self.assertTrue('side_bar' in response.context)

    def test_add_book(self):
        title = 'title'
        author = 'author'
        thumbnail = 'https://test.com'
        publishedDate = 2012
        review = 'some text'

        login = self.client.login(username='testuser1', password='12345')
        response = self.client.post('/add_book', {'title': title,
                                                  'author': author,
                                                  'thumbnail': thumbnail,
                                                  'publishedDate': publishedDate,
                                                  'review': review,
                                                  'status': 5})
        self.assertRedirects(response, reverse('home'))
        user_list = UserBookList.objects.last()
        book = Book.objects.last()
        self.assertEqual(user_list.user, self.user)
        self.assertEqual(user_list.book, book)


class UpdateBookViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('testuser1', 'testuser1@test.com', '12345')
        self.user.save()
        self.user2 = User.objects.create_user('testuser2', 'testuser2@test.com', '12345')
        self.user2.save()
        self.book = Book.objects.create(
            title='title',
            author='author',
            thumbnail="https://test.com",
            publishedDate=2023,
        )
        self.status = BookStatus.objects.create(
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

        UserBookList.objects.create(
            user=self.user,
            book=self.book,
            status=self.status,
            review='some text',
            favorites=True,
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('update_book', kwargs={'slug': self.book.slug}))
        self.assertRedirects(response, '/login/?next=/update_book/title/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='12345')
        response = self.client.get(reverse('update_book', kwargs={'slug': self.book.slug}))

        # Проверка что пользователь залогинился
        self.assertEqual(str(response.context['user']), 'testuser1')

        # Проверка ответа на запрос
        self.assertEqual(response.status_code, 200)

        # Проверка того, что мы используем правильный шаблон
        self.assertTemplateUsed(response, 'account/addbook.html')

        # Проверка что в шаблон передаеться Заголовок и Сайдбар
        self.assertTrue('title' in response.context)
        self.assertTrue('side_bar' in response.context)

    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser2', password='12345')
        response = self.client.get(reverse('update_book', kwargs={'slug': self.book.slug}))
        self.assertEqual(response.status_code, 302)

    def test_update_book(self):
        title = 'newtitle'
        author = 'author'
        thumbnail = 'https://test.com'
        publishedDate = 2022
        review = 'new text'
        favorites = False
        login = self.client.login(username='testuser1', password='12345')
        response = self.client.post(reverse('update_book', kwargs={'slug': self.book.slug}), {'title': title,
                                                                                              'author': author,
                                                                                              'thumbnail': thumbnail,
                                                                                              'publishedDate': publishedDate,
                                                                                              'review': review,
                                                                                              'status': 33,
                                                                                              'favorites': favorites})
        self.assertEqual(response.status_code, 302)
        update_book = Book.objects.get(title='newtitle')
        update_book_list = UserBookList.objects.get(book=update_book)
        self.assertEqual(title, update_book.title)
        self.assertEqual(author, update_book.author)
        self.assertEqual(publishedDate, update_book.publishedDate)
        self.assertEqual(review, update_book_list.review)
        self.assertEqual(favorites, update_book_list.favorites)


class BookViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser1', 'testuser1@test.com', '12345')
        self.user.save()
        self.user2 = User.objects.create_user('testuser2', 'testuser2@test.com', '12345')
        self.user2.save()
        self.book = Book.objects.create(
            title='title',
            author='author',
            thumbnail="https://test.com",
            publishedDate=2023,
        )
        self.status = BookStatus.objects.create(
            status_name='To read',
            slug='to_read',
        )
        UserBookList.objects.create(
            user=self.user,
            book=self.book,
            status=self.status,
            review='some text',
            favorites=True,
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('book', kwargs={'book_slug': self.book.slug}))
        self.assertRedirects(response, '/login/?next=/book/title/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='12345')
        response = self.client.get(reverse('book', kwargs={'book_slug': self.book.slug}))

        # Проверка что пользователь залогинился
        self.assertEqual(str(response.context['user']), 'testuser1')

        # Проверка ответа на запрос
        self.assertEqual(response.status_code, 200)

        # Проверка того, что мы используем правильный шаблон
        self.assertTemplateUsed(response, 'account/book.html')

        # Проверка что в шаблон передаеться Заголовок и Сайдбар
        self.assertTrue('title' in response.context)
        self.assertTrue('side_bar' in response.context)

    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser2', password='12345')
        response = self.client.get(reverse('book', kwargs={'book_slug': self.book.slug}))
        self.assertEqual(response.status_code, 302)

    def test_book_context(self):
        login = self.client.login(username='testuser1', password='12345')
        response = self.client.get(reverse('book', kwargs={'book_slug': self.book.slug}))
        self.assertTrue('user_book' in response.context)