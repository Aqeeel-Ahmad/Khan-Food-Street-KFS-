from django.core.management.base import BaseCommand
from core.models import Category, Product, Deal, SpecialOffer, GalleryImage

class Command(BaseCommand):
    help = "Seed database with KFS Khan Food Street categories, products, deals, and Friday special."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting KFS Database Seeding..."))

        # Clear existing data
        Category.objects.all().delete()
        Product.objects.all().delete()
        Deal.objects.all().delete()
        SpecialOffer.objects.all().delete()
        GalleryImage.objects.all().delete()

        # 1. Categories
        cat_pizzas = Category.objects.create(name="Pizzas", icon="fa-pizza-slice", description="Artisan wood-fired & deep dish street style pizzas loaded with cheese", order=1)
        cat_burgers = Category.objects.create(name="Burgers & Shawarmas", icon="fa-burger", description="Juicy stacked beef patties & crispy zinger chicken burgers", order=2)
        cat_fries = Category.objects.create(name="Fries & Sides", icon="fa-french-fries", description="Golden crinkle cut loaded fries with liquid cheddar", order=3)
        cat_pasta = Category.objects.create(name="Pasta & Noodles", icon="fa-bowl-food", description="Creamy Alfredo, spicy red sauce penne & wok fried street noodles", order=4)
        cat_drinks = Category.objects.create(name="Beverages & Shakes", icon="fa-glass-water", description="Refreshing ice cold sodas, shakes, and signature mint margaritas", order=5)

        # 2. Products
        Product.objects.create(
            category=cat_pizzas,
            name="KFS Crown Crust Pizza",
            description="Loaded chicken tikka chunks, jalapenos, black olives, extra mozzarella, and stuffed cheese garlic crown crust.",
            price=1299.00,
            image="products/pizza_supreme.png",
            is_available=True,
            is_featured=True,
            spicy_level=2,
            flavor_tags="Cheese Loaded, Crown Crust, Chef Special",
            has_size_options=True
        )
        Product.objects.create(
            category=cat_pizzas,
            name="Street Pepperoni Feast",
            description="Double crispy beef pepperoni slices with melted aged mozzarella and spicy tomato sauce.",
            price=1199.00,
            image="products/pizza_supreme.png",
            is_available=True,
            is_featured=True,
            spicy_level=1,
            flavor_tags="Classic Pepperoni, Extra Cheese",
            has_size_options=True
        )
        Product.objects.create(
            category=cat_burgers,
            name="Monster Zinger Burger",
            description="Double crisp fried chicken breast fillets with liquid melted cheddar, spicy mayonnaise, and pickled jalapenos.",
            price=699.00,
            image="products/burger_zinger.png",
            is_available=True,
            is_featured=True,
            spicy_level=3,
            flavor_tags="Extra Spicy, Double Patty, Crunchy",
            has_size_options=False
        )
        Product.objects.create(
            category=cat_burgers,
            name="Smokey Beef Charcoal Burger",
            description="100% pure beef patty grilled over charcoal coals topped with caramelized onions and smokey barbecue sauce.",
            price=749.00,
            image="products/burger_zinger.png",
            is_available=True,
            is_featured=True,
            spicy_level=2,
            flavor_tags="Charcoal Grilled, Smoky BBQ",
            has_size_options=False
        )
        Product.objects.create(
            category=cat_fries,
            name="KFS Loaded Cheesy Fries",
            description="Bucket of crispy golden french fries topped with hot liquid cheddar, chicken chunks, and secret spice blend.",
            price=449.00,
            image="products/burger_zinger.png",
            is_available=True,
            is_featured=False,
            spicy_level=2,
            flavor_tags="Cheese Lava, Crispy",
            has_size_options=False
        )
        Product.objects.create(
            category=cat_pasta,
            name="Creamy Chicken Alfredo Pasta",
            description="Penne pasta tossed in rich white garlic cream sauce, grilled herb chicken strips, and parmesan.",
            price=799.00,
            image="products/pizza_supreme.png",
            is_available=True,
            is_featured=False,
            spicy_level=1,
            flavor_tags="Creamy White Sauce, Grilled Chicken",
            has_size_options=False
        )
        Product.objects.create(
            category=cat_drinks,
            name="Electric Blue Mint Margarita",
            description="Crushed ice blended with fresh mint leaves, lime juice, sprite, and blue curacao syrup.",
            price=299.00,
            image="products/burger_zinger.png",
            is_available=True,
            is_featured=False,
            spicy_level=1,
            flavor_tags="Refreshing, Ice Cold",
            has_size_options=False
        )

        # 3. Deals (Friends Deal, Family Deal, Lover Deal)
        Deal.objects.create(
            title="Friends Deal",
            tagline="Perfect street combo for 3 Best Friends!",
            items_included="2 Medium Pizzas (Any Flavor) + 2 Zinger Burgers + 1 Large Cheesy Fries + 1.5L Soft Drink",
            price=1399.00,
            original_price=1799.00,
            image="deals/friends_deal.png",
            is_active=True,
            is_featured=True
        )
        Deal.objects.create(
            title="Family Deal",
            tagline="Ultimate Feast for the Whole Squad & Family!",
            items_included="2 Large Crown Crust Pizzas + 4 Zinger Burgers + Bucket Loaded Fries + 6 Garlicky Rolls + 2.25L Soft Drink",
            price=2599.00,
            original_price=3299.00,
            image="deals/family_deal.png",
            is_active=True,
            is_featured=True
        )
        Deal.objects.create(
            title="Lover Deal",
            tagline="Romantic Street Food Date Special for Two!",
            items_included="1 Large Heart-Shape Pizza + 2 Double Beef Burgers + Molten Chocolate Lava Cake + 2 Mint Margaritas",
            price=1399.00,
            original_price=1699.00,
            image="deals/lover_deal.png",
            is_active=True,
            is_featured=True
        )

        # 4. Special Offer (Friday Special: Authentic Kabuli Pulao)
        SpecialOffer.objects.create(
            title="Friday Special: Authentic Kabuli Pulao",
            day_of_week="Friday",
            description="Slow-cooked tender beef shank cooked with aromatic long-grain basmati rice, caramelized sweet carrot juliennes, golden raisins, roasted almonds, and authentic Pashtun secret spices. Served fresh hot every Friday!",
            price=799.00,
            original_price=999.00,
            banner_image="specials/kabuli_pulao.png",
            is_active=True,
            countdown_hours=14
        )

        # 5. Gallery Images
        GalleryImage.objects.create(title="Kabuli Pulao Master Prep", category="Food", image="gallery/gallery3.png")
        GalleryImage.objects.create(title="Flaming Charcoal Grill", category="Kitchen", image="gallery/gallery2.png")
        GalleryImage.objects.create(title="Fresh Wood-Fired Pizza Pull", category="Food", image="gallery/gallery1.png")
        GalleryImage.objects.create(title="KFS Neon Street Vibe", category="Atmosphere", image="gallery/gallery2.png")
        GalleryImage.objects.create(title="Chef Handcrafting Pizzas", category="Kitchen", image="gallery/gallery1.png")
        GalleryImage.objects.create(title="Night Street Dining Area", category="Atmosphere", image="gallery/gallery3.png")

        self.stdout.write(self.style.SUCCESS("Successfully seeded KFS Database!"))
