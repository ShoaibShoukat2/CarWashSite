from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password ,check_password # Import make_password
from .models import *
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
import stripe
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
import qrcode   
from io import BytesIO
from django.http import FileResponse
import os
from django.http import HttpResponse
import requests

from urllib.parse import urlparse, parse_qs


# Create your views here.

def Gateway(request):       
    context = {}    

    # Parse the URL to extract query parameters
    query_params = request.META.get('QUERY_STRING', '')
    parsed_query_params = parse_qs(query_params)

    # Extract the parameters you need
    subscription_id = parsed_query_params.get('subscription_id', [''])[0]
    package_id = parsed_query_params.get('package_id', [''])[0]
    vehicle_id = parsed_query_params.get('vehicle_id', [''])[0]


    try:
        # Retrieve necessary data from your database
        vehicle_data = Vehicle.objects.get(id=vehicle_id)
        subscription_data = SubscrationDuration.objects.get(id=subscription_id)
        package_data = Packages.objects.get(id=package_id)
        description_price = DescriptionPrice.objects.get(
            vehicle_id=vehicle_data, 
            subscription_id=subscription_data, 
            package_id=package_data
        )       

        user_id = request.session.get('user_id')
        user_name = request.session.get('user_name')
        user_email = request.session.get('user_email')



        # Add retrieved data to context
        context['user_id'] = user_id
        context['user_name'] = user_name
        context['user_email'] = user_email
        context['subscription'] = subscription_data.subscription_name
        context['package'] = package_data.name
        context['vehicle'] = vehicle_data.name
        context['price'] = description_price.price
        context['vehicle_id'] = vehicle_id


        if not user_email:
            context['error_message'] = "Please login first"


    except (Vehicle.DoesNotExist, SubscrationDuration.DoesNotExist, Packages.DoesNotExist, DescriptionPrice.DoesNotExist):
        context['error_message'] = "Facing some issues"

    return render(request, 'gateway.html', context)






def verify_userprofile(request):
    if request.method == 'GET':
        email = request.session.get('user_email')

        if email:
            try:
                # Check if a user with the given email exists in UserProfile
                user_profile = UserProfile.objects.get(user_email=email)
                return JsonResponse({'success': True, 'email': email})
            except UserProfile.DoesNotExist:
                # User with the given email does not exist
                return JsonResponse({'success': False, 'error': 'User profile not found'}, status=404)
        else:
            return JsonResponse({'success': False, 'error': 'Email not found in session'}, status=400)









def index(request):

    vehicle_data = Vehicle.objects.all()


    context = {
        'CarData':vehicle_data
    }

    return render(request,'index.html',context)


def signup(request):
    context = {}

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        vehicle_brand = request.POST.get('vehicle_brand')
        vehicle_model = request.POST.get('vehicle_model')
        vehicle_type = request.POST.get('vehicle_type')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the email already exists
        if Signup.objects.filter(email=email).exists():
            context['error_message'] = 'User with this email already exists. Please use a different email.'
            context['redirect_url'] = 'signup'
        else:
            # Check if passwords match
            if password != confirm_password:
                context['error_message'] = 'Passwords do not match.'
                context['redirect_url'] = 'signup'
            else:
                # Hash the password
                hashed_password = make_password(password)
                
                # Handle image upload
                image_file = request.FILES.get('image')
                if image_file:
                    fs = FileSystemStorage()
                    filename = fs.save(image_file.name, image_file)
                    image_url = fs.url(filename)
                else:
                    # Set a default image URL or handle accordingly
                    image_url = None

                # Create a new Signup object and save it to the database
                new_signup = Signup.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone_number,
                    vehicle_brand=vehicle_brand,
                    vehicle_model=vehicle_model,
                    vehicle_type=vehicle_type,
                    password=hashed_password,
                    image=image_url  # Save the image URL to the database
                )
                context['success_message'] = 'Submitted successfully'
                context['redirect_url'] = 'login'

    return render(request, 'signup.html', context)

