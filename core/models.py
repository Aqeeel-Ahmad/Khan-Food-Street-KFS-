from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=50, default="fa-utensils", help_text="FontAwesome or Lucide icon class e.g. fa-pizza-slice, fa-burger, fa-cocktail")
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    spicy_level = models.IntegerField(default=1, choices=[(1, 'Mild'), (2, 'Medium'), (3, 'Hot'), (4, 'Extra Hot')])
    flavor_tags = models.CharField(max_length=200, default="Street Style, Chef Special", help_text="Comma-separated flavor tags e.g. Spicy, Cheese Loaded, Crunchy")
    has_size_options = models.BooleanField(default=False, help_text="Enable Small / Medium / Large & Crust options for Pizzas")

    class Meta:
        ordering = ['-is_featured', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - Rs {self.price}"


class Deal(models.Model):
    title = models.CharField(max_length=150) # e.g. Friends Deal, Family Deal, Lover Deal
    tagline = models.CharField(max_length=200, help_text="e.g. Best Combo for 3 Friends!")
    items_included = models.TextField(help_text="Bullet points or summary of included items")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    original_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to="deals/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=True)

    class Meta:
        ordering = ['price']

    def __str__(self):
        return f"{self.title} - Rs {self.price}"


class SpecialOffer(models.Model):
    DAYS_OF_WEEK = [
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
        ('Everyday', 'Everyday'),
    ]

    title = models.CharField(max_length=200, default="Friday Special: Authentic Kabuli Pulao")
    day_of_week = models.CharField(max_length=50, choices=DAYS_OF_WEEK, default='Friday')
    description = models.TextField(default="Slow-cooked tender beef with aromatic rice, sweet raisins, and roasted almonds. Prepared fresh every Friday!")
    price = models.DecimalField(max_digits=8, decimal_places=2, default=799.00)
    original_price = models.DecimalField(max_digits=8, decimal_places=2, default=999.00)
    banner_image = models.ImageField(upload_to="specials/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    countdown_hours = models.IntegerField(default=12, help_text="Countdown hours for special offer badge")

    def __str__(self):
        return f"{self.title} ({self.day_of_week})"


class GalleryImage(models.Model):
    title = models.CharField(max_length=150)
    category = models.CharField(max_length=50, choices=[('Food', 'Food'), ('Atmosphere', 'Atmosphere'), ('Kitchen', 'Kitchen Prep')], default='Food')
    image = models.ImageField(upload_to="gallery/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    subject = models.CharField(max_length=200, blank=True, default="General Inquiry")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} - {self.phone}"
