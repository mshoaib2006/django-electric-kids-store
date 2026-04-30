from decimal import Decimal, InvalidOperation

from django.contrib import admin
from django.utils.html import format_html, strip_tags

from .models import Category, Product, ProductImage, Order, OrderItem, Review, UserProfile


def format_money(value):
    """
    Safe money formatter.
    Handles Decimal, int, float, string, and SafeString values.
    """
    if value is None:
        return "0"

    text = strip_tags(str(value))
    text = text.replace("Rs.", "").replace("Rs", "").replace(",", "").strip()

    try:
        amount = Decimal(text)
        return f"{amount:,.0f}"
    except (InvalidOperation, ValueError, TypeError):
        return str(value)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 5
    fields = ["image", "alt_text", "is_primary", "sort_order", "image_preview"]
    readonly_fields = ["image_preview"]

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" width="80" height="60" '
                'style="object-fit:cover;border-radius:4px;" />',
                obj.image.url,
            )
        return "No image"

    image_preview.short_description = "Preview"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["product", "quantity", "price", "subtotal_display"]

    def subtotal_display(self, obj):
        amount_text = format_money(getattr(obj, "subtotal", 0))
        return f"Rs. {amount_text}"

    subtotal_display.short_description = "Subtotal"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "product_count", "created_at"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]

    def product_count(self, obj):
        return obj.products.count()

    product_count.short_description = "Products"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "category",
        "price",
        "stock",
        "is_available",
        "is_featured",
        "image_preview",
        "created_at",
    ]

    list_filter = ["category", "is_available", "is_featured"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ["price", "stock", "is_available", "is_featured"]
    inlines = [ProductImageInline]

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "category",
                    "name",
                    "slug",
                    "description",
                    "is_available",
                    "is_featured",
                )
            },
        ),
        (
            "Pricing & Stock",
            {
                "fields": (
                    "price",
                    "original_price",
                    "stock",
                )
            },
        ),
        (
            "Specifications",
            {
                "fields": (
                    "weight",
                    "dimensions",
                    "age_group",
                    "battery_life",
                    "max_speed",
                    "color_options",
                    "warranty",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    def image_preview(self, obj):
        img = obj.primary_image

        if img and img.image:
            return format_html(
                '<img src="{}" width="50" height="40" '
                'style="object-fit:cover;border-radius:4px;" />',
                img.image.url,
            )

        return "—"

    image_preview.short_description = "Image"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "order_number",
        "full_name_display",
        "phone",
        "city",
        "status",
        "payment_method",
        "total_display",
        "created_at",
    ]

    list_filter = ["status", "payment_method", "created_at"]
    search_fields = ["order_number", "first_name", "last_name", "email", "phone", "city"]
    list_editable = ["status"]
    readonly_fields = ["order_number", "created_at", "updated_at"]
    inlines = [OrderItemInline]

    def total_display(self, obj):
        amount_text = format_money(getattr(obj, "total_amount", 0))
        return format_html("<strong>Rs. {}</strong>", amount_text)

    total_display.short_description = "Total"

    def full_name_display(self, obj):
        return getattr(obj, "full_name", "—")

    full_name_display.short_description = "Customer"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["product", "user", "rating", "title", "created_at"]
    list_filter = ["rating"]
    search_fields = ["product__name", "user__username", "title"]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "phone", "city", "created_at"]
    search_fields = ["user__username", "phone", "city"]