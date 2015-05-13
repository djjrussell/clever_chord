from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.models import Note
from rango.models import Type
from rango.forms import CategoryForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from engine import Chord
from django.contrib.auth.models import User
from rango.models import Favorites
from django.views.decorators.csrf import csrf_exempt

def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})


def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.
    # category_list = Category.objects.order_by('-likes')[:5]
    category_list = Category.objects.all()
    context_dict = {'categories': category_list}

    # Render the response and send it back!

    return render(request, 'rango/index.html', context_dict)


def chords(request):
    response = ""
    data = []
    note = ""
    ch_type = ""
    is_favorite = False
    favorites = ""
    if request.POST:
        note = request.POST["note"]
        ch_type = request.POST["type"]
        favorites = Favorites.objects.filter(note=note, ch_type=ch_type, user=request.user)
        is_favorite = len(favorites) > 0
    c = Chord()
    response = c.get_strings(note, ch_type)
    data = c.get_array(note, ch_type)
    context_dict = {"get_array": data, "ch_type": ch_type, "note": note, "response": response,
                    "notes": Note.objects.all(), "types": Type.objects.all(), "favorites": favorites, "is_favorite": is_favorite}

    return render(request, 'rango/chords.html', context_dict)


def favorites(request):
    favorites = Favorites.objects.filter(user=request.user)
    return render(request, 'rango/favorites.html', {"favorites": favorites, })

@csrf_exempt
def add_favorite(request):
    print request.POST
    favorite = Favorites()
    favorite.ch_type = request.POST["ch_type"]
    favorite.note = request.POST["note"]
    favorite.user = request.user
    favorite.save()
    return HttpResponse("success")

@csrf_exempt
def del_favorite(request):
    note = request.POST["note"]
    ch_type = request.POST["ch_type"]
    favorites = Favorites.objects.filter(note=note, ch_type=ch_type, user=request.user)
    for f in favorites:
        f.delete()
    return HttpResponse("success")





def about(request):
    # Query the database     for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.
    # category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {}

    # Render the response and send it back!

    return render(request, 'rango/about.html', context_dict)


def category(request, category_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'rango/category.html', context_dict)


def register(request):
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        user = User()
        user.username = request.POST["email"]

        # Now we hash the password with the set_password method.
        # Once hashed, we can update the user object.
        user.set_password(request.POST["password"])
        user.save()
        return HttpResponseRedirect("../login/")

    # Render the template depending on the context.
    return render(request, 'rango/chords_register.html', {})


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
        # because the request.POST.get('<variable>') returns None, if the value does not exist,
        # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('email')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('../chords/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'rango/chords_login.html', {})


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")


# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/rango/login')



