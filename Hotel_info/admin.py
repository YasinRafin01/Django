from django.contrib import admin
from django.utils.html import format_html
from .models import Location,Amenity,Property,PropertyImage

# Register your models here.
# admin.site.register(Location)
# admin.site.register(Amenity)
# admin.site.register(Property)
# admin.site.register(PropertyImage)

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    fields = ('image', 'caption', 'image_preview')
    readonly_fields = ('image_preview',)
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return "No Image"

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('property_id', 'title', 'create_date', 'update_date')
    search_fields = ('property_id', 'title', 'description')
    filter_horizontal = ('locations', 'amenities')
    inlines = [PropertyImageInline]

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'image', 'caption','image_preview')
    list_filter = ('property',)
    search_fields = ('property__title', 'caption')
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return "No Image"

    image_preview.short_description = 'Image Preview'


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'latitude', 'longitude')
    list_filter = ('type',)
    search_fields = ('name',)

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
