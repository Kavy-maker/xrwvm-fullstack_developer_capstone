# Uncomment the imports before you add the code
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView 
from . import views


app_name = 'djangoapp'
urlpatterns = [
    # # path for registration

    # path for login
    # API endpoint for login authentication (called by React frontend)
    path('api/login/', views.login_user, name='login'),  

    # Path for serving the React login page
    path('login/', TemplateView.as_view(template_name="index.html"), name='react_login'),

    # path for dealer reviews view

    # path for add a review view

    #path for get_cars
    path(route='get_cars', view=views.get_cars, name ='getcars'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
