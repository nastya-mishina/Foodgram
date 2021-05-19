from django import template


register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def get_tags(request):
    return request.getlist('tags')


@register.filter
def rebuild_tag_link(request, tag):
    request_copy = request.GET.copy()
    tags = request_copy.getlist('tags')
    if tag in tags:
        tags.remove(tag)
        request_copy.setlist('tags', tags)
    else:
        request_copy.appendlist('tags', tag)
    return request_copy.urlencode()
