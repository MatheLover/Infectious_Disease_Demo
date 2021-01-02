from .models import Malaria
from django.db.models import Q
from django.shortcuts import render
from bokeh.embed import components
from bokeh.plotting import figure

# Create your views here.
def malaria_home_view(request):
    if request.GET.get("Country"):
        country_filter = request.GET.get("Country")
        startyear_filter = request.GET.get("starting_year")
        endyear_filter = request.GET.get("end_year")
        result = Malaria.objects.filter(Q(Country=country_filter) & Q(Year__gte=startyear_filter)
                                        & Q(Year__lte=endyear_filter))

        # Create a list to hold the years that have been chosen
        year_list = []
        startyear_int_form = int(startyear_filter)
        endyear_int_form = int(endyear_filter)
        for year in range(startyear_int_form, endyear_int_form + 1):
            year_str_form = str(year)
            year_list.append(year_str_form)

        # Prepare data for the graphs
        population_list = []
        cases_list = []
        deaths_list = []

        for population in result.values_list('Population_at_risk'):
            population_list.append(population)

        for case in result.values_list('Cases'):
            cases_list.append(case)

        for death in result.values_list('Deaths'):
            deaths_list.append(death)

        plot1 = figure(x_range=year_list, plot_width=800, plot_height=400)
        plot1.line(year_list, population_list, line_width=2)
        plot2 = figure(x_range=year_list, plot_width=800, plot_height=400)
        plot2.line(year_list, cases_list, line_width=2)
        plot3 = figure(x_range=year_list, plot_width=800, plot_height=400)
        plot3.line(year_list, deaths_list, line_width=2)
        script, div = components({"Population_at_risk": plot1, "Cases": plot2, "Deaths": plot3})
        return render(request, 'malaria/malaria_home.html', {"Malaria": result, 'script': script, 'div': div})

    else:
        result = Malaria.objects.all()

    return render(request, 'malaria/malaria_home.html', {"Malaria": result})
