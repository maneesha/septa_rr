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
    if 'search_term_1' in request.GET and request.GET['search_term_1']:
        search_term_1 = request.GET['search_term_1'] 
        field_name_1 = request.GET['field_name_1']      
        filter_type_1 = request.GET['filter_type_1'] 
        query1 = field_name_1 + filter_type_1
        kwargs = {query1:search_term_1}   
        search_term_2 = request.GET['search_term_2'] #a is the search term
        field_name_2 = request.GET['field_name_2'] #b is the field name
        filter_type_2 = request.GET['filter_type_2'] #c is the filter type
        query2 = field_name_2 + filter_type_2  
        #if a second search term was submitted, add it to kwargs        
        if search_term_2:
            kwargs[query2]  = search_term_2
        trains = Trains.objects.filter(**kwargs).order_by('trainno', 'date_and_time')
        #__icontains and __istartswith are case-insensitive (compare to _contains & _startswith) 
        plain_english = {'__icontains':'contains', '__gt':'greater than', '__lt':'less than', '__istartswith':'starts with', '__exact':'equals'}        
        return render(request, 'search_results.html', {'trains':trains, 'query1':search_term_1, 'field1':field_name_1, 'filter1':plain_english[filter_type_1], 'query2':search_term_2, 'field2':field_name_2, 'filter2':plain_english[filter_type_2]})
    elif 'train_number_search' in request.GET and request.GET['train_number_search']:
        #return HttpResponse("You searched for: %r" % request.GET['zz'])
        train_number_search = request.GET['train_number_search']
        trainno_filter = Trains.objects.filter(trainno__exact=train_number_search)
        latest_train = trainno_filter.aggregate(Max('late'))
        lt = latest_train['late__max']
        return render(request, 'late_results.html', {'latest_train':latest_train, 'lt':lt, 'trainno':train_number_search})
    #testing passing date submission
    elif 'start_date' in request.GET and request.GET['start_date']:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        if start_date < end_date:
            message = "You searched for the start date " + start_date + " and the end date " + end_date
        else:
            message = "End date must be after start date."
        return HttpResponse(message)
    else:
        return HttpResponse("Please submit a search term") #suggestion: bring this to top so it doesn't get lost 






    
