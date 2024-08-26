from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm

import random, json

# Create your views here.

# rooms = [
#     {'id': 1, 'name': 'Lets learn python!'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'Frontend developers'},
# ]


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))[0:3]

    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)


##POKER GAME FUNCTIONALITY INSIDE A SINGLE ROOM --------------------------------------------------- START

def get_deck():
    deck = ['1H', '1D', '1C', '1S', '13H', '13D', '13C', '13S', '12H', '12D', '12C', '12S', '11H', '11D', 
            '11C', '11S', '10H', '10D', '10C', '10S', '9H', '9D', '9C', '9S', '8H', '8D', '8C', '8S', 
            '7H', '7D', '7C', '7S', '6H', '6D', '6C', '6S', '5H', '5D', '5C', '5S', '4H', '4D', 
            '4C', '4S', '3H', '3D', '3C', '3S', '2H', '2D', '2C', '2S']
    random.shuffle(deck)
    return deck


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    
    deck = get_deck()
    cards = [deck[0], deck[1]]
    deck = deck[2:]
    room.deck=json.dumps(deck)
    room.pot_size = 0
    user = request.user
    user.card1 = cards[0]
    user.card2 = cards[1]
    user.save()
    room.save()

    context = {'pot_size': room.pot_size,'chip_count': user.chip_count, 'room': room, 'room_messages': room_messages,
               'participants': participants, 'player_cards': cards}
    return render(request, 'base/room.html', context)

def flop(request, pk):
    if request.method == "POST":
        bet_amount = int(request.POST.get('bet_amount'))
        room = Room.objects.get(id=pk)
        user=request.user
        user.chip_count -= bet_amount
        room.pot_size += bet_amount
        user.save()
        room.save()
        
        deck = json.loads(room.deck)
        room.card1 = deck[0]
        room.card2 = deck[1]
        room.card3 = deck[2]
        deck = deck[3:]
        room.deck = json.dumps(deck)
        room.save() 
        
        context = {'room': room, 'pot_size': room.pot_size,'chip_count': user.chip_count}
        return render(request, 'base/gameplay/flop.html', context)
    
    return redirect('home')

def turn(request, pk):
    if request.method == "POST":
        bet_amount = int(request.POST.get('bet_amount'))
        room = Room.objects.get(id=pk)
        user=request.user
        user.chip_count -= bet_amount
        room.pot_size += bet_amount
        user.save()
        room.save()
        
        deck = json.loads(room.deck)
        room.card4 = deck[0]
        deck = deck[1:]
        room.deck = json.dumps(deck)
        room.save() 
        
        context = {'room': room, 'pot_size': room.pot_size,'chip_count': user.chip_count}
        return render(request, 'base/gameplay/turn.html', context)
    
    return redirect('home')

def river(request, pk):
    if request.method == "POST":
        bet_amount = int(request.POST.get('bet_amount'))
        room = Room.objects.get(id=pk)
        user=request.user
        user.chip_count -= bet_amount
        room.pot_size += bet_amount
        user.save()
        room.save()
        
        deck = json.loads(room.deck)
        room.card5 = deck[0]
        deck = deck[1:]
        room.deck = json.dumps(deck)
        room.save() 
        
        context = {'room': room, 'pot_size': room.pot_size,'chip_count': user.chip_count}
        return render(request, 'base/gameplay/river.html', context)
    
    return redirect('home')    

def reveal_hand(request, pk):
    if request.method == "POST":
        bet_amount = int(request.POST.get('bet_amount'))
        room = Room.objects.get(id=pk)
        user=request.user
        user.chip_count -= bet_amount
        room.pot_size += bet_amount
        user.save()
        room.save()
        
        
        
        deck = json.loads(room.deck)
        room.card4 = deck[0]
        deck = deck[1:]
        room.deck = json.dumps(deck)
        room.save() 
        
        context = {'room': room, 'pot_size': room.pot_size,'chip_count': user.chip_count}
        return render(request, 'base/gameplay/turn.html', context)
    
    return redirect('home')

def fold(request):
    return redirect('home')


#END -----------------------------------------------------------------------------


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})
