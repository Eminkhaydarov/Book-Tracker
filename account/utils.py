from django.db.models import Count

from account.models import BookStatus

side_bar_menu = [
    {'status_name': 'My book', 'slug': ''},
    {'status_name': 'Favorites', 'slug': 'favorites'},

]


class SideBarMixin:

    def add_side_bar_context(self, context):
        side_bar = side_bar_menu.copy()
        status = BookStatus.objects.all()
        side_bar.extend(status)
        context['side_bar'] = side_bar
        return context

