from django.views.generic import CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from .forms import * 
from django.contrib.auth.decorators import login_required
from .models import *
from django.urls import reverse

def home(request):
    return render(request, 'home.html')

def base(request):
    return render(request, 'base.html')

class UserSignupView(CreateView):
    model = User
    form_class = UserSignupForm
    template_name = 'user_signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/login')
    
class UserLoginView(LoginView):
    template_name='login.html'

def logout_user(request):
    logout(request)
    return redirect("/")

@login_required(login_url='/login')
def account(request):
    return render(request, 'account.html')

@login_required(login_url="/login")
def orderhistory(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_time')
    return render(request, 'orderhistory.html', {'orders': orders})

@login_required(login_url='/login')
def createorder(request):
    pizza = None
    if request.method == "POST":
        form = PizzaOrder(request.POST)
        if form.is_valid():
            pizza = form.save(commit=False)
            pizza.user = request.user
            pizza.save()
            form.save_m2m()

            return redirect('/payment')
    else:
        form = PizzaOrder()

    return render(request, 'createorder.html', {'form': form, 'pizza': pizza})

@login_required(login_url='/login')
def payment(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            latest_pizza = Pizza.objects.filter(user=request.user).order_by('-id').first()
            if latest_pizza:
                order.pizza = latest_pizza
            else:
                 return render(request, 'payment.html', {'form': form, 'error': 'No pizza found! Please create a pizza first.'})
            order.save()
            return redirect('order_summary')
    else:
        form = OrderForm()

    return render(request, 'payment.html', {'form': form})

@login_required(login_url='/login')
def order_summary(request):
    order = Order.objects.filter(user=request.user).order_by('-order_time').first()
    pizza = order.pizza
    return render(request, 'order_summary.html', {'order': order, 'pizza': order.pizza})