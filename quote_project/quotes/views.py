from django.shortcuts import render
from django.http import HttpResponse
from .models import Quote
import random

def aug15(request):
    return render(request, "aug15.html")

def random_quote(request):
    quotes = Quote.objects.all()
    
    if quotes.exists():
        quote = random.choice(quotes)
    else:
        quote = None
    
    return render(request, 'quotes/index.html', {'quote': quote})