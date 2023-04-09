from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView

from account.forms import *
from account.utils import SideBarMixin


class MyBook(LoginRequiredMixin, ListView, SideBarMixin):
    model = UserBookList
    template_name = 'account/my_book.html'
    context_object_name = 'favorites'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'My Book'
        context['to_read'] = UserBookList.objects.select_related('book').filter(user=self.request.user.id,
                                                                                status__status_name='To read')[:4]
        context['have_read'] = UserBookList.objects.select_related('book').filter(user=self.request.user.id,
                                                                                  status__status_name='Have read')[:4]
        context['reading_now'] = UserBookList.objects.select_related('book').filter(user=self.request.user.id,
                                                                                    status__status_name='Reading now')[
                                 :4]
        context = self.add_side_bar_context(context)
        return context

    def get_queryset(self):
        return UserBookList.objects.select_related('book').filter(user=self.request.user.id, favorites=True)[:4]


class FavoritesBookView(LoginRequiredMixin, ListView, SideBarMixin):
    model = UserBookList
    template_name = 'account/sorted_book.html'
    context_object_name = 'sorted_book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Favorites'
        context = self.add_side_bar_context(context)
        return context

    def get_queryset(self):
        return UserBookList.objects.select_related('book').filter(user=self.request.user.id, favorites=True)


class SortedByStatusBookView(LoginRequiredMixin, ListView, SideBarMixin):
    model = UserBookList
    template_name = 'account/sorted_book.html'
    context_object_name = 'sorted_book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bs = BookStatus.objects.get(slug=self.kwargs['status_slug'])
        context['title'] = str(bs.status_name)
        context['status_selected'] = bs.pk
        context = self.add_side_bar_context(context)
        return context

    def get_queryset(self):
        return UserBookList.objects.filter(status__slug=self.kwargs['status_slug'],
                                           user=self.request.user.id).select_related('book')


@login_required
def add_book(request):
    """View for create Book model and UserBookList model"""
    book_form = BookForm()
    user_book_list_form = BookListForm()
    if request.method == "POST":
        book_form = BookForm(request.POST)
        user_book_list_form = BookListForm(request.POST)
        if book_form.is_valid() and user_book_list_form.is_valid():
            b_form = book_form.save()
            list_form = user_book_list_form.save(commit=False)
            list_form.book = b_form
            list_form.user = request.user
            list_form.save()
            user_book_list_form.save_m2m()
            return redirect("home")
    context = {'book_form': book_form, 'user_book_list_form': user_book_list_form,
               'side_bar': BookStatus.objects.annotate(Count('userbooklist')),
               'title': 'Add book'}
    return render(request, 'account/addbook.html', context)


class BookView(LoginRequiredMixin, DetailView, SideBarMixin):
    model = UserBookList
    template_name = 'account/book.html'
    context_object_name = 'user_book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.add_side_bar_context(context)
        context['title'] = context['user_book'].book
        return context

    def get_object(self, queryset=None):
        slug = self.kwargs['book_slug']
        obj = UserBookList.objects.get(book__slug=slug)
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != self.request.user:
            return redirect('add_book')
        return super().get(request, *args, **kwargs)


class DeleteBookView(LoginRequiredMixin, DeleteView, SideBarMixin):
    model = Book
    context_object_name = 'book'
    success_url = reverse_lazy('home')
    template_name = 'account/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete'
        context = self.add_side_bar_context(context)
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_list = UserBookList.objects.get(book=self.object)
        if user_list.user != self.request.user:
            return redirect('add_book')
        return super().get(request, *args, **kwargs)


@login_required
def update_book(request, slug: str):
    """View for updating Book model and UserBookList model"""
    book = Book.objects.get(slug=slug)
    user_list = UserBookList.objects.get(book=book.id)
    if user_list.user != request.user:
        return redirect('add_book')
    user_book_list_form = BookListForm(instance=user_list)
    book_form = BookForm(instance=book)
    if request.method == "POST":
        book_form = BookForm(request.POST, instance=book)
        user_book_list_form = BookListForm(request.POST, instance=user_list)
        print(user_book_list_form)
        if book_form.is_valid() and user_book_list_form.is_valid():
            book_form.save()
            user_book_list_form.save()
            return HttpResponseRedirect(book.get_absolute_url())
    context = {'book_form': book_form, 'user_book_list_form': user_book_list_form,
               'side_bar': BookStatus.objects.annotate(Count('userbooklist')), 'title': book}
    return render(request, 'account/addbook.html', context)
