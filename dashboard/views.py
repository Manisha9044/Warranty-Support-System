from django.shortcuts import render
from .models import *
from django.contrib import messages
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import authenticate, login,logout
from dashboard.admin import*  
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import update_session_auth_hash



class Adminloginview(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, 'dashboard/admin-login.html')

    def post(self, request):
        email = request.POST.get('email')  
        print(email,'email') 
        password = request.POST.get('password') 
        print(password,'password')
        user = authenticate(request, username=email, password=password)
        print(user,'user')

        if user is not None:
            if user.is_superuser:
                login(request, user)
                messages.success(request, 'Login Successfully')
                return redirect('index')
        messages.error(request, 'Wrong Email or Password')
        return render(request, 'dashboard/admin-login.html', {'email': email})
    


class IndexView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('admin_login')
        context = {
        }

        return render(request, 'index.html', context)
    
list="WebnMobapps Solutions Pvt. Ltd. is a Noida‑based tech company that develops " \
"custom web and mobile applications using modern frameworks and technologies. " \
"They focus on building scalable, user‑friendly digital solutions for " \
"clients across various industries. In my current role as a Python Developer," \
" I build scalable APIs, develop custom dashboards, and create dynamic websites " \
"using Python, Django, Django REST Framework, and MySQL, contributing to " \
"high-quality projects for clients."   




class Adminlogout(View):
    def get(self,request):
        logout(request)
        return redirect('admin-login')  


class AdminUpdateProfile(View):

    def get(self, request):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return redirect('login')

        return render(request, 'dashboard/profile_update.html', {
            'user': request.user
        })

    def post(self, request):
        user = request.user

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.phone_number = request.POST.get('phone_number')

        if request.FILES.get('profile_pic'):
            user.profile_pic = request.FILES.get('profile_pic')

        user.save()
        messages.success(request, 'Admin Profile Updated Successfully!')
        return redirect('index')

class Admin_changepassord(View):
    def get(self,request):
        return render(request,'dashboard/admin-change-password.html')
    
    def post(self,request):
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')
        if old_password and new_password and confirm_new_password:
            if request.user.check_password(old_password):
                if new_password == confirm_new_password:
                    user = Custom_User.objects.get(id=request.user.id)
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request,user)
                    messages.success(request,'Password changed successfully.')
                    return redirect('index')
                else:
                    messages.error(request, 'New password and confirm password do not match.')
            else:
                messages.error(request, 'Old password is incorrect.')        

        else:
            messages.error(request, 'All fields are required.')
        return redirect('admin_updateprofile')
    

class CustomerList(View):
    def get(self,request):
        customers = Custom_User.objects.filter(is_superuser=False)
        return render(request,'managecustomers/customer_list.html',{'customers':customers})    
    
class AddCustomer(View):
    def get(self, request):
        return render(request, 'managecustomers/addcustomer.html')

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        profile_pic = request.FILES.get('profile_pic')

        user = Custom_User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            user_type='Customer',
            is_customer=True,
            is_active=True
        )

        if profile_pic:
            user.profile_pic = profile_pic
            user.save()

        messages.success(request, 'Customer created successfully')
        return redirect('customer_list')
class CustomerActiveinactive(View):
    def post(self, request, id):
        customer = Custom_User.objects.get(id=id, user_type='Customer')
        customer.is_active = not customer.is_active
        customer.save()
        return JsonResponse({
            "success": True,
            "is_active": customer.is_active
        })

class EditCustomer(View):
    def get(self, request,id):
        user = Custom_User.objects.get(id=id)
        return render(request, 'managecustomers/editcustomer.html',{'user':user})

    def post(self, request,id):
        user = Custom_User.objects.get(id=id)
        First_Name = request.POST.get('First_Name')
        Last_Name = request.POST.get('Last_Name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        profile_pic = request.FILES.get('profile_pic')
        user.First_Name=First_Name
        user.Last_Name=Last_Name
        user.email=email
        user.phone_number=phone_number
        user.profile_pic = profile_pic
        user.user_type = 'Customer'
        user.is_customer = True
        user.is_active = True
        user.save()

        messages.success(request, 'Customer Updated successfully')
        return redirect('customer_list')
 
class DeleteCustomer(View):
    def get(self, request,id):
        user = Custom_User.objects.get(id=id)
        user.delete()
        messages.success(request, 'Customer Deleted successfully')
        return redirect('customer_list')
    