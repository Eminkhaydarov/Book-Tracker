from django.db.models import Count

from account.models import BookStatus



class SideBarMixin:

    def add_side_bar_context(self, context):
        status = BookStatus.objects.annotate(Count('userbooklist'))
        context['side_bar'] = status
        return context

