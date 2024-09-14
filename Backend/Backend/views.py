from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
import bcrypt
from django.http import HttpResponse
from django.shortcuts import render
import json
from django.core.files.storage import FileSystemStorage

# Setup MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client.GFG_HackFest
users_collection = db.Users
hospitals_collection = db.Hospitals

def home(request):
    return render(request, 'website/index.html')

def signin_page(request):
    return render(request, 'website/Auth/signin.html')

# This function renders the signup form (GET request)
def signup_page(request):
    return render(request, 'website/Auth/signup.html')

def hospitals(request):
    return render(request, 'website/hospitals.html')

def search_hospitals(request):
    return render(request, 'website/search.html')

def list_hospitals_page(request):
    return render(request, 'website/list_hospitals.html')

# This function handles the API for signup (POST request)
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if email already exists
        if users_collection.find_one({"email": email}):
            return JsonResponse({'error': 'Email already exists'}, status=400)

        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Save user
        users_collection.insert_one({
            'username': username,
            'email': email,
            'password': hashed_password
        })

        return JsonResponse({'message': 'User created successfully'}, status=201)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Find user by email
        user = users_collection.find_one({"email": email})
        if not user:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)

        # Check password
        if not bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return JsonResponse({'error': 'Invalid credentials'}, status=400)

        return JsonResponse({'message': 'Login successful'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def get_hospitals(request):
    if request.method == 'GET':
        # Fetch hospitals from MongoDB
        hospitals = list(hospitals_collection.find({}, {'_id': 0}))  # Exclude the MongoDB ID from the response
        return JsonResponse(hospitals, safe=False)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def add_hospital(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        ward_beds = request.POST.get('ward_beds')
        emergency_beds = request.POST.get('emergency_beds')
        icu_beds = request.POST.get('icu_beds')

        # Handle image upload
        if 'image' in request.FILES:
            image = request.FILES['image']
            fs = FileSystemStorage(location='Backend/static/images/Hospitals')
            filename = fs.save(image.name, image)
            image_path = f'/static/images/Hospitals/{filename}'

            # Save hospital data with image path
            hospitals_collection.insert_one({
                'name': name,
                'location': location,
                'image': image_path,
                'beds': {
                    'ward': int(ward_beds) if ward_beds else 0,
                    'emergency': int(emergency_beds) if emergency_beds else 0,
                    'icu': int(icu_beds) if icu_beds else 0,
                }
            })
            return JsonResponse({'message': 'Hospital added successfully'}, status=201)

        return JsonResponse({'error': 'No image file provided'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def get_cities(request):
    # Extract unique cities from the hospitals collection
    cities = hospitals_collection.distinct('location')
    city_names = list(set([city.split(',')[1].strip() for city in cities if ',' in city]))
    return JsonResponse(city_names, safe=False)

def get_hospitals(request):
    if request.method == 'GET':
        # Extract city from GET parameters
        city = request.GET.get('city')
        query = {}
        if city:
            query['location'] = {'$regex': f'{city}', '$options': 'i'}

        hospitals = list(hospitals_collection.find(query))
        # Remove MongoDB specific fields
        for hospital in hospitals:
            hospital['_id'] = str(hospital['_id'])
        return JsonResponse(hospitals, safe=False)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
