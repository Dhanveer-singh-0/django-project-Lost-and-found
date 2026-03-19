from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField
from django.templatetags.static import static

class Item(models.Model):

    ITEM_TYPE_CHOICES = (
        ('lost', 'Lost'),
        ('found', 'Found'),
    )
    CATEGORY_CHOICES = (
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('wallet', 'Wallet'),
        ('documents', 'Documents'),
        ('bag', 'Bag'),
        ('keys', 'Keys'),
        ('accessories', 'Accessories'),
        ('others', 'Others'),
    )
    STATUS_CHOICSE=[
        ("pending", "Pending"),
        ("settled", "Settled"),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    item_id = models.AutoField(primary_key=True)
    item_type = models.CharField(
        max_length=10,
        choices=ITEM_TYPE_CHOICES
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )
    title = models.CharField(max_length=200)
    description = models.TextField()

    location = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
    max_length=10,
    choices=STATUS_CHOICSE,
    default="pending"
)

    def __str__(self):
        return f"{self.title} ({self.item_type})"
    
    def get_image(self):
        img = self.images.first()  # since only 1 image expected

        if img and img.image:
            return img.image.url  # Cloudinary URL
        return static("images/default_item.jpg")
    

class ItemImage(models.Model):

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = CloudinaryField(
        'item_image', blank=True, null=True
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Image for {self.item.title}"