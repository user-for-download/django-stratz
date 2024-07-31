from django.views.generic import ListView

from dj.heroes.models import Hero


# Create your views here.


class HeroesListView(ListView):
    model = Hero
    paginate_by = 25


heroes_list_view = HeroesListView.as_view()
