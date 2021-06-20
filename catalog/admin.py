from django.contrib import admin

from .models import Gift, Category, Brand, GiftInstance, Country


admin.site.register(Category)
admin.site.register(Country)

class GiftsInline(admin.TabularInline):
    model = Gift
    extra=0

class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'est')
    inlines = [GiftsInline]

admin.site.register(Brand, BrandAdmin)


class GiftsInstanceInline(admin.TabularInline):
    model = GiftInstance
    extra=0

@admin.register(Gift)
class GiftAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'display_category')
    fields = [('brand', 'name'), 'description', 'ref', 'category', 'made_in']
    inlines = [GiftsInstanceInline]

@admin.register(GiftInstance)
class GiftInstanceAdmin(admin.ModelAdmin):
    list_display = ('gift','event_date', "requester")
    list_filter = ('gift','event_date',)
