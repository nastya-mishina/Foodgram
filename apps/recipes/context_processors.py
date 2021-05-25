def get_purchases_count(request):
    if request.user.is_authenticated:
        count = request.user.purchases.all().count()
    else:
        count = 0
    return {
        "get_purchases_count": count
    }
