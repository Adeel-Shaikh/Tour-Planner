from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from numpy.core.numeric import full
import pandas as pd
from django.http import JsonResponse
from .models import TravelPlans
from shortest_path import Graph
from apriori_result import *
from datetime import datetime
from django.urls import reverse
import calendar
from explore_time import time_list
from datetime import timedelta
import numpy as np

        

# Create your views here.

def HomeView(request):
    csv=pd.read_csv('places.csv')
    df=pd.DataFrame(csv)
    autocomplete=[]
    for i in range(len(df['countries'])):
        autocomplete.append(df['countries'][i])
    
    context={
        'autocomplete':autocomplete,
    }
    return render(request,'homepage/home.html',context)

def SearchResultView(request):
    search_key=request.GET.get('q','')
    
    places=[]
    places_nodes=[]
    df=pd.read_csv('places.csv')
    for i in range(len(df)):
        if df.iloc[i].city==search_key:
            places.append(df.iloc[i])
            places_nodes.append(i)
    nearby=zip(places_nodes,places)
    nearby=tuple(nearby)

    visited_list=TravelPlans.objects.filter(user=request.user)
    visited_places=[]
    for i in visited_list:
        visited_places.append(i.place_id)

    context={
        'search_key':search_key,
        'nearby_places':nearby,
        'visited_places':visited_places,
    }
    return render(request,'homepage/search_result.html',context)

def ListofAddedPlaces(request):
    visited_list=TravelPlans.objects.filter(user=request.user)
    df=pd.read_csv('places.csv')
    visited_places=[]
    for i in visited_list:
        visited_places.append(df.iloc[i.place_id])
    context={
        'visited_places':visited_places,
    }
    return render(request,'homepage/list_of_places.html',context)
    
def AddTravelPlace(request,id,place):
    #exists=TravelPlans.objects.filter(user=request.user,place_id=id)
    print(place)
    saveit=TravelPlans(user=request.user,place_id=id)
    saveit.save()
    return redirect(reverse('search-result')+'?q=Mumbai')

def AddTravelFromRecomm(request,id):
    saveit=TravelPlans(user=request.user,place_id=id)
    saveit.save()
    return redirect('list-of-places')

def PlacesListView(request):
    place=TravelPlans.objects.filter(user=request.user)
    csv=pd.read_csv('places.csv')
    places=[]
    antecedents=[]
    for i in place:
        antecedents.append(i.place_id)
        places.append(csv.loc[i.place_id])
    sp=AprioriReturns(antecedents)
    suggested_places=[]
    df1=pd.read_csv('travel_matrix.csv')
    near_places=[]
    near_nodes=[]
    for i in place:
        for indx,j in enumerate(df1.iloc[i.place_id][1:]):
            if j<12 and j!=0.0:
                if indx not in antecedents:
                    near_nodes.append(indx)

    for i in near_nodes[:3]:
        near_places.append(csv.iloc[i])
    nearby=zip(near_nodes,near_places)
    nearby=tuple(nearby)
    for i in sp:
        suggested_places.append(csv.loc[int(i)])
    recommends=zip(sp,suggested_places)
    recommends=tuple(recommends)
    context={
        'places':places,
        'recommends':recommends,
        'nearby':nearby,
    }
    return render(request,'homepage/added_places.html',context)



def solve(s, minutes):
    time_instance = datetime.strptime(s, '%I:%M%p')
    time_instance += timedelta(minutes=minutes)
    return time_instance.strftime('%I:%M%p').lower()

def find_time(path):
    df=pd.read_csv('places.csv')
    df1=pd.read_csv('travel_matrix.csv')
    car_time=[]
    for i in range(len(path)):
        if i==len(path)-1:
            car_time.append('')
        else:
            car_time.append((round((int(df1.iloc[path[i]][path[i+1]+1])*3)/10)*10)+10)

    spend_time=[]
    for i in range(len(path)):
        spend_time.append(int(df.iloc[path[i]]['time_spent']))

    start_time="10:00am"
    explore_time=[]
    for i in range(len(spend_time)):
        if i==0:
            explore_time.append([start_time,solve(start_time,spend_time[i])])
        else:
            strt=solve(explore_time[i-1][1],round(car_time[i-1]))
            explore_time.append([strt,solve(strt,spend_time[i])])
    return car_time,explore_time

def RoutePageView(request):
    start_point=request.GET.get('start','')
    start_date=request.GET.get('date','')
    
    try:
        date=datetime(int(start_date[:4]),int(start_date[5:7]),int(start_date[8:10]))
        day=date.strftime('%A')[:3]+", "+start_date[8:10]+" "+date.strftime("%B")
    except:
        date=""
        day=""
    
    
    places=TravelPlans.objects.filter(user=request.user)
    csv=pd.read_csv('places.csv')
    header=csv.iloc[places[0].place_id].city
    edges=[]
    for i in places:
        edges.append(i.place_id)
    if start_point:
        g=Graph(edges)
        path,cost=g.get_shortest(int(start_point))
        print(cost)
        #print(time_list([path]))
        #print(solve('10:00am',45))
 
        travel_path=[]
        for i in path:
            travel_path.append(csv.loc[i])
    else:
        travel_path=[]
    
    option_box_path=[]
    for i in edges:
        option_box_path.append(csv.loc[i])

    start_point_options=zip(edges,option_box_path)
    start_point_options=tuple(start_point_options)

    #for time 
    
    if travel_path:
        car_time,explore_time=find_time(path)
        """  print(explore_time)
        for indx,i in enumerate(explore_time):
            if i[0][5:]=='pm':
                if int(i[0][:2])>7 and  int(i[0][:2])!=12:
                        message=True """
        print(len(car_time),len(explore_time),len(travel_path))
        full_key=zip(travel_path,car_time,explore_time)
        full_key=tuple(full_key)
        #print(full_key)
    else:
        full_key=tuple()


    context={
        'travel_path':travel_path,
        'start_point_options':start_point_options,
        'day':day,
        'header':header,
        'full_key':full_key,
    }
    return render (request,'homepage/route.html',context)