def SubscriptionPage(request):

    vehicle_data = Vehicle.objects.all()


    context = {
        'CarData':vehicle_data
    }

 
    return render(request,'sub_category.html',context)


def Details(request, id):
    try:
        vehicle = Vehicle.objects.get(id=id)
        sub_data = SubscrationDuration.objects.filter(vehicle_id=vehicle)
        subscription_dict = {}

        for data in sub_data:
            subscription_packages = []
            package_info = Packages.objects.filter(subscription_id=data)
            
            for package in package_info:
                descriptions = []
                description_prices = DescriptionPrice.objects.filter(vehicle_id=vehicle, subscription_id=data, package_id=package.id)
                
                for dp in description_prices:
                    descriptions.append({
                        'description': dp.description,
                        'price': dp.price,
                        'package_id': package.id,
                        'subscription_id': data.id,
                        'vehicle_id': vehicle.id
                    })

                subscription_packages.append({
                    'name': package.name,
                    'id': package.id,
                    'descriptions': descriptions
                })
            
            subscription_dict[data.subscription_name] = subscription_packages

        context = {
            'vehicle': {
                'id': vehicle.id,
                'name': vehicle.name,  # Add other fields as needed
                # Add other fields as needed
            },
            'sub_data': subscription_dict,
        }

        return JsonResponse(context)
    except Vehicle.DoesNotExist:
        return JsonResponse({'error': 'Vehicle not found'}, status=404)


def login(request):
    context = {}  # Initialize an empty context dictionary
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Signup.objects.get(email=email)
            if check_password(password, user.password):
                request.session['user_email'] = email
                request.session['user_id'] = user.id
                request.session['user_name'] = user.first_name
                context['success_message'] = 'Login successful'

            else:
                context['error_message'] = 'Invalid email or password. Please try again.'
                context['redirect_url'] = 'login'
        except Signup.DoesNotExist:

            context['error_message'] = 'Invalid email or password. Please try again.'
            context['redirect_url'] = 'login'

    return render(request, 'login.html',context)

def Logout(request):
    
    del request.session['user_email']
    del request.session['user_id']
    del request.session['user_name']


    return redirect('index-page')

def Guide(request):
    return render(request,'Guide.html')

def contact(request):
    return render(request,'contact.html')

def blog(request):

    admin = Admin.objects.all()
    blog_data = Blog.objects.all()
    category_data = Category.objects.all()
    comments_data = Comments.objects.all()


    blog_data_with_comments = {} 

    for blog in blog_data:
        comments_for_blog = comments_data.filter(blog_id=blog.id)
        blog_data_with_comments[blog] = {
            'id':blog.id,
            'title': blog.title,
            'description': blog.description,
            'comments': comments_for_blog,
    
        }
        
    return render(request, 'Blogs.html', {
        'blog_data_with_comments': blog_data_with_comments,
        'cat_data':category_data,
        'Admin':admin
        
        })

