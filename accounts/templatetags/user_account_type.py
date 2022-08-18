from django import template
from accounts.models import Developer, Client
from accounts.views import ClientMixin, DeveloperMixin
register = template.Library()


@register.simple_tag(name='user_type')
def get_type():
    if DeveloperMixin.test_func:
        return 'Developer'
    else:
        if ClientMixin.test_func:
            return 'Client'
        else:
            return 'User'
