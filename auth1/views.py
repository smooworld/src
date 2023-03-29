from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout,update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from django.contrib import messages
from .forms import SignUpForm,EditProfileForm,ProfileForm
from .models import Profile

# Create your views here.

def home(request):
	"""Returns the user back to home page."""
	return render(request,'home.html',{'name':'Dr Abimbola Oluyemi'})

def intro(request):
	return render(request,'intro.html',{'name':'Dr Abimbola Oluyemi'})

def about(request):
    return render(request, 'about.html', {'name':'Dr Abimbola Oluyemi'})


def projects(request):
    return render(request, 'projects.html', {'name':'Dr Abimbola Oluyemi'})

def login_user(request):
	if request.method =='POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request,('Hi',user.username, 'you have been logged in'))
			return redirect('home')
		else:
			messages.success(request,('Error login in log in with valid username..'))
			return redirect('login')
	else:
		return render(request,'login.html',{})

def logout_user(request):
    logout(request)	
    messages.success(request,('you have been successfully Logged Out'))
    return redirect('home')	
def register_user(request):
	if request.method =='POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']   
			password = form.cleaned_data['password1']
			user = authenticate(request, username=username, password=password)	
			login(request, user)
			messages.success(request,('you have been successfully registered in'))
			return redirect('home')			
	else:
		form = SignUpForm()
	context={'form':form}
	return render(request,'register.html',context)

def edit_profile(request):
	if request.method =='POST':
		form = EditProfileForm(request.POST,instance=request.user)
		profile_form = ProfileForm(request.POST, instance=request.user.profile)
		if form.is_valid() and profile_form.is_valid():
			form.save()
			profile_form.save()
			messages.success(request,('you have been successfully registered in'))
			return redirect('home')
		else:
			messages.error(request, ('Please correct the error below.'))


	else:
		form = EditProfileForm(instance=request.user)
		profile_form = ProfileForm(instance=request.user.profile)
	context={'form':form,'profile_form':profile_form}
	return render(request,"edit_profile.html",context)

def change_password(request):
	if request.method =='POST':
		form = PasswordChangeForm(data=request.POST,user=request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request,form.user)
			messages.success(request,('you have been successfully registered in'))
			return redirect('home')			
	else:
		form = PasswordChangeForm(user=request.user)
	context={'form':form}
	return render(request,'change_password.html',context)


