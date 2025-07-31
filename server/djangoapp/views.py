# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime
from django.core.management import call_command   # NEW
from django.utils.timezone import now             # NEW
import os       


from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
#from .populate import initiate
from djangoapp.scripts.populate import run
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)  # Terminate user session
    data = {"userName": ""}  # Return empty username
    return JsonResponse(data)

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    context = {}

    # Load JSON data from the request body
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    email_exist = False
    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except:
        # If not, simply log this is a new user
        logger.debug("{} is new user".format(username))

    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,password=password, email=email)
        # Login the user and redirect to list page
        login(request, user)
        data = {"userName":username,"status":"Authenticated"}
        return JsonResponse(data)
    else :
        data = {"userName":username,"error":"Already Registered"}
        return JsonResponse(data)
    
  

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...
def get_dealerships(request, state="All"):
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/"+state
    dealerships = get_request(endpoint)
    return JsonResponse({"status":200,"dealers":dealerships})


# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request,dealer_id):
    # if dealer id has been provided
    if(dealer_id):
        endpoint = "/fetchReviews/dealer/"+str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            print(response)
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status":200,"reviews":reviews})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})

# Create a `get_dealer_details` view to render the dealer details
def get_dealer_details(request, dealer_id):
    if(dealer_id):
        endpoint = "/fetchDealer/"+str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status":200,"dealer":dealership})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})


# Create a `add_review` view to submit a review
def add_review(request):
    if(request.user.is_anonymous == False):
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status":200})
        except:
            return JsonResponse({"status":401,"message":"Error in posting review"})
    else:
        return JsonResponse({"status":403,"message":"Unauthorized"})


# Create a `import CarMake & CarModel` .
#def get_cars(request):
    #count = CarMake.objects.filter().count()
    #print(count)
    #if(count == 0):
        #run()
    #car_models = CarModel.objects.select_related('car_make')
    #cars = []
    #for car_model in car_models:
        #cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    #return JsonResponse({"CarModels":cars})

def get_cars(request):
    if CarMake.objects.count() == 0:
        run()

    car_models = CarModel.objects.select_related('car_make')
    cars = [
        {
            "model": car_model.name,
            "make": car_model.car_make.name,
            "type": car_model.type,
            "year": car_model.year
        }
        for car_model in car_models
    ]

    return JsonResponse(cars, safe=False)

def show_inventory(request):
    if CarMake.objects.count() == 0:
        run()

    makes = CarMake.objects.all()
    models = CarModel.objects.select_related('car_make')
    return render(request, 'inventory.html', {
        'makes': makes,
        'models': models,
    })

def inventory_dashboard(request):
    # Auto-populate if DB is empty
    if CarMake.objects.count() == 0:
        try:
            fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures/cars.json')
            call_command('loaddata', fixture_path)
        except Exception as e:
            print(f"Error loading fixture: {e}")

    makes = CarMake.objects.all()
    models = CarModel.objects.select_related('car_make')
    newest_model = models.order_by('-year').first()

    context = {
        'makes': makes,
        'models': models,
        'total_makes': makes.count(),
        'total_models': models.count(),
        'newest_model': newest_model,
        'backup_time': now().strftime('%Y-%m-%d %H:%M:%S'),  # pretend timestamp
    }
    return render(request, 'inventory.html', context)    





def populate_cars(request):
    run()
    return JsonResponse({"status": 200, "message": "Car data added!"})