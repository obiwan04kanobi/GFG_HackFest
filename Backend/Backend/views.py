from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
import bcrypt
from django.http import HttpResponse
from django.shortcuts import render

# Setup MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client.GFG_HackFest
users_collection = db.Users

def home(request):
    return render(request, 'website/index.html')

def signin_page(request):
    return render(request, 'website/Auth/signin.html')

# This function renders the signup form (GET request)
def signup_page(request):
    return render(request, 'website/Auth/signup.html')

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
