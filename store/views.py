from .models import Book, Category
from django.views.generic import ListView, TemplateView, DetailView
from django.db.models import Q

# Create your views here.
class HomeView(ListView):
     model = Book
     template_name = "home.html"

class ProductDetailView(DetailView):
     model = Book
     template_name = "details.html"


class ExploreView(ListView):
     model = Book
     template_name = "explore.html"
     context_object_name = "books"
     paginate_by = 12

     def get_queryset(self):
          qs = Book.objects.all()

          query = self.request.GET.get("q", "").strip()
          if query:
               qs = qs.filter(
                    Q(name__icontains=query) |
                    Q(description__icontains=query)
               ).distinct()

          genre = self.request.GET.get("genre")
          if genre:
               qs = qs.filter(category__slug=genre)


          min_price = self.request.GET.get("min_price")
          max_price = self.request.GET.get("max_price")
          if min_price:
               try:
                    qs = qs.filter(price__gte=float(min_price))
               except ValueError:
                    pass
          if max_price:
               try:
                    qs = qs.filter(price__lte=float(max_price))
               except ValueError:
                    pass

          sort = self.request.GET.get("sort", "name")
          sort_options = {
               "name": "name",
               "price_low": "price",
               "price_high": "-price",
               "newest": "-id",
          }
          qs = qs.order_by(sort_options.get(sort, "name"))

          return qs

     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          context["categories"] = Category.objects.all()
          context["current_query"] = self.request.GET.get("q", "").strip()
          context["current_genre"] = self.request.GET.get("genre", "")
          context["current_min_price"] = self.request.GET.get("min_price", "")
          context["current_max_price"] = self.request.GET.get("max_price", "")
          context["current_sort"] = self.request.GET.get("sort", "name")
          context["total_results"] = self.get_queryset().count()
          return context