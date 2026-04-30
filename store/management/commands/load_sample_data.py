from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from store.models import Category, Product, UserProfile


class Command(BaseCommand):
    help = 'Load sample data for Electric Toy Store'

    def handle(self, *args, **kwargs):
        # Create categories
        bike_cat, _ = Category.objects.get_or_create(name='Electric Bikes', slug='electric-bikes', defaults={'description': 'Battery-powered bikes for kids of all ages.'})
        car_cat, _ = Category.objects.get_or_create(name='Electric Cars', slug='electric-cars', defaults={'description': 'Ride-on electric cars for young drivers.'})
        jeep_cat, _ = Category.objects.get_or_create(name='Electric Jeeps', slug='electric-jeeps', defaults={'description': 'Off-road electric jeeps for adventurous kids.'})
        self.stdout.write('✅ Categories created')

        products_data = [
            {'category': bike_cat, 'name': 'Thunder Bolt Electric Bike', 'slug': 'thunder-bolt-electric-bike', 'description': 'High-speed electric bike with LED lights, dual-speed modes and rechargeable battery. Perfect for kids aged 3-8 years. Features sturdy steel frame and safety gear.', 'price': 12500, 'original_price': 15000, 'stock': 25, 'age_group': '3-8 Years', 'battery_life': '2-3 Hours', 'max_speed': '5 km/h', 'warranty': '6 Months', 'is_featured': True},
            {'category': bike_cat, 'name': 'Mini Racer Electric Bike', 'slug': 'mini-racer-electric-bike', 'description': 'Compact electric bike designed for toddlers. Soft start feature for safety.', 'price': 8500, 'original_price': 10000, 'stock': 30, 'age_group': '2-5 Years', 'battery_life': '1.5 Hours', 'max_speed': '3 km/h', 'warranty': '3 Months', 'is_featured': False},
            {'category': car_cat, 'name': 'SuperSport Electric Car', 'slug': 'supersport-electric-car', 'description': 'Full-featured electric car with working horn, music system, and parent remote control. Kids will love this realistic sports car experience!', 'price': 18000, 'original_price': 22000, 'stock': 15, 'age_group': '3-7 Years', 'battery_life': '2-4 Hours', 'max_speed': '6 km/h', 'color_options': 'Red, White, Black', 'warranty': '6 Months', 'is_featured': True},
            {'category': car_cat, 'name': 'Baby Cruiser Electric Car', 'slug': 'baby-cruiser-electric-car', 'description': 'Safe and sturdy electric car for babies and toddlers with parental remote control.', 'price': 9500, 'original_price': 12000, 'stock': 20, 'age_group': '1-3 Years', 'battery_life': '1 Hour', 'max_speed': '2.5 km/h', 'warranty': '3 Months', 'is_featured': False},
            {'category': jeep_cat, 'name': 'Off-Road King Electric Jeep', 'slug': 'off-road-king-electric-jeep', 'description': 'Built tough for outdoor adventures! This electric jeep handles all terrains with its rubber tires and powerful motor. Features 2.4G parental remote control.', 'price': 24000, 'original_price': 28000, 'stock': 10, 'age_group': '3-8 Years', 'battery_life': '3-5 Hours', 'max_speed': '7 km/h', 'color_options': 'Army Green, Black', 'warranty': '1 Year', 'is_featured': True},
            {'category': jeep_cat, 'name': 'Dune Rider Electric Jeep', 'slug': 'dune-rider-electric-jeep', 'description': 'Compact off-road jeep perfect for garden adventures. LED headlights and horn included.', 'price': 16000, 'original_price': 19000, 'stock': 18, 'age_group': '2-6 Years', 'battery_life': '2 Hours', 'max_speed': '5 km/h', 'warranty': '6 Months', 'is_featured': False},
        ]

        for data in products_data:
            product, created = Product.objects.get_or_create(slug=data['slug'], defaults=data)
            if created:
                self.stdout.write(f'  + Product: {product.name}')

        # Create admin user
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@electrictoys.pk', 'admin123')
            UserProfile.objects.create(user=admin)
            self.stdout.write('✅ Admin user created: admin / admin123')

        self.stdout.write(self.style.SUCCESS('\n✅ Sample data loaded successfully!\n   Run: python manage.py runserver\n   Visit: http://127.0.0.1:8000'))
