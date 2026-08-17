from django.contrib import admin
from django.utils.html import mark_safe
from .models import Category, Product, Deal, SpecialOffer, GalleryImage, ContactMessage

# Custom Admin Site Branding
admin.site.site_header = "KFS Management Portal"
admin.site.site_title = "KFS Admin Portal"
admin.site.index_title = "Welcome to Khan Food Street Management Dashboard"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon', 'order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    ordering = ('order', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'category', 'price', 'spicy_level', 'is_available', 'is_featured')
    list_filter = ('category', 'is_available', 'is_featured', 'spicy_level')
    search_fields = ('name', 'description', 'flavor_tags')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'is_available', 'is_featured')
    list_per_page = 15

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 8px; border: 2px solid #F5A623;" />')
        return mark_safe('<span style="color: #888;">No Image</span>')
    image_preview.short_description = 'Preview'


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'title', 'price', 'original_price', 'is_active', 'is_featured')
    list_filter = ('is_active', 'is_featured')
    search_fields = ('title', 'tagline', 'items_included')
    list_editable = ('price', 'is_active', 'is_featured')

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="width: 60px; height: 40px; object-fit: cover; border-radius: 6px; border: 2px solid #D32F2F;" />')
        return mark_safe('<span style="color: #888;">No Image</span>')
    image_preview.short_description = 'Preview'


@admin.register(SpecialOffer)
class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'title', 'day_of_week', 'price', 'original_price', 'is_active')
    list_filter = ('day_of_week', 'is_active')
    search_fields = ('title', 'description')
    list_editable = ('price', 'is_active')

    def image_preview(self, obj):
        if obj.banner_image:
            return mark_safe(f'<img src="{obj.banner_image.url}" style="width: 70px; height: 45px; object-fit: cover; border-radius: 6px; border: 2px solid #F5A623;" />')
        return mark_safe('<span style="color: #888;">No Image</span>')
    image_preview.short_description = 'Banner Preview'


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'title', 'category', 'uploaded_at')
    list_filter = ('category', 'uploaded_at')
    search_fields = ('title',)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 6px;" />')
        return mark_safe('<span style="color: #888;">No Image</span>')
    image_preview.short_description = 'Thumbnail'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'phone', 'subject', 'message')
    readonly_fields = ('created_at',)
    list_editable = ('is_read',)
