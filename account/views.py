from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.views.generic import ListView

from account.models import *
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


class FavoritesBook(LoginRequiredMixin, ListView, SideBarMixin):
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


class SortedByStatusBook(LoginRequiredMixin, ListView, SideBarMixin):
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
        return UserBookList.objects.filter(status__slug=self.kwargs['status_slug']).select_related('book')
