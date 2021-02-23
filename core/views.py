from django.shortcuts import render, get_object_or_404
from .models import Item, OrderItem, Order
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
from .forms import CheckoutForm
from django.core.exceptions import ObjectDoesNotExist
import urllib

import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

# Create your views here.
class HomeView(ListView):
    model = Item
    template_name = 'home.html'


class ItemDetailView(DetailView):
    model = Item 
    template_name = 'product.html'


def product(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'product.html', context)

def checkout(request):
    return render(request, 'checkout.html')


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        ordered=False)
    order_qs = Order.objects.filter(ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request, 'This item quantity was updated.')
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.success(request, 'This item was added to your cart.')
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, 'This item was added to your cart.')
        return redirect("core:order-summary")


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                ordered=False)[0] 
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, 'This item was removed from your cart.')
            return redirect('core:product', slug=slug)
        else:
            # Add a message saying the order does not exist
            messages.warning(request, 'This item was not in your your cart.')
            return redirect('core:product', slug=slug)
    else:
        # Add a message saying the user doesn't have an order
        messages.info(request, 'You do not have an active order.')
        return redirect('core:product', slug=slug)


class OrderSummaryView(View):
    def get(self, *arg, **kwargs):
        try:
            order = Order.objects.get(ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order.")
            return redirect("/")


def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)
    
