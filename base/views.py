from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm
from django.urls import reverse

from .evaluate_hands import *

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
    deck = ['AH', 'AD', 'AC', 'AS', 'KH', 'KD', 'KC', 'KS', 'QH', 'QD', 'QC', 'QS', 'JH', 'JD', 
            'JC', 'JS', 'TH', 'TD', 'TC', 'TS', '9H', '9D', '9C', '9S', '8H', '8D', '8C', '8S', 
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
    
    context={'room_messages': room_messages,
               'participants': participants, 'room': room}
    return render(request, 'base/room.html', context)

def preflop(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    deck = get_deck()
    cards = [deck[0], deck[1], deck[2], deck[3]]
    deck = deck[4:]
    room.deck=json.dumps(deck)
    room.pot_size = 0
    user = request.user
    user.card1 = cards[0]
    user.card2 = cards[1]
    room.bot_card1 = cards[2]
    room.bot_card2 = cards[3]
    user.hand_strength = 0
    user.save()
    room.save()

    context = {'pot_size': room.pot_size,'chip_count': user.chip_count, 'room': room, 'room_messages': room_messages,
               'participants': participants, 'player_cards': cards}
    
    return render(request, 'base/gameplay/preflop.html', context) 

def flop(request, pk):
    if request.method == "POST":
        bet_amount = int(request.POST.get('bet_amount'))
        room = Room.objects.get(id=pk)
        user=request.user
        user.chip_count -= bet_amount
        room.bot_chip_count -= bet_amount
        room.pot_size +=  2 * bet_amount
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
        room.bot_chip_count -= bet_amount
        room.pot_size +=  2 * bet_amount
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
        room.bot_chip_count -= bet_amount
        room.pot_size +=  2 * bet_amount
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
        room.bot_chip_count -= bet_amount
        room.pot_size +=  2 * bet_amount
        user.save()
        room.save()
        
        user_cards = [user.card1, user.card2, room.card1, room.card2, room.card3, room.card4, room.card5]
        bot_cards = [room.bot_card1, room.bot_card2, room.card1, room.card2, room.card3, room.card4, room.card5]
        user_hand = calculateHand(user_cards)
        bot_hand = calculateHand(bot_cards)
        
        winner=""
        hand_strength = user_hand[0]
        best_hand_text = translate(user_hand[0])
        best_hand_identifier = user_hand[1]
        bot_hand_strength = bot_hand[0]
        bot_best_hand_text = translate(bot_hand[0])
        bot_best_hand_identifier = bot_hand[1]
        result = compare_hand_bool(user_hand, bot_hand)
        if result == 1:
            # user wins
            user.chip_count += room.pot_size
            winner = user.username
        elif result == 0:
            #bot wins
            room.bot_chip_count += room.pot_size
            winner = "BetSmartBot"

        else:
            #tie
            split_pot = room.pot_size // 2
            user.chip_count += split_pot
            room.bot_chip_count += split_pot
            winner = "both players! It's a tie!"
        
        user.save()
        room.save()
        context = {'room': room, 'best_hand_text': best_hand_text, 'hand_strength': hand_strength, 'bot_hand_strength': bot_hand_strength,
                   'best_hand_identifier': best_hand_identifier, 'winner': winner, 'bot_best_hand_text': bot_best_hand_text, 'bot_best_hand_identifier': bot_best_hand_identifier,
                   'pot_size': room.pot_size, 'chip_count': user.chip_count}
        return render(request, 'base/gameplay/reveal_hand.html', context)
    
    return redirect('home')

def calculateHand(cards):
    all_hands = get_hands(cards) #get all 7 choose 2 = 21 possible hands
    best_hand = [0,0,[]]
    for hand in all_hands:
        cur_hand = evaluate(hand)
        best_hand = compare_hand(best_hand, cur_hand)
    return best_hand

def fold(request, pk):
    user = request.user
    room = Room.objects.get(id=pk)
    room.bot_chip_count += room.pot_size
    room.save()
    user.save()
    url = reverse('room', args=[pk])
    # need to add in player who doesn't fold gains chips in pot
    return redirect(url)


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
