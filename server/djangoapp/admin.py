from django.contrib import admin
from .models import CarMake, CarModel

# Inline class for CarModel
class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1

# Admin class for CarMake
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ('name', 'description')
    search_fields = ('name',)

# Admin class for CarModel
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'type', 'year')
    list_filter = ('type', 'year')
    search_fields = ('name', 'car_make__name')

# Register models with the admin site *after* classes are defined
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)


#previous code
#from django.contrib import admin
# from .models import related models
#from .models import CarMake, CarModel

# CarModelInline class
#class CarModelInline(admin.TabularInline):
    #model = CarModel
    #extra = 1  # Shows 1 empty form for quick additions


# CarModelAdmin class

# CarMakeAdmin class with CarModelInline
#class CarMakeAdmin(admin.ModelAdmin):
    #inlines = [CarModelInline]
    #list_display = ('name', 'description')
    #search_fields = ('name',)


# Register models here
#class CarModelAdmin(admin.ModelAdmin):
    #list_display = ('name', 'car_make', 'type', 'year')
    #list_filter = ('type', 'year')
    #search_fields = ('name', 'car_make__name')
#Register your models here.
#admin.site.register(CarMake)
#admin.site.register(CarModel)
#admin.site.register(CarMake, CarMakeAdmin)
#admin.site.register(CarModel, CarModelAdmin)

