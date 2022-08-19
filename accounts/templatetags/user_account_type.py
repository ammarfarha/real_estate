from django import template
from accounts.models import Developer, Client
from accounts.views import ClientMixin, DeveloperMixin
register = template.Library()


@register.simple_tag(name='is_developer', takes_context=True)
def is_developer(context):
    request = context['request']
    user = request.user
    return user.is_authenticated and user.is_developer()
