from django.db import models

# Django adds this default id if pk is not defined => id = models.AutoField(primary_key=True)

class Customer(models.Model):
    id = models.AutoField(primary_key=True) # Id (int)
    name = models.CharField(max_length=100, null=False, blank=False) # Ad (varchar)
    surname = models.CharField(max_length=100, null=False, blank=False) # Soyad (varchar)
    city = models.CharField(max_length=100, null=False, blank=False) # Sehir (varchar)

    def __str__(self):
        return "Customer's ID = " + str(self.id) + ", Name = " + self.name \
            + ", Surname = " + self.surname + ", City = " + self.city

class Basket(models.Model):
    id = models.AutoField(primary_key=True) # Id (int)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE) # MusteriId (int)

    def __str__(self):
        return "Basket's ID = " + str(self.id) + ", CustomerID = " + str(self.customer_id)

class BasketProduct(models.Model):
    id = models.AutoField(primary_key=True) # Id (int)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE) # SepetId (int)
    cost = models.DecimalField(max_digits=11, decimal_places=2, null=False) # Tutar (numeric)
    description = models.TextField(default="No description.") # Aciklama (varchar)

    def __str__(self):
        return "BasketProduct's ID = " + str(self.id) + ", BasketID = " + str(self.basket_id) \
            + ", Cost = " + str(self.cost) + ", Description = " + self.description
