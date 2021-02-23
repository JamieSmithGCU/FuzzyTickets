from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from datetime import datetime


VENUE_CHOICES = (
    ('O2 Academy', 'O2 Academy'),
    ('King Tuts', 'King Tuts'),
    ('Glasgow Green', 'Glasgow Green'),
    ('Hampden Park', 'Hampden Park'),
)

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    venue = models.CharField(choices=VENUE_CHOICES, max_length=50)
    slug = models.SlugField()
    description = models.TextField()
    photo = models.ImageField()
    date = models.DateField(default=datetime.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })

class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price
    

class Order(models.Model):
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add = True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default = False)
    
    def __str__(self):
        return str(self.items)
    
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total
