from django.shortcuts import render, redirect
import random
from time import gmtime, strftime

def index(request):
    if 'gold_count' not in request.session:
        request.session['gold_count'] = 0
    if 'turns' not in request.session:
        request.session['turns_to_win'] = 100
    if 'gold_to_win' not in request.session:
        request.session['winning_gold'] = 1000
        return render(request, 'index.html')
    elif int(request.session['gold_count']) >= int(request.session['winning_gold']) and int(request.session['turns_to_win']) <= int(request.session['turn_counter']):
        return redirect('/win')
    elif int(request.session['gold_count']) < int(request.session['winning_gold']) and int(request.session['turns_to_win']) < int(request.session['turn_counter']):
        return redirect('/loss')

def process_gold(request):
    if 'activity_log' not in request.session:
        request.session['activity_log'] = []
    if 'turn_counter' not in request.session:
        request.session['turn_counter'] = 1
    if request.POST['gold_acquisition_method'] == 'farm':
        farm_gold = random.randint(10, 20)
        time = strftime("%m-%d-%Y %I:%M %p")
        request.session['gold_count'] += farm_gold
        request.session['turn_counter'] += 1
        request.session['activity_log'].append(f"<p class='green'>Earned {farm_gold} gold from the farm! ({time}) </p>")

    elif request.POST['gold_acquisition_method'] == 'cave':
        cave_gold = random.randint(5, 10)
        time = strftime("%m-%d-%Y %I:%M %p")
        request.session['gold_count'] += cave_gold
        request.session['turn_counter'] += 1
        request.session['activity_log'].append(f"<p class='green'>Earned {cave_gold} gold from the cave! ({time}) </p>")

    elif request.POST['gold_acquisition_method'] == 'house':
        house_gold = random.randint(2, 5)
        time = strftime("%m-%d-%Y %I:%M %p")
        request.session['gold_count'] += house_gold
        request.session['turn_counter'] += 1
        request.session['activity_log'].append(f"<p class='green'>Earned {house_gold} gold from the house! ({time}) </p>")

    elif request.POST['gold_acquisition_method'] == 'casino':
        casino_gold = random.randint(-50, 50)
        time = strftime("%m-%d-%Y %I:%M %p")
        request.session['gold_count'] += casino_gold
        request.session['turn_counter'] += 1
        if casino_gold > 0:
            request.session['activity_log'].append(f"<p class='green'>Earned {casino_gold} gold from the casino! ({time}) </p>")
        else:
            request.session['activity_log'].append(f"<p class='red'>Oh no! You lost {casino_gold} gold from the casino! ({time}) </p>")
            if request.session['gold_count'] < 0:
                request.session['activity_log'].append(f"<p class='red'>You're in debt! You should go to casino less often. </p>")

    return redirect('/')

def reset(request):
    del request.session['gold_count']
    del request.session['activity_log']
    del request.session['winning_gold']
    del request.session['turns_to_win']
    return redirect('/')

def win_conditions(request):
    if request.method == 'GET':
        return render(request, 'win_conditions.html')
    if request.method == 'POST':
        turns_from_form = request.POST['turns']
        gold_from_form = request.POST['gold_to_win']
        request.session['turns_to_win'] = turns_from_form
        request.session['winning_gold'] = gold_from_form
        return redirect('/')

def win(request):
    return render(request, 'win.html')

def loss(request):
    return render(request, 'loss.html')