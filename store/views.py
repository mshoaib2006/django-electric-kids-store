from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg, Count, Sum
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.auth.models import User
from .models import Product, Category, Order, OrderItem, Review, UserProfile
from .forms import RegisterForm, UserProfileForm, ReviewForm, CheckoutForm
from .cart import Cart
import json


def home(request):
    featured_products = Product.objects.filter(is_available=True, is_featured=True).prefetch_related('images')[:6]
    latest_products = Product.objects.filter(is_available=True).prefetch_related('images')[:8]
    categories = Category.objects.annotate(product_count=Count('products')).filter(product_count__gt=0)
    context = {
        'featured_products': featured_products,
        'latest_products': latest_products,
        'categories': categories,
    }
    return render(request, 'store/home.html', context)


def product_list(request):
    products = Product.objects.filter(is_available=True).prefetch_related('images')
    categories = Category.objects.all()
    
    # Filters
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'newest')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )
    
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    sort_options = {
        'newest': '-created_at',
        'price_low': 'price',
        'price_high': '-price',
        'name': 'name',
    }
    products = products.order_by(sort_options.get(sort_by, '-created_at'))
    
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'sort_by': sort_by,
        'category_slug': category_slug,
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    images = product.images.all()
    reviews = product.reviews.select_related('user').all()
    related_products = Product.objects.filter(category=product.category, is_available=True).exclude(id=product.id)[:4]
    
    review_form = ReviewForm()
    user_review = None
    
    if request.user.is_authenticated:
        user_review = Review.objects.filter(product=product, user=request.user).first()
    
    if request.method == 'POST' and request.user.is_authenticated:
        if not user_review:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                messages.success(request, 'Your review has been submitted!')
                return redirect('product_detail', slug=slug)
    
    # WhatsApp order link
    whatsapp_msg = f"Hi! I want to order: {product.name} (Rs. {product.price}). Please confirm availability."
    whatsapp_url = f"https://wa.me/{settings.WHATSAPP_NUMBER}?text={whatsapp_msg}"
    
    context = {
        'product': product,
        'images': images,
        'reviews': reviews,
        'related_products': related_products,
        'review_form': review_form,
        'user_review': user_review,
        'whatsapp_url': whatsapp_url,
    }
    return render(request, 'store/product_detail.html', context)


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_available=True).prefetch_related('images')
    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'store/category_products.html', {'category': category, 'page_obj': page_obj})


# ---- CART VIEWS ----
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'store/cart.html', {'cart': cart})


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': len(cart),
            'cart_total': str(cart.get_total_price()),
            'message': f"{product.name} added to cart!"
        })
    messages.success(request, f"'{product.name}' added to cart!")
    return redirect('cart_detail')


def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart.add(product=product, quantity=quantity, override_quantity=True)
    else:
        cart.remove(product)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        item_total = 0
        for item in cart:
            if item['product'].id == product_id:
                item_total = item['total_price']
                break
        return JsonResponse({
            'success': True,
            'cart_count': len(cart),
            'cart_total': str(cart.get_total_price()),
            'item_total': str(item_total),
        })
    return redirect('cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'cart_count': len(cart), 'cart_total': str(cart.get_total_price())})
    messages.success(request, "Item removed from cart.")
    return redirect('cart_detail')


# ---- CHECKOUT & ORDER ----
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "Your cart is empty!")
        return redirect('cart_detail')
    
    initial = {}
    if request.user.is_authenticated:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        try:
            profile = request.user.profile
            initial.update({'phone': profile.phone, 'address': profile.address, 'city': profile.city})
        except:
            pass
    
    form = CheckoutForm(initial=initial)
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.total_amount = cart.get_total_price()
            order.save()
            
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['price'],
                )
                # Reduce stock
                product = item['product']
                product.stock = max(0, product.stock - item['quantity'])
                product.save()
            
            cart.clear()
            messages.success(request, f"Order #{order.order_number} placed successfully!")
            return redirect('order_confirmation', order_number=order.order_number)
    
    return render(request, 'store/checkout.html', {'form': form, 'cart': cart})


def order_confirmation(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    whatsapp_msg = f"Hi! My order #{order.order_number} has been placed. Total: Rs. {order.total_amount}. Please confirm."
    whatsapp_url = f"https://wa.me/{settings.WHATSAPP_NUMBER}?text={whatsapp_msg}"
    return render(request, 'store/order_confirmation.html', {'order': order, 'whatsapp_url': whatsapp_url})


# ---- AUTH ----
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, f"Welcome, {user.first_name}! Account created successfully.")
            return redirect('home')
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
    
    profile_form = UserProfileForm(instance=user_profile)
    
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if profile_form.is_valid():
            profile_form.save()
            # Update user name/email
            request.user.first_name = request.POST.get('first_name', request.user.first_name)
            request.user.last_name = request.POST.get('last_name', request.user.last_name)
            request.user.email = request.POST.get('email', request.user.email)
            request.user.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/profile.html', {'profile_form': profile_form, 'orders': orders})


# ---- DASHBOARD (Admin) ----
@login_required
def dashboard(request):
    if not request.user.is_staff:
        return redirect('home')
    
    from django.utils import timezone
    from datetime import timedelta
    
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_products = Product.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    
    recent_orders = Order.objects.order_by('-created_at')[:10]
    top_products = Product.objects.annotate(order_count=Count('orderitem')).order_by('-order_count')[:5]
    
    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_products': total_products,
        'pending_orders': pending_orders,
        'recent_orders': recent_orders,
        'top_products': top_products,
    }
    return render(request, 'store/dashboard.html', context)


def search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query),
        is_available=True
    ).prefetch_related('images') if query else Product.objects.none()
    return render(request, 'store/search_results.html', {'products': products, 'query': query})
