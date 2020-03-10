from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, reverse
from google.cloud import datastore
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, update_session_auth_hash
from .models import CustomUser, metadata
from .models import collection as Collection
from dialektor_files.fileHandling import DialektFileSecurity, StorageBucket
import hashlib
from django.core.mail import send_mail


def login_user(request, second=None):
    # main entry page (aka. login page)
    # The "second" argument is not used here, however, it is needed for the group regex call on urls
    return render(request, 'login.html')


def index_home(request, second=None):
    print(request.user)
    if request.user.is_anonymous:
        return render(request, 'home.html')
    return render(request, 'home.html', {'user_id': request.user.user_id})


def render_sound(request, sound_id):
    sound = metadata.objects.get(fileID=sound_id)
    user = CustomUser.objects.get(user_id=sound.user_id)
    print(sound.title)
    return render(request, 'sound.html', {'sound': sound_id, 'title': sound.title, 'author': user.username})


def get_sound(request, sound_id):
    meta_obj = metadata.objects.get(fileID=sound_id)
    storage = StorageBucket(meta_obj)
    storage.s_read_file_from_bucket()
    file_rcv = storage.file
    return HttpResponse(file_rcv, content_type='application/force-download')


def create_user(request):
    print(request.POST)
    email = request.POST['email']
    username = request.POST['username']
    password = request.POST['password']
    firstName = request.POST['first_name']
    lastName = request.POST['last_name']
    instName = request.POST['institution_name']
    instAddr = request.POST['institution_address']
    instCity = request.POST['institution_city']
    instState = request.POST['institution_state']
    instCountry = request.POST['institution_country']
    id = hashlib.md5(str.encode(username+email))
    CustomUser.objects.create_user(username, email, password, first_name=firstName, last_name=lastName, inst_name=instName, inst_addr=instAddr, inst_city=instCity, inst_state=instState, inst_country=instCountry, user_id=id.hexdigest())
    loginInfo = authenticate(username=username, password=password)
    login(request, loginInfo)
    return redirect('/')


def upload(request):
    print(request.POST)
    print(request.FILES)
    print(request.user.user_id)
    title = request.POST.get('title', 'none')
    collection = request.POST.get('collection', 'none')
    category = request.POST.get('category', 'none')
    tags = request.POST.get('tags', 'none')
    length = request.POST.get('length', 'none')
    user = request.user.user_id
    fileID = hash_object = hashlib.md5(str.encode(title+user+collection)).hexdigest()
    file = metadata(user_id=user, title=title,  rec_length=length, collection=collection, category=category, tags=tags, fileID=fileID)
    file.save()
    meta_obj = metadata.objects.get(fileID=fileID)
    storage_bucket = StorageBucket(meta_obj)
    storage_bucket.file = request.FILES['blob'].read()
    storage_bucket.s_write_file_to_bucket()
    del storage_bucket
    storage_bucket2 = StorageBucket(meta_obj)
    storage_bucket2.s_read_file_from_bucket()
    file_rcv = storage_bucket2.file
    collections = Collection.objects.all().filter(user_id=user)
    col_name = request.POST.get('collection', 'none')
    names = [collection.name for collection in collections]
    if col_name not in names:
        c = Collection(user_id=user, name=request.POST.get('collection', 'none'), pic_id=fileID)
        c.save()
    #return HttpResponseRedirect(reverse('render_sound', kwargs={'sound_id': fileID}))
    return HttpResponse(fileID)

def signup(request):
    # renders the signup form
    return render(request, 'signup.html')


