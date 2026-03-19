import random
import requests

from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout

from items.models import Item
from .forms import UserForm, CitizenForm, AreaOfficerForm, ContactForm
from .models import User, Contact, Citizen, AreaOfficer, UserProfile


def select_role_view(request):
    return render(request, 'account/index.html')

class CreateUserView(View):

    def post(self, request):

        role = request.POST.get("role")
        request.session['role'] = role
        user_form = UserForm(request.POST)
        contact_form = ContactForm(request.POST)
        citizen_form = CitizenForm(request.POST)
        officer_form = AreaOfficerForm(request.POST)

        if user_form.is_valid() and contact_form.is_valid():

            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data["password"])
            user.save()

            contact = contact_form.save(commit=False)
            contact.user = user
            contact.save()


            if role == "citizen" and citizen_form.is_valid():
                citizen = citizen_form.save(commit=False)
                citizen.user = user
                citizen.save()

            elif role == "area_officer" and officer_form.is_valid():
                officer = officer_form.save(commit=False)
                officer.user = user
                officer.save()

            request.session['email'] = user.email
            request.session['phone'] = contact.phone

            # generate email here then send via api and will validate in otp post
            # self.sendOTP(request)

            # messages.success(request, "Account created successfully")
            # return redirect("/account/otp_verification")
            return render(request, "account/login.html")


        # render page again with errors
        return render(request, "account/register.html", {
            "user_form": user_form,
            "citizen_form": citizen_form if role == "citizen" else None,
            "officer_form": officer_form if role == "area_officer" else None,
            "contact_form": contact_form,
            "role": role
        })

    def sendOTP(self, request):
        otp = str(random.randint(100000, 999999))
        phone = int(request.session['phone'])
        request.session['otp'] = otp

        url = "https://www.fast2sms.com/dev/bulkV2"

        payload = {
            "authorization": "Q1NOHwFanr7hvJjM69ZKg2VGz84BixltPYqmCRkEupW5yTdAbeMaZD4Wx8bqnvkKwI2Rc3ioYdtGSTEO",
            "variables_values": otp,
            "route": "otp",
            "numbers": phone
        }

        response = requests.get(url, params=payload)

        return response.json()

def register_user(request):

    role = request.GET.get("role")

    user_form = UserForm()
    contact_form = ContactForm()

    citizen_form = None
    officer_form = None

    if role == "citizen":
        citizen_form = CitizenForm()

    elif role == "area_officer":
        officer_form = AreaOfficerForm()

    return render(request, "account/register.html", {
        "user_form": user_form,
        "citizen_form": citizen_form,
        "officer_form": officer_form,
        "contact_form": contact_form,
        "role": role
    })

def logout_user(request):
    logout(request)
    return render(request, 'account/login.html')

class LoginView(View):

    def get(self, request):
        return render(request, 'account/login.html')

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")
        print('\n\n')
        print(request.POST)
        user = authenticate(request, username=email, password=password)
        print('\n\n')
        print(user)
        if user is not None:

            # optional role check
            if user.role == 'citizen':
                login(request, user)

                return redirect("citizen_dashboard")
                # return redirect("otp_verification")

            elif user.role == 'area_officer':
                login(request, user)
                return redirect("officer_dashboard")
                # return redirect("otp_verification")

            else:
                return render(request, "account/login.html", {"error": "Invalid role selected"})

        return render(request, "account/login.html", {"error": "Invalid email or password"})

def citizen_dashboard(request):
    items = Item.objects.all().order_by("-created_at")
    # for item in items:
    #     print('item',item.user.full_name)
    context = {
        "items": items,
    }
    return render(request, 'citizen_dashboard.html',context)

def officer_dashboard(request):
    return render(request, 'officer_dashboard.html')

class OTP_verification(View):
    def get(self, request):
        return render(request, 'account/otp_verify.html')

    def post(self, request):

        return redirect("officer_dashboard")

def chat_view(request):
    return render(request, 'account/chat.html',{"active_page" : 'chat'})

# def profile_view(request):
#     user = None
#     img_url=None
#     if request.user.is_authenticated:
#         user=request.user
#         img=UserProfile.objects.get(user_id=user.user_id)
#         print('\n\n',img)
#         if user.profile:
#             img_url=user.profile.profile_picture.url
#         else:
#             img_url='/media/profile_pics/default.jpg'
#         print(user.profile.profile_picture.url)
#         print(user.user_id)
#         contact=Contact.objects.get(user_id=user.user_id)
#         aadhar=Citizen.objects.get(user_id=user.user_id).aadhar
#         print(contact.phone)
#         print(user.role)

#         user={
#             'role':user.role,
#             'full_name':user.full_name,
#             'email':user.email,
#             'user_id':user.user_id,
#         }
#         contact={
#             'phone':contact.phone,
#             'address':contact.address,
#             'city':contact.city,
#             'state':contact.state,
#             'aadhar':aadhar
#             }
        


#     return render(request, 'account/profile.html', {"img_url":img_url,"user": user,"contact":contact,"active_page" : 'profile'})


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')  # optional safety

    user = request.user

    # ✅ Safe profile fetch
    profile = getattr(user, "profile", None)

    # ✅ Image logic
    if profile and profile.profile_picture:
        img_url = profile.profile_picture.url
    else:
        img_url = "/static/images/default.jpg"  # better than /media

    # ✅ Contact safe fetch
    contact_obj, _ = Contact.objects.get_or_create(user=user)

    # ✅ Aadhar safe fetch
    citizen = Citizen.objects.filter(user=user).first()
    aadhar = citizen.aadhar if citizen else None

    # ✅ Data for template (DO NOT overwrite user object)
    user_data = {
        'role': user.role,
        'full_name': user.full_name,
        'email': user.email,
        'user_id': user.user_id,
    }

    contact_data = {
        'phone': contact_obj.phone,
        'address': contact_obj.address,
        'city': contact_obj.city,
        'state': contact_obj.state,
        'aadhar': aadhar
    }

    return render(request, 'account/profile.html', {
        "img_url": img_url,
        "user": user_data,
        "contact": contact_data,
        "active_page": 'profile'
    })

def update_profile_view(request):

    user_id=request.user.user_id
    user=User.objects.get(user_id=user_id)
    contact=Contact.objects.get(user_id=user_id)
    user.email=request.POST.get('email')
    contact.phone=request.POST.get('phone')
    user.full_name=request.POST.get('full_name')
    contact.address=request.POST.get('address')
    contact.city=request.POST.get('city')
    contact.state=request.POST.get('state')
    user.save()
    contact.save()
    return redirect('profile')