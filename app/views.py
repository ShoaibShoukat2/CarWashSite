from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password ,check_password # Import make_password
from .models import Signup,Vehicle,SubscrationDuration,Packages,DescriptionPrice


# Create your views here.



def index(request):
    return render(request,'index.html')




def signup(request):
    context = {}  # Initialize an empty context dictionary
    if request.method == 'POST':
        first_name = request.POST.get('fname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if Signup.objects.filter(email=email).exists():
            context['error_message'] = 'User with this email already exists. Please use a different email.'
            context['redirect_url'] = 'signup'

        else:

            hashed_password = make_password(password)


            # Create a new Signup object and save it to the database
            new_signup = Signup.objects.create(
                name=first_name,
                email=email,
                password=hashed_password,
            )


            context['success_message'] = 'submitted successfully'
            context['redirect_url'] = 'login'

        

    return render(request, 'signup.html',context) 



def SubscriptionPage(request):

    vehicle_data = Vehicle.objects.all()


    context = {
        'CarData':vehicle_data
    }

 
    return render(request,'sub_category.html',context)



def Details(request, id):
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
        'vehicle': vehicle,
        'sub_data': subscription_dict,
    }

    return render(request, 'details.html', context)







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
                request.session['user_name'] = user.name
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



def Blog(request):

    return render(request,'Blogs.html')


