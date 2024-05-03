from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password ,check_password # Import make_password
from .models import *
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse

# Create your views here.



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
                        'price': dp.price
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




def Schedule(request):
    return render(request,'Scheduling.html')


