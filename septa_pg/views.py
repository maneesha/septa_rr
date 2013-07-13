from django.http import HttpResponse
#from django.template.loader import get_template
from django.shortcuts import render
#from django.template import Context
from regional_rail.models import Trains
from django.db.models import Max

def search_form(request):
    return render(request, 'search_form.html')

def search_x(request):
    #to have only one search term & hard-coded filter
    #as an example only - not used in this project/app
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        trains = Trains.objects.filter(source__icontains=q)
        return render(request, 'search_results.html', {'trains':trains, 'query':q})
    else:
        return HttpResponse("please submit a search term")
   

def search(request):
    #is this the best way to have multiple search terms?
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q'] #q is the search term
        w = request.GET['w'] #w is the field name       
        x = request.GET['x'] #x is filter type
        query1 = w + x
        kwargs = {query1:q}   
        a = request.GET['a'] #a is the search term
        b = request.GET['b'] #b is the field name
        c = request.GET['c'] #c is the filter type
        query2 = b + c  
        #if a second search term was submitted, add it to kwargs        
        if a:
            kwargs[query2]  = a
        trains = Trains.objects.filter(**kwargs)
        #__icontains and __istartswith are case-insensitive (compare to _contains & _startswith) 
        plain_english = {'__icontains':'contains', '__gt':'greater than', '__lt':'less than', '__istartswith':'starts with', '__exact':'equals'}        
        return render(request, 'search_results.html', {'trains':trains, 'query1':q, 'field1':w, 'filter1':plain_english[x], 'query2':a, 'field2':b, 'filter2':plain_english[c]})
    elif 'zz' in request.GET and request.GET['zz']:
        #return HttpResponse("You searched for: %r" % request.GET['zz'])
        zz = request.GET['zz']
        trainno_filter = Trains.objects.filter(trainno__exact=zz)
        latest_train = trainno_filter.aggregate(Max('late'))
        lt = latest_train['late__max']
        return render(request, 'late_results.html', {'latest_train':latest_train, 'lt':lt, 'trainno':zz})
    else:
        return HttpResponse("Please submit a search term") #suggestion: bring this to top so it doesn't get lost 






    
