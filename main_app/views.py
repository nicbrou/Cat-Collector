from django.shortcuts import redirect, render
# from django.http import HttpResponse
from .models import Cat, Toy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import FeedingForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
import os

class CatCreate(CreateView):
    model = Cat 
    fields = ['name', 'breed', 'description', 'age', 'image']
    # success_url = '/cats/'
    # IF you want to dsiplay specific fields code like this: fields = ['name']

    def form_valid(self, form):
        # After Submitting the form, and before commiting to the database
        form.instance.user = self.request.user 
        return super().form_valid(form)

def home(request):
    print(os.getenv('NAME'))
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def cat_index(request):
    cats = Cat.objects.all()
    # SELECT * from Cat
    return render(request, 'cats/index.html', { 'cats': cats })

def cats_detail(request, cat_id):
  cat = Cat.objects.get(id=cat_id)
  # Get the toys the cat doesn't have
  toys_cat_doesnt_have = Toy.objects.exclude(id__in = cat.toys.all().values_list('id'))
  
  feeding_form = FeedingForm()
  return render(request, 'cats/detail.html', {
    'cat': cat, 'feeding_form': feeding_form,
    # Add the toys to be displayed
    'toys': toys_cat_doesnt_have
  })

def add_feeding(request, cat_id):
    print("I'm in add feeding")
    print(request.POST)
    form = FeedingForm(request.POST)
    print(form)
    if form.is_valid():
        print("I'm valid")
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = cat_id
        new_feeding.save()
    return redirect('detail', cat_id = cat_id)

class CatUpdate(UpdateView):
    model = Cat
    fields = ['breed', 'description', 'age']

class CatDelete(DeleteView):
    model = Cat
    success_url = '/cats/'

class ToyList(ListView):
    model = Toy

class ToyDetails(DetailView):
    model = Toy 

class ToyCreate(CreateView):
    # create a form.html for create and update
    model = Toy 
    fields = '__all__'

class ToyUpdate(UpdateView):
    model = Toy 
    fields = '__all__'

class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'

def assoc_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('detail', cat_id=cat_id)

def unassoc_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.remove(toy_id)
    return redirect('detail', cat_id=cat_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the user to the database, see below:
            user = form.save()
            # Then login the user
            login(request, user)
            return redirect('index')
        else:
            error_message = "Invalid Sign Up. Try Again!"
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

