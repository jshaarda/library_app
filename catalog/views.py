from django.shortcuts import render

# Create your views here.

from .models import Book

def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={'num_books': num_books, 'num_visits': num_visits},
    )

from django.views import generic

class BookListView(generic.ListView):
    """Generic class-based view for a list of books."""
    model = Book
    paginate_by = 20

class BookDetailView(generic.DetailView):
    """Generic class-based detail view for a book."""
    model = Book

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin

class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.can_mark_returned'

from django.db.models import Q
from django.views.generic import TemplateView, ListView
 
class SearchPageView(TemplateView):
    template_name = 'catalog/search_page.html'
    
class SearchResultsView(ListView):
    model = Book
    paginate_by = 20
    template_name = 'catalog/search_results.html'
    
    def get_queryset(self):
        title = self.request.GET.get('title','')
        author = self.request.GET.get('author','')
        bookcase = self.request.GET.get('bookcase','')
        shelf = self.request.GET.get('shelf','')
        genre = self.request.GET.get('genre','')
        language = self.request.GET.get('language','')
        frmt = self.request.GET.get('format','')
        other = self.request.GET.get('other','')
        object_list = Book.objects.filter(
            Q(title__icontains=title) & Q(author__icontains=author) & 
            Q(bookcase__icontains=bookcase) & Q(shelf__icontains=shelf) & 
            Q(genre__icontains=genre) & Q(language__icontains=language) & 
            Q(format__icontains=frmt) & Q(other__icontains=other)
        )
        num_results = object_list.count()
        return object_list