def add_comment(request, pk):
    blog = Blog.objects.get(pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name')
        comment_text = request.POST.get('comment')

        new_comment = Comments.objects.create(
            blog_id=blog,
            name=name,
            comments=comment_text
        )

        new_comment.save()

    return redirect('blog-page')

def FAQ_Function(request):

    return render(request,'FAQ.html')

def schedule_appointment(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        date = request.POST.get('date')
        
        # Get the user_id from the session
        user_id = request.session.get('user_id')
        
        # If user_id exists in session, try to get the user
        if user_id:
            try:
                user = Signup.objects.get(id=user_id)
                # If user is found, create the appointment
                appointment = AppoitmentSchedule.objects.create(
                    user_id=user,
                    location=location,
                    date=date
                )
                # Optionally, you can add a success message
                return render(request, 'Scheduling.html', {'success_message': 'Appointment data submitted successfully.'})
                return redirect('/')  # Redirect to a success page
            except Signup.DoesNotExist:
                pass  # Handle the case where the user does not exist
        # If user_id does not exist in session or user is not found, render the error message
        return render(request, 'Scheduling.html', {'error_message': 'Please log in first.'})
    else:
        return render(request, 'Scheduling.html')

def Profile(request):

    # Get user ID from session
    user_id = request.session.get('user_id')

    # Fetch user's subscription details
    try:
        user_profile = UserProfile.objects.get(user_id=user_id)
    except UserProfile.DoesNotExist:
        user_profile = None


    return render(request, 'profile.html', {'user_profile': user_profile})

def Subscribe(request):

    context = {}

    if request.method == 'GET': 
        subscription_id = request.GET.get('subscription_id')
        package_id = request.GET.get('package_id')
        vehicle_id = request.GET.get('vehicle_id')

        try:
            # Retrieve necessary data from the database
            vehicle_data = Vehicle.objects.get(id=vehicle_id)
            subscription_data = SubscrationDuration.objects.get(id=subscription_id)
            package_data = Packages.objects.get(id=package_id)
            description_price = DescriptionPrice.objects.get(vehicle_id=vehicle_data, subscription_id=subscription_data, package_id=package_data)

            # Get user information from session
            user_id  = request.session.get('user_id')
            user_name = request.session.get('user_name')
            user_email = request.session.get('user_email')

            if not user_email:
                context['error_message'] = "Please login first"
                return render(request,'index.html',context)


            # Check if the user exists in the Signup database
            try:
                user = Signup.objects.get(id=user_id)
            except Signup.DoesNotExist:
                context['error_message'] = "User does not exist"
                return render(request,'index.html',context)

            # Save data into UserProfile model after successful payment
            UserProfile.objects.create(
                user_id=user,
                user_name=user_name,
                user_email=user_email,
                subscription=subscription_data.subscription_name,
                package=package_data.name,
                vehicle=vehicle_data.name,
                price=description_price.price
            )


            # Path to your QR code PNG file
            qr_code_path = "D:/Salman_Projects/CarWash/main/static/img/QRCode.jpeg"



            # Check if the file exists
            if os.path.exists(qr_code_path):
                # Serve the PNG file as response
                return FileResponse(open(qr_code_path, 'rb'), content_type='image/png')
            else:
                # If the file does not exist, return an error message
                return HttpResponse("QR code image not found", status=404)

        except (Vehicle.DoesNotExist, SubscrationDuration.DoesNotExist, Packages.DoesNotExist, DescriptionPrice.DoesNotExist) as e:
            print("Error:", e)
            return render(request, 'subscribe_template.html', {'error_message': 'Error processing subscription'})

    return render(request, 'subscribe_template.html')






def Success(request):

    return render(request,'success_page.html')


def Error(request):


    return render(request,'error_page.html')


# Dashboard Functions



def Dashboard(request):

    user_profiles = UserProfile.objects.all()

    
    return render(request,'Dashboard/admin.html', {'user_profiles': user_profiles})


def AdminLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Authentication successful, login the user
            auth_login(request, user)
            # Redirect to the admin page or any other page you want
            return redirect('Dashboard-Page')  # Assuming 'admin_dashboard' is the name of the URL pattern for the admin page
        else:
            # Authentication failed, display an error message
            error_message = "Invalid username or password"
            return render(request, 'adminlogin.html', {'error_message': error_message})
    else:
        return render(request, 'adminlogin.html')



def Addblog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        
        if title and description and category_id:
            category = Category.objects.get(pk=category_id)
            # Assuming you have an Admin object associated with the admin_id
            admin = Admin.objects.get(pk=1)
            Blog.objects.create(admin=admin, title=title, description=description, category=category)
            return redirect('addblogsuccess-Page')  # Redirect to a success page after adding the blog
        else:
            # Handle invalid form data here
            pass
    else:
        categories = Category.objects.all()
        return render(request, 'Dashboard/AddBlog.html', {'categories': categories})



def adminsuccess(request):
    return render(request,'Dashboard/success.html')




def Appointments(request):

    appointments = AppoitmentSchedule.objects.all()

    return render(request,'Dashboard/Appointments.html',{'appointments': appointments})



