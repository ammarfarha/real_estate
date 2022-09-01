from django import template


register = template.Library()


@register.filter('is_similar')
def is_similar(url1, url2):
    return url1.startswith(url2)
