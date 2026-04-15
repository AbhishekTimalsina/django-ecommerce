from .models import Book
from django.views.generic import TemplateView

# Create your views here.
class HomeView(TemplateView):
     model = Book
     template_name = "home.html"

class ProductDetailView(TemplateView):
     model = Book
     template_name = "details.html"

    