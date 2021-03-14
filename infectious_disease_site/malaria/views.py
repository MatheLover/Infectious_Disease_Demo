from .models import Malaria
from django.db.models import Q
from django.shortcuts import render, redirect
from bokeh.embed import components
from bokeh.plotting import figure
import pandas as pd
import folium


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

        plot1 = figure(title="Number of Population at Risk by Year in " + country_filter, x_range=year_list,
                       plot_width=800, plot_height=400)
        plot1.left[0].formatter.use_scientific = False
        plot1.line(year_list, population_list, line_width=2)

        plot2 = figure(title="Number of Cases by Year in " + country_filter, x_range=year_list, plot_width=800,
                       plot_height=400)
        plot2.left[0].formatter.use_scientific = False
        plot2.vbar(year_list, width=0.5, bottom=0, top=cases_list, color="firebrick")

        plot3 = figure(title="Number of Estimated Deaths by Year in " + country_filter, x_range=year_list,
                       plot_width=800, plot_height=400)
        plot3.left[0].formatter.use_scientific = False
        plot3.line(year_list, deaths_list, line_width=2)

        script1, div1 = components(plot1)
        script2, div2 = components(plot2)
        script3, div3 = components(plot3)
        context = {'Malaria': result, 'script1': script1, 'div1': div1, 'script2': script2, 'div2': div2,
                   'script3': script3, 'div3': div3}

        return render(request, 'malaria/malaria_home.html', context)

    return render(request, 'malaria/malaria_home.html')


def malaria_map_view(request):
    return render(request, 'malaria/malaria_map.html')


def malaria_annual_stat_view(request):
    return render(request, 'malaria/malaria_annual_stat.html')


def malaria_annual_stat_map_view(request):
    year_list = []
    lat_list = []
    lon_list = []
    name_list = []
    case_map_list = []
    death_map_list = []
    pop_map_list = []
    if request.GET.get("Year") and request.GET.get("Country"):
        country_selected = request.GET.get("Country")
        year_selected = request.GET.get("Year")
        result = Malaria.objects.filter(Q(Year=year_selected) & Q(Country=country_selected))

        for m in result:
            year_list.append(m.Year)
            lat_list.append(m.Latitude)
            lon_list.append(m.Longitude)
            name_list.append(m.Country)
            case_map_list.append(m.Cases)
            death_map_list.append(m.Deaths)
            pop_map_list.append(m.Population_at_risk)

        latlon = zip(lat_list, lon_list, name_list, case_map_list, death_map_list, pop_map_list, year_list)
        zipped_latlon = list(latlon)

        map_demo = folium.Map(min_zoom=2, max_bounds=True, tiles='cartodbpositron')

        for co in zipped_latlon:
            html = """Country: """ + co[2] \
                   + """<br>Case Number in """ + str(co[6]) + """: """ + str(co[3]) \
                   + """<br>Deaths """ + str(co[6]) + """: """ + str(co[4]) \
                   + """<br>Population at risk """ + str(co[6]) + """: """ + str(co[5])

            iframe = folium.IFrame(html,
                                   width=400,
                                   height=100)

            popup = folium.Popup(iframe,
                                 max_width=500)
            folium.Marker(location=[co[0], co[1]], popup=popup).add_to(map_demo)

        map_demo.save("malaria/malaria_annual_stat_map.html")
        map_demo = map_demo._repr_html_()
        context = {
            'map_demo': map_demo
        }

        return render(request, 'malaria/malaria_annual_stat_map.html', context)

    elif request.GET.get("Year"):
        year_selected = request.GET.get("Year")
        result = Malaria.objects.filter(Year=year_selected)

        for m in result:
            year_list.append(m.Year)
            lat_list.append(m.Latitude)
            lon_list.append(m.Longitude)
            name_list.append(m.Country)

        featured_Group = folium.FeatureGroup(name="Malaria Map")
        map_demo = folium.Map(min_zoom=2, max_bounds=True, tiles='cartodbpositron')
        for lat, lon, name in zip(lat_list, lon_list, name_list):
            featured_Group.add_child(folium.Marker(location=[lat, lon], popup=name))
        map_demo.add_child(featured_Group)

        # for m in result:
        #     lat_list.append(m.Latitude)
        #     lon_list.append(m.Longitude)
        #     name_list.append(m.Country)
        #     case_map_list.append(m.Cases)
        #     death_map_list = [m.Deaths]
        #     pop_map_list = [m.Population_at_risk]
        #
        # # Combine data
        # country_case = zip(name_list, case_map_list, death_map_list, pop_map_list)
        # zipped_country_case = list(country_case)
        # df = pd.DataFrame(data=zipped_country_case, columns=['Country', 'Cases'])
        #
        # map_demo = folium.Map(min_zoom=2, max_bounds=True, tiles='cartodbpositron')
        # #map_demo.save(outfile='malaria_annual_stat_map.html')
        #
        # geojson = "/Users/benchiang/Desktop/countries.geojson"
        # g = folium.GeoJson(
        #     geojson,
        #     name=geojson
        # ).add_to(map_demo)
        #
        # # Choropleth Map
        # folium.Choropleth(
        #     geo_data=geojson,
        #     name="choropleth",
        #     data=df,
        #     columns=["Country", "Cases"],
        #     key_on="feature.properties.ADMIN",
        #     fill_color="Set2",
        #     fill_opacity=0.7,
        #     line_opacity=0.2,
        #     legend_name="Case Number",
        #     bins=6,
        #     reset=True,
        #
        # ).add_to(map_demo)

        map_demo.save("malaria/malaria_annual_stat_map.html")
        map_demo = map_demo._repr_html_()
        context = {
            'map_demo': map_demo
        }

        return render(request, 'malaria/malaria_annual_stat_map.html', context)

    return render(request, 'malaria/malaria_annual_stat_map.html')