def profile(request):
    # check if user is logged in
    # since we are trying to access user information
    if request.user.is_anonymous:
        return HttpResponseRedirect('/')



    ## TODO: only list latest 10 recordings

    userId = request.user.user_id

    # Get list of all user recordings, we need all of them for getting tags
    meta_objs = metadata.objects.filter(user_id=userId).order_by('-date_created')

    # All user tags
    tags = set([])

    user_tags = {}

    # records are dic of all user recordings
    records = {}
    for obj in meta_objs:
        # Add the tags in the current record to the list
        for tag in obj.tags.split(','):
            tags.add(tag.strip())

        data = {
            'title': obj.title,
            'date': obj.date_created,
            'collection': obj.collection,
            'tags': obj.tags,
        }
        records[obj.fileID] = data

    # get user collections

    collection_list = Collection.objects.filter(user_id=userId)
    collections = {}

    for obj in collection_list:
        data = {
            'picture': obj.pic_id
        }
        collections[obj.name] = data

    # Collect all user tags
    for tag in tags:
        data = {
            'tag_name': tag
        }
        user_tags[tag] = data

    content = {
        # TODO: get real profile pic name after it gets implemented
        'profile_pic': '/static/defaultprofile1.png',
        'user_records': records,
        'user_collections': collections,
        'user_tags': user_tags
    }
    return render(request, 'profile/profile.html', content)


def collection_list(request, collection_name):

    print("Get collection: " + collection_name)

    # check if user is logged in
    if request.user.is_anonymous:
        return HttpResponseRedirect('/')

    user = request.user.user_id
    collections = Collection.objects.all().filter(user_id=user)

    col_list = []

    for col in collections:
        col_list.append(col.name)

    if collection_name not in col_list:
        return messenger(request, message="No such collection as " + collection_name, m_type="warning", url_return='/profile/')

        # Get list of all user recordings, we need all of them for getting tags
    meta_objs = metadata.objects.filter(user_id=user, collection=collection_name).order_by('-date_created')
    # records are dic of all user recordings
    records = {}
    tags = set([])
    for obj in meta_objs:
        # Add the tags in the current record to the list
        for tag in obj.tags.split(','):
            tags.add(tag.strip())

        data = {
            'title': obj.title,
            'date': obj.date_created,
            'collection': obj.collection,
            'tags': obj.tags,
        }
        records[obj.fileID] = data

    user_tags = {}

    # Collect all user tags
    for tag in tags:
        data = {
            'tag_name': tag
        }
        user_tags[tag] = data

    content = {
        'collection_name': collection_name,
        'user_records': records,
        'user_tags': user_tags
    }

    return render(request, 'profile/collectionList.html', content)


def profile_update(request):
    if request.method == 'POST':
        user = CustomUser.objects.get(username=request.user.username)
        user.first_name = request.POST.get('first_name', 'none')
        user.last_name = request.POST.get('last_name', 'none')
        user.save()

        return HttpResponseRedirect('/profile')

    else:    
        content = {
            # TODO: get real profile pic name after it gets implemented
            'profile_pic': '/static/defaultprofile1.png',
        }
        return render(request, "profile/editUserProfile.html", content)


def change_pass(request):
    message = ""
    if request.method == 'POST':
        user = CustomUser.objects.get(username=request.user.username)
        entered_pass = request.POST.get('password', False)
        new_pass = request.POST.get('new_password', False)
        if entered_pass is not False:
            # check for current password
            if user.check_password(entered_pass):
                return render(request, 'profile/changePass.html')
            else:
                message = "Password is not correct!"
                return render(request, 'profile/providePass.html', {'message': message})
        else:
            # Change pass word
            user.set_password(new_pass)
            user.save()
            update_session_auth_hash(request, request.user)
            return messenger(request, message="Password successfully updated!", m_type="success", url_return="/profile")
    else:
        return render(request, 'profile/providePass.html', {'message': message})
    pass


def messenger(request, message="Hello there", m_type="undefined", url_return="/"):
    return render(request, 'profile/messenger.html', {'message': message, 'type': m_type, 'ureturn': url_return})


def get_collections(request):
    collection_list = ""
    user = request.user.user_id
    collections = Collection.objects.all().filter(user_id=user)
    for collection in collections:
        collection_list += collection.name + ", "
    return HttpResponse(collection_list)

