# Uncomment the imports before you add the code
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView 
from . import views
from .views import inventory_dashboard

app_name = 'djangoapp'
urlpatterns = [
    # # path for registration
    path('api/register/', views.registration, name='register'),

    # path for login
    # API endpoint for login authentication (called by React frontend)
    path('api/login/', views.login_user, name='login'),  
    

    # Path for serving the React login page
    path('login/', TemplateView.as_view(template_name="index.html"), name='react_login'),
    
    #path for logout
    path('logout/', views.logout_request, name='logout'),


    # path for dealer reviews view
    path(route='reviews/dealer/<int:dealer_id>', view=views.get_dealer_reviews, name='dealer_details'),

    # path for add a review view
    path(route='add_review', view=views.add_review, name='add_review'),

    #path for get_cars
    #path(route='get_cars', view=views.get_cars, name ='getcars'),
    path('api/cars/', views.get_cars, name='get_cars'),

    #path for get_dealerships
    #path(route='get_dealers/<str:state>', view=views.get_dealerships, name='get_dealers_by_state'),
    path(route='get_dealers/', view=views.get_dealerships, name='get_dealers'),
        path('get_dealers/<str:state>', views.get_dealerships, name='get_dealers_by_state'),

    path('inventory/', views.show_inventory, name='inventory'),

    
    #path for get_dealer_details
    path(route='dealer/<int:dealer_id>', view=views.get_dealer_details, name='dealer_details'),    

    #path('<path:resource>', TemplateView.as_view(template_name="index.html")),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
