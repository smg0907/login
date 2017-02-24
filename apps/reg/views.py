from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

def index(req):
    return render(req, 'reg/index.html')

def login(req):
    if req.method == 'POST':
        validate = User.objects.login(req.POST)
        print "login data received", validate
        if validate[0] == False:
            print "Hello World2"
            loginMessages = {'absent': 'This username could not be located in our database', 'password': 'The password you entered is incorrect.'}
            for problem in validate[1]:
                messages.error(req, loginMessages[problem], extra_tags = "login")
            return redirect('/')
        req.session['loggedin'] = validate[1].id
        return redirect('/success')
    else:
        return redirect('/')

def register(req):
    if req.method == 'POST':
        validate = User.objects.register(req.POST)
        if validate[0] == False:
            assignMessages = {'empty': "All fields are required",
              'name': "Names must contain at least 3 characters and be composed only of letters",
              'username': "Invalid username entered",
              'passlength':"Password must contain at least 8 characters",
              'passmatch': "Passwords must match",
              'unique': "Username has already been taken"}
            if len(validate[1])>0:
                for problem in validate[1]:
                    messages.error(req, assignMessages[problem], extra_tags = "register {}".format(problem))
                messages.info(req, req.POST['name'], extra_tags="name")
                messages.info(req, req.POST['username'], extra_tags="username")
            return redirect('/')

        print "Sucessful registration", validate[1].id
        req.session['loggedin'] = validate[1].id
        return redirect('/success')
    else:
        return redirect('/')

def success(req):
    if 'loggedin' not in req.session:
        messages.error(req, "You must be logged in to view the requested page", extra_tags = 'login')
        return redirect('/')
    # if int(req.session['loggedin']) != int(id):
    #     messages.error(req, "You are not permitted to view the requested page", extra_tags = 'login')
    #     return redirect('/')
    # context = {'guest':User.objects.get(id=id)}
    return render(req, 'reg/success.html')

def addPlan(req):
    return render(req, 'reg/add_plan.html')


def logout(req):
    req.session.clear()
    messages.success(req, "You have been logged out", extra_tags = 'login')
    return redirect('/')
