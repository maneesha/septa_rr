from django.http import HttpResponse
#from django.template.loader import get_template
from django.shortcuts import render
#from django.template import Context
from regional_rail.models import Trains
from django.db.models import Max
from datetime import timedelta, datetime, date

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
    #initialize dates to be extreme range; these can be modified with user input
    start_date = '1900-01-01'
    end_date = "2020-12-31"


    if 'start_date' in request.GET and request.GET['start_date']:
    #user input to modify dates 
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        if start_date < end_date:
            message = "You searched for the start date " + start_date + " and the end date " + end_date
        else:
            message = "End date must be after start date."

    if 'search_term_1' in request.GET and request.GET['search_term_1']:
    #user input to search all trains by lateness, source, destination, and/or next stop
        search_term_1 = request.GET['search_term_1'] 
        field_name_1 = request.GET['field_name_1']      
        filter_type_1 = request.GET['filter_type_1'] 
        query1 = field_name_1 + filter_type_1
        kwargs = {query1:search_term_1}
        search_term_2 = request.GET['search_term_2'] 
        field_name_2 = request.GET['field_name_2'] 
        filter_type_2 = request.GET['filter_type_2'] 
        query2 = field_name_2 + filter_type_2  
        #if a second search term was submitted, add it to kwargs        
        if search_term_2:
            kwargs[query2]  = search_term_2

        #create django queryset called trains that filters all data by specified date range
        trains = Trains.objects.filter(date_and_time__range = [start_date, end_date])

        #filter this queryset based on user search terms
        trains = trains.filter(**kwargs).order_by('trainno', 'date_and_time')

        #dictionary to convert search types from plain english to django
        #__icontains and __istartswith are case-insensitive (compare to _contains & _startswith) 
        plain_english = {'__icontains':'contains', '__gt':'greater than', '__lt':'less than', '__istartswith':'starts with', '__exact':'equals'}        
        
        return render(request, 'search_results.html', {'trains':trains, 'query1':search_term_1, 'field1':field_name_1, 'filter1':plain_english[filter_type_1], 'query2':search_term_2, 'field2':field_name_2, 'filter2':plain_english[filter_type_2], 'start_date': start_date, 'end_date':end_date})
   
    elif 'train_number_search' in request.GET and request.GET['train_number_search']:
        train_number_search = request.GET['train_number_search']
        
        #create django queryset called latest_train that filters all data by specified date range
        latest_train = Trains.objects.filter(date_and_time__range = [start_date, end_date])

        #filter this data by trains matching specified train number
        latest_train = latest_train.filter(trainno__exact = train_number_search)

        #########
        ##NEED TO GET THE DATE THAT THIS MAX LATE VALUE HAPPENED
        #########

        #get the max value for late from this query set
        latest_train_minutes = latest_train.aggregate(Max('late')) #this is an object in the form: {'late__max': 5}
        #get just the value from that object
        latest_train_minutes = latest_train_minutes['late__max']


        return render (request, 'late_results.html', {'latest_train':latest_train, 'latest_train_minutes':latest_train_minutes, 'train_number_search': train_number_search, 'start_date':start_date, 'end_date':end_date})


    else:
        return HttpResponse("Please submit a search term") #suggestion: bring this to top so it doesn't get lost 






    
