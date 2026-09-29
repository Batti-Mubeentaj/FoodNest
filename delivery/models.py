from django.db import models

# Create your models here.
class Customer(models.Model):
    username = models.CharField(max_length = 20)
    password = models.CharField(max_length = 20)
    email = models.CharField(max_length = 20)
    mobile = models.CharField(max_length = 10)
    address = models.CharField(max_length = 50)
    
    

class Restaurant(models.Model):
    name = models.CharField(max_length=20)

    picture = models.URLField(
        max_length=200,
        default='https://static-images.aptoide.com/_next/image?url=https%3A%2F%2Fcdn.aptoide.com%2Fimgs%2F7%2F3%2Fd%2F73d71649f84ae88f2d293d527c7541cd_icon.png&w=256&q=75'
    )

    cuisine = models.CharField(max_length=200)

    rating = models.FloatField()

    location = models.CharField(
        max_length=100,
        default='Not Available'
    )
   
    
class Item(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete = models.CASCADE, related_name = "items")
    name = models.CharField(max_length = 20)
    description = models.CharField(max_length = 200)
    price = models.FloatField()
    vegeterian = models.BooleanField(default=False)
    picture = models.URLField(max_length = 400, default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR6Mf4WedoB3ya_4tixHXsNmpyb6FeqF8oy-K68AJgfjA&s') 
    
class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE, related_name = "cart")
    items = models.ManyToManyField("Item", related_name = "carts")

    def total_price(self):
        return sum(item.price for item in self.items.all())
            