from collections import Counter
import itertools

def Most_Common(lst):
    data = Counter(lst)
    return data.most_common(1)[0]


#gets card value from  a hand. converts A to 14,  is_seq function will convert the 14 to a 1 when necessary to evaluate A 2 3 4 5 straights
def convert_to_nums(hand):
    nums = {'1': 14}
    for x in range(len(hand)):
        if (hand[x][0]) in nums.keys():
            hand[x] = str(nums[hand[x][0]]) + hand[x][1]

    return hand

# is royal flush
# if a hand is a straight and a flush and the lowest value is a 10 then it is a royal flush
def is_royal_flush(hand):
    new_hand = convert_to_nums(hand)
    if is_seq(hand):
        if is_flush(hand):
            nn = [int(x[:-1]) for x in new_hand]
            if min(nn) == 10:
                return True
    else:
        return False
   
# converts hand to number values and then evaluates if they are sequential  
def is_seq(h):
    ace = False
    r = h[:]

    h = [x[:-1] for x in convert_to_nums(h)]


    h = [int(x) for x in h]
    h = list(sorted(h))
    ref = True
    for x in range(0,len(h)-1):
        if not h[x]+1 == h[x+1]:
            ref =  False
            break

    if ref:
        return True, h[4]

    aces = [i for i in h if str(i) == "14"]
    if len(aces) == 1:
        for x in range(len(h)):
            if str(h[x]) == "14":
                h[x] = 1

    h = list(sorted(h))
    for x in range(0,len(h)-1):
        if not h[x]+1 == h[x+1]:
            return False
    return True, h[4]

# call set() on the suit values of the hand and if it is 1 then they are all the same suit
def is_flush(h):
 suits = [x[-1] for x in h]
 if len(set(suits)) == 1:
  hand = convert_to_nums(h)
  nn = [int(x[:-1]) for x in hand]
  max_num = max(nn)
  return True, max_num
 else:
  return False


# if the most common element occurs 4 times then it is a four of a kind
def is_fourofakind(h):
 h = [a[:-1] for a in h]
 i = Most_Common(h)
 if i[1] == 4:
  return True, int(i[0])
 else:
  return False


# if the most common element occurs 3 times then it is a three of a kind
def is_threeofakind(h):
 h = [a[:-1] for a in h]
 i = Most_Common(h)
 if i[1] == 3:
  return True, int(i[0])
 else:
  return False


# if the first 2 most common elements have counts of 3 and 2, then it is a full house
def is_fullhouse(h):
 h = [a[:-1] for a in h]
 data = Counter(h)
 a, b = data.most_common(1)[0], data.most_common(2)[-1]
 if str(a[1]) == '3' and str(b[1]) == '2':
  return True, int(a[0])
 return False

# if the first 2 most common elements have counts of 2 and 2 then it is a two pair
def is_twopair(h):
 h = [a[:-1] for a in h]
 data = Counter(h)
 a, b = data.most_common(1)[0], data.most_common(2)[-1]
 if str(a[1]) == '2' and str(b[1]) == '2':
  print (a[0], b[0])
  return True, max(int(a[0]), int(b[0]))
 return False


#if the first most common element is 2 then it is a pair
def is_pair(h):
 h = [a[:-1] for a in h]
 data = Counter(h)
 a = data.most_common(1)[0]

 if str(a[1]) == '2':
  return True, int(a[0]) 
 else:
  return False

#get the high card 
def get_high(h):
 return int(list(sorted([int(x[:-1]) for x in convert_to_nums(h)], reverse =True))[0])

# # FOR HIGH CARD or ties, this function compares two hands by ordering the hands from highest to lowest and comparing each card and returning when one is higher then the other
# def compare(xs, ys):
#   xs, ys = list(sorted(xs, reverse =True)), list(sorted(ys, reverse = True))

#   for i, c in enumerate(xs):
#    if ys[i] > c:
#     return 'RIGHT'
#    elif ys[i] < c:
#     return 'LEFT'

#   return "TIE"



def get_hands(cards):
    l = list(itertools.combinations(cards, 5))
    r = [list(a) for a in l]
    return r

def evaluate(hand):
      if is_royal_flush(hand):  
           return 10, 14, hand 
      elif is_seq(hand) and is_flush(hand) :  #straight flush
           _, s_flush = is_seq(hand)
           return 9, s_flush, hand  
      elif is_fourofakind(hand):  
           _, fourofakind = is_fourofakind(hand)  
           return 8, fourofakind, hand
      elif is_fullhouse(hand): 
           _, fullhouse = is_fullhouse(hand) 
           return 7, fullhouse, hand
      elif is_flush(hand):  
           _, flush = is_flush(hand)  
           return 6, flush, hand  
      elif is_seq(hand):  #straight
           _, seq = is_seq(hand)  
           return 5, seq, hand 
      elif is_threeofakind(hand):  
           _, threeofakind = is_threeofakind(hand) 
           return 4, threeofakind, hand
      elif is_twopair(hand):  
           _, two_pair = is_twopair(hand)  
           return 3, two_pair, hand 
      elif is_pair(hand):  
           _, pair = is_pair(hand)  
           return 2, pair, hand   
      else:  
           return 1, get_high(hand), hand 

def translate(num):
    if num == 10:
        return "Royal Flush"
    elif num == 9:
        return "Straight Flush"
    elif num == 8:
        return "Four of A Kind"
    elif num == 7:
        return "Full House"
    elif num == 6:
        return "Flush"
    elif num == 5:
        return "Straight"
    elif num == 4:
        return "Three of A Kind"
    elif num == 3:
        return "Two pair"
    elif num == 2:
        return "Pair"
    else:
        return "High Card"


#best_hand and cur_hand are in format ["hand_type (in number format)", "highest card", exact hand(in list form)], ex. ["Full House", 5, hand]
def compare_hand(best_hand, cur_hand):
    if cur_hand[0] > best_hand[0]:
        return cur_hand
    elif best_hand[0] > cur_hand[0]:
        return best_hand
    else:
        if cur_hand[1] > best_hand[1]:
            return cur_hand
        else:
            #In this case, the two hands are the same, doesn't matter which hand gets returned
            return best_hand
    