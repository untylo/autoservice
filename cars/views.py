from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import *
from .forms import *

def home(request):
    return render(request, 'base.html')
def brand_list(request):
    brands = Brand.objects.all()
    return render(request, 'brand.html', {'brands': brands})
def brand_add(request):
    if request.method == "POST":
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('brand_list')
    else:
        form = BrandForm()
    return render(request, 'brand_add.html', {'form': form})
def model_add(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    if request.method == "POST":
        form = CarModelForm(request.POST)
        if form.is_valid():
            model = form.save(commit=False)
            model.brand = brand
            model.save()
            return redirect('brand_list')
    else:
        form = CarModelForm()
    return render(request, 'model_add.html', {'form': form, 'brand': brand})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Client, Car
from .forms import ClientForm, CarForm

def client_list(request):
    clients = Client.objects.prefetch_related("cars").all()
    return render(request, 'client.html', {'clients': clients})

def client_add(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'client_add.html', {'form': form})

def car_add(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == "POST":
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.client = client
            car.save()
            return redirect('client_list')
    else:
        form = CarForm()
    return render(request, 'car_add.html', {'form': form, 'client': client})

def load_models(request):
    brand_id = request.GET.get('brand')
    models = CarModel.objects.filter(brand_id=brand_id).values('id', 'name')
    return JsonResponse(list(models), safe=False)


