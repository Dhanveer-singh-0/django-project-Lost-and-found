from django.shortcuts import render, redirect
from .models import Item, ItemImage
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def items_by_type(request, item_type):

    items = Item.objects.filter(item_type=item_type).order_by("-created_at")
    context = {
        "items": items,
        "item_type": item_type,

    }
    return render(request, "items/items_list.html", context)


@login_required(login_url='login')
def lost_view(request):
    items = Item.objects.filter(item_type='lost').order_by("-created_at")
    context = {
        "items": items,
        "item_type": 'lost',
        "active_page": 'lost'
    }
    return render(request, "items/lost_or_found.html", context)


@login_required(login_url='login')
def found_view(request):
    items = Item.objects.filter(item_type='found').order_by("-created_at")
    context = {
        "items": items,
        "item_type": 'found',
        "active_page": 'found'
    }
    return render(request, "items/lost_or_found.html", context)


@login_required(login_url='login')
def upload_item(request):
    user_id = request.user.user_id
    item=Item.objects.create(
        user_id=request.user.user_id,
        title=request.POST.get('title'),
        description=request.POST.get('description'),
        category=request.POST.get('category'),
        location=request.POST.get('location'),
        city=request.POST.get('city'),
        state=request.POST.get('state'),
        item_type=request.POST.get('item_type'),
    )
    image = request.FILES.get('image')
    if image:
        ItemImage.objects.create(item=item, image=image)
        
    if request.POST.get('item_type') == 'found':
        return redirect('found_items')
    return redirect('lost_items')


@login_required(login_url='login')
def history_view(request):
    user_id = request.user.user_id
    # items=Item.objects.filter(user_id=user_id)

    filter_type = request.GET.get("filter")  # no default now

    items = None

    if filter_type:
        items = Item.objects.filter(user=request.user)

    if filter_type == "pending":
        items = items.filter(status="pending")
    elif filter_type == "resolved":
        items = items.filter(status="settled")

    context = {
            "items": items,
            "filter_type": filter_type,
            "total_count": Item.objects.filter(user=request.user).count(),
            "pending_count": Item.objects.filter(user=request.user, status="pending").count(),
            "resolved_count": Item.objects.filter(user=request.user, status="settled").count(),
            "active_page" : 'history'
        }       
    return render(request, 'items/history.html',context)


@login_required(login_url='login')
def my_posts(request):
    

    return redirect('my_posts')


