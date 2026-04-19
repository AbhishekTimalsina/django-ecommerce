from .models import Book
from django.views.generic import ListView, TemplateView, DetailView

# Create your views here.
class HomeView(ListView):
     model = Book
     template_name = "home.html"

class ProductDetailView(DetailView):
     model = Book
     template_name = "details.html"

    