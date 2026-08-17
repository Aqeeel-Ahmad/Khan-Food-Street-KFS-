from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Category, Product, Deal, SpecialOffer, GalleryImage, ContactMessage
from .forms import ContactForm

def home_view(request):
    special_offer = SpecialOffer.objects.filter(is_active=True).first()
    featured_deals = Deal.objects.filter(is_active=True)[:4]
    featured_products = Product.objects.filter(is_available=True, is_featured=True)[:6]
    categories = Category.objects.all()
    gallery_preview = GalleryImage.objects.all()[:6]

    context = {
        'special_offer': special_offer,
        'featured_deals': featured_deals,
        'featured_products': featured_products,
        'categories': categories,
        'gallery_preview': gallery_preview,
        'whatsapp_number': '923442041131',
        'display_phone': '0344 2041131',
    }
    return render(request, 'core/index.html', context)


def menu_view(request):
    categories = Category.objects.prefetch_related('products').all()
    selected_category = request.GET.get('category', 'all')
    
    if selected_category != 'all':
        products = Product.objects.filter(category__slug=selected_category, is_available=True)
    else:
        products = Product.objects.filter(is_available=True)

    context = {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
        'whatsapp_number': '923442041131',
    }
    return render(request, 'core/menu.html', context)


def deals_view(request):
    deals = Deal.objects.filter(is_active=True)
    context = {
        'deals': deals,
        'whatsapp_number': '923442041131',
    }
    return render(request, 'core/deals.html', context)


def gallery_view(request):
    images = GalleryImage.objects.all()
    context = {
        'images': images,
    }
    return render(request, 'core/gallery.html', context)


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': 'Thank you! Your message has been sent to KFS team.'})
            messages.success(request, 'Thank you! Your message has been sent to Khan Food Street team.')
            return redirect('contact')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors})
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = ContactForm()

    context = {
        'form': form,
        'whatsapp_number': '923442041131',
        'display_phone': '0344 2041131',
    }
    return render(request, 'core/contact.html', context)
