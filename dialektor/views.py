from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, reverse
from google.cloud import datastore
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from .models import CustomUser, metadata
from .models import collection as Collection
from dialektor_files.fileHandling import DialektFileSecurity, StorageBucket
import hashlib

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
        collection_pic = request.FILES.get('collection-pic', None)
        if collection_pic is not None:
            StorageBucket.write_file_to_storage("testingname.png",collection_pic)
    return HttpResponse(fileID)
def signup(request):
    # renders the signup form
    return render(request, 'signup.html')

def get_collections(request):
    collection_list = ""
    user = request.user.user_id
    collections = Collection.objects.all().filter(user_id=user)
    for collection in collections:
        collection_list += collection.name + ", "
    return HttpResponse(collection_list)
