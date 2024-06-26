from django import template

register = template.Library()


@register.filter
def in_category(comments, post):
    return comments.filter(post=post).all()
