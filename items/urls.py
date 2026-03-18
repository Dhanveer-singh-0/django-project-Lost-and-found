from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from .views import lost_view,found_view,upload_item,my_posts,history_view

urlpatterns = [
    path("lost/", lost_view, name="lost_items"),
    path("found/", found_view, name="found_items"),
    path("upload_item/", upload_item, name="upload_item"),
    path("history/", history_view, name="history"),
    path("history/my-posts", my_posts, name="my_posts"),



]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)