from django.shortcuts import render

from django.views.generic import TemplateView, ListView

from .models import Anime

from django.db.models import Q #import Q objects for QuerySet
# Create your views here.

class HomePageView(TemplateView):
	template_name = "home.html"

class SearchResultsView(ListView):
	model = Anime
	template_name = 'search_results.html'

	def get_queryset(self): #this will use the query we send from the form to query the results in
	#our database
	
		query = self.request.GET.get('query')
		object_list = Anime.objects.filter(
			Q(name__icontains=query))
		
		return object_list
