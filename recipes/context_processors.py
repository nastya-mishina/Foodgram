from .models import Tag


def all_tags(request):
    all_tags = Tag.objects.all()
    return {'all_tags': all_tags}
