from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='categories')
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    name= models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price= models.DecimalField(max_digits=10,decimal_places=2)
    discount_price = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    category= models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class BookImage(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to='books')
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.book.name}"