class CheckoutView(View):
    def get(self, *args, **kwardgs):
        # form
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, 'checkout.html', context)


    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        print(self.request.POST)
        print("xxxxxxxx")
        if form.is_valid():
            print(form.cleaned_data)
            print('The form is valid.')

            # New Antecedent/Consequent objects hold universe variables and membership
            # functions
            Level_Of_Loyalty = ctrl.Antecedent(np.arange(0, 6, 1), 'Level of Loyalty')
            Merchandise_Purchased = ctrl.Antecedent(np.arange(0, 6, 1), 'Merchandise Purchased')
            Remaining_Tickets = ctrl.Antecedent(np.arange(0, 6, 1), 'Remaining Tickets')
            Discount_Amount = ctrl.Consequent(np.arange(0, 16, 1), 'Discount Amount')
            # Auto-membership function population is possible with .automf(3, 5, or 7)
            # x_Level_Of_Loyalty.automf(3)
            Level_Of_Loyalty['Low'] = fuzz.gaussmf(Level_Of_Loyalty.universe, -2.776e-17, 1.062)
            Level_Of_Loyalty['Medium'] = fuzz.gaussmf(Level_Of_Loyalty.universe, 2.5, 1.062)
            Level_Of_Loyalty['High'] = fuzz.gaussmf(Level_Of_Loyalty.universe, 6, 1.062)

            # x_Merchandise_Purchased.automf(3)
            Merchandise_Purchased['None'] = fuzz.gaussmf(Merchandise_Purchased.universe, 2.776e-17, 0.8846)
            Merchandise_Purchased['Some'] = fuzz.gaussmf(Merchandise_Purchased.universe, 2.5, 0.8846)
            Merchandise_Purchased['Alot'] = fuzz.gaussmf(Merchandise_Purchased.universe, 6, 0.8846)

            # x_Remaining_Tickets.automf(3)
            Remaining_Tickets['Low'] = fuzz.gaussmf(Remaining_Tickets.universe, -6.94e-17, 0.8845)
            Remaining_Tickets['Medium']= fuzz.gaussmf(Remaining_Tickets.universe, 2.5, 0.8845)
            Remaining_Tickets['High'] = fuzz.gaussmf(Remaining_Tickets.universe, 6, 0.8845)

            # Custom membership functions can be built interactively with a familiar,
            # Pythonic API
            Discount_Amount['None'] = fuzz.trapmf(Discount_Amount.universe, [-3.38, -0.375, 0, 0])
            Discount_Amount['Low'] = fuzz.trapmf(Discount_Amount.universe, [0, 3.38, 4.12, 7.12])
            Discount_Amount['Medium'] = fuzz.trapmf(Discount_Amount.universe, [4.125, 7.125, 7.875, 10.88])
            Discount_Amount['High'] = fuzz.trapmf(Discount_Amount.universe, [7.875, 10.88, 11.62, 14.62])
            Discount_Amount['Very High'] = fuzz.trapmf(Discount_Amount.universe, [11.6, 14.984693877551, 15.4, 18.4])
            
            ## Rules
            rule1 = ctrl.Rule(Level_Of_Loyalty['Low'] & Merchandise_Purchased['None'] & Remaining_Tickets['High'], Discount_Amount['Low'])
            rule2 = ctrl.Rule(Level_Of_Loyalty['Low'] & Merchandise_Purchased['None'] & Remaining_Tickets['Medium'], Discount_Amount['None'])

            rule3 = ctrl.Rule(Level_Of_Loyalty['Low'] & Merchandise_Purchased['None'] & Remaining_Tickets['Low'], Discount_Amount['None'])

            rule4 = ctrl.Rule(Level_Of_Loyalty['Low'] & Merchandise_Purchased['Some'] & Remaining_Tickets['High'], Discount_Amount['Medium'])

            rule5 = ctrl.Rule(Level_Of_Loyalty['Low'] & Merchandise_Purchased['Some'] & Remaining_Tickets['Medium'], Discount_Amount['Low'])

            rule6 = ctrl.Rule(Level_Of_Loyalty['Low'] & Merchandise_Purchased['Some'] & Remaining_Tickets['Low'], Discount_Amount['Low'])

            rule7 = ctrl.Rule(Level_Of_Loyalty['Low'] & Merchandise_Purchased['Alot'] & Remaining_Tickets['High'], Discount_Amount['Medium'])

            rule8 = ctrl.Rule(Level_Of_Loyalty['Low'] & Merchandise_Purchased['Alot'] & Remaining_Tickets['Medium'], Discount_Amount['Low'])

            rule9 = ctrl.Rule(Level_Of_Loyalty['Low'] & Merchandise_Purchased['Alot'] & Remaining_Tickets['Low'], Discount_Amount['Low'])

            rule10 = ctrl.Rule(Level_Of_Loyalty['Medium'] & Merchandise_Purchased['None'] & Remaining_Tickets['Low'], Discount_Amount['Low'])

            rule11 = ctrl.Rule(Level_Of_Loyalty['Medium'] & Merchandise_Purchased['None'] & Remaining_Tickets['Medium'], Discount_Amount['Medium'])

            rule12 = ctrl.Rule(Level_Of_Loyalty['Medium'] & Merchandise_Purchased['None'] & Remaining_Tickets['High'], Discount_Amount['Medium'])

            rule13 = ctrl.Rule(Level_Of_Loyalty['Medium'] & Merchandise_Purchased['Some'] & Remaining_Tickets['Low'], Discount_Amount['Low'])

            rule14 = ctrl.Rule(Level_Of_Loyalty['Medium'] & Merchandise_Purchased['Some'] & Remaining_Tickets['Medium'], Discount_Amount['Medium'])

            rule15 = ctrl.Rule(Level_Of_Loyalty['Medium'] & Merchandise_Purchased['Some'] & Remaining_Tickets['High'], Discount_Amount['High'])

            rule16 = ctrl.Rule(Level_Of_Loyalty['Medium'] & Merchandise_Purchased['Alot'] & Remaining_Tickets['Low'], Discount_Amount['Low'])

            rule17 = ctrl.Rule(Level_Of_Loyalty['Medium'] & Merchandise_Purchased['Alot'] & Remaining_Tickets['Medium'], Discount_Amount['Medium'])

            rule18 = ctrl.Rule(Level_Of_Loyalty['Medium'] & Merchandise_Purchased['Alot'] & Remaining_Tickets['High'], Discount_Amount['High'])

            rule19 = ctrl.Rule(Level_Of_Loyalty['High'] & Merchandise_Purchased['None'] & Remaining_Tickets['Low'], Discount_Amount['Medium'])

            rule20 = ctrl.Rule(Level_Of_Loyalty['High'] & Merchandise_Purchased['None'] & Remaining_Tickets['Medium'], Discount_Amount['Medium'])

            rule21 = ctrl.Rule(Level_Of_Loyalty['High'] & Merchandise_Purchased['None'] & Remaining_Tickets['High'], Discount_Amount['High'])

            rule22 = ctrl.Rule(Level_Of_Loyalty['High'] & Merchandise_Purchased['Some'] & Remaining_Tickets['Low'], Discount_Amount['Medium'])

            rule23 = ctrl.Rule(Level_Of_Loyalty['High'] & Merchandise_Purchased['Some'] & Remaining_Tickets['Medium'], Discount_Amount['High'])

            rule24 = ctrl.Rule(Level_Of_Loyalty['High'] & Merchandise_Purchased['Some'] & Remaining_Tickets['High'], Discount_Amount['Very High'])

            rule25 = ctrl.Rule(Level_Of_Loyalty['High'] & Merchandise_Purchased['Alot'] & Remaining_Tickets['Low'], Discount_Amount['High'])

            rule26 = ctrl.Rule(Level_Of_Loyalty['High'] & Merchandise_Purchased['Alot'] & Remaining_Tickets['Medium'], Discount_Amount['Very High'])

            rule27 = ctrl.Rule(Level_Of_Loyalty['High'] & Merchandise_Purchased['Alot'] & Remaining_Tickets['High'], Discount_Amount['Very High'])

            discount_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27])
            discount = ctrl.ControlSystemSimulation(discount_ctrl)

            # Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
            discount.input['Level of Loyalty'] = float(form.cleaned_data['level_of_loyalty'])
            discount.input['Merchandise Purchased'] = float(form.cleaned_data['merchandise_purchased'])
            discount.input['Remaining Tickets'] = float(form.cleaned_data['remaining_tickets'])

            # Crunch the numbers
            discount.compute()

            # Get order
            order = Order.objects.get(ordered=False)

            order_total = order.get_total()

            # Discount percentage determined by FL model
            discount_percent = discount.output['Discount Amount'].round(2)
            total_discount = (order.get_total() / 100) * discount_percent
            total_discount = total_discount.round(2)

            # Calculate final price
            final_price = order.get_total() - total_discount.round(2)

            # print(discount.output['Discount Amount'].round(2))

            context = {
                'final_price': final_price,
                'discount_percent': discount_percent,
                'total_discount': total_discount,
                'order_total': order_total
            }

            # return HttpResponseRedirect('confirm_purchase.html', context)
            # return redirect('confirm_purchase.html' + context)
            # return redirect('confirm_purchase.html' + urllib.parse.urlencode(context))
            return render(self.request, 'confirm_purchase.html', context)
        messages.warning(self.request, "Failed checkout")
        return redirect('core:checkout')


def confirm_purchase(request):
    context = {
                'final_price': final_price
            }
    return render(request, 'confirm_purchase.html', context)