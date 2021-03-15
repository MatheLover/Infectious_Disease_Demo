from .models import Malaria
from django.db.models import Q
from django.shortcuts import render, redirect
from bokeh.embed import components
from bokeh.plotting import figure
import pandas as pd
import folium
import branca.colormap as cm
import geopandas as gpd
import numpy as np

from datetime import datetime, timedelta



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



        map_demo.save("malaria/malaria_annual_stat_map.html")
        map_demo = map_demo._repr_html_()
        context = {
            'map_demo': map_demo
        }

        return render(request, 'malaria/malaria_annual_stat_map.html', context)

    return render(request, 'malaria/malaria_annual_stat_map.html')

def malaria_cumulative_stat_view(request):
    return render(request, 'malaria/malaria_cumulative_stat.html')

def malaria_cumulative_stat_map_view(request):
    obtained_feature = request.GET.get("Feature")
    if obtained_feature == "Cases":
        slider_name_list = []
        slider_case_list = []
        slider_lat_list = []
        slider_lon_list = []
        slider_year_list = []

        for m in Malaria.objects.all():
            slider_lat_list.append(m.Latitude)
            slider_lon_list.append(m.Longitude)
            slider_name_list.append(m.Country)
            slider_case_list.append(m.Cases)
            year = str(m.Year)
            if year != '2010':
                year = year + '/12/31'
            slider_year_list.append(year)

        country_case = zip(slider_name_list, slider_case_list, slider_year_list)
        slider_zipped_country_case = list(country_case)
        df_slider = pd.DataFrame(data=slider_zipped_country_case, columns=['Country', 'Cases', 'Year'])
        df_slider = df_slider[df_slider.Cases != 0]

        # sorting
        sorted_df = df_slider.sort_values(['Country',
                                           'Year']).reset_index(drop=True)

        # Combine data with the file
        country = gpd.read_file("/Users/benchiang/Desktop/countries.geojson")
        country = country.rename(columns={'ADMIN': 'Country'})
        combined_df = sorted_df.merge(country, on='Country')
        # print(combined_df)

        # Use Log to plot the cases
        combined_df['log_cases'] = np.log10(combined_df['Cases'])
        combined_df = combined_df[['Country', 'log_cases', 'Year', 'geometry']]
        # print(combined_df)

        combined_df['Year'] = pd.to_datetime(combined_df['Year']).astype(int) / 10 ** 9
        combined_df['Year'] = combined_df['Year'].astype(int).astype(str)

        # Construct color map
        max_color = max(combined_df['log_cases'])
        min_color = min(combined_df['log_cases'])
        color_map = cm.linear.YlOrRd_09.scale(min_color, max_color)
        combined_df['color'] = combined_df['log_cases'].map(color_map)
        # print(combined_df)

        # Construct style dictionary
        unique_country_list = combined_df['Country'].unique().tolist()
        ctry_index = range(len(unique_country_list))

        style_dic = {}
        for j in ctry_index:
            ctry = unique_country_list[j]
            country = combined_df[combined_df['Country'] == ctry]
            in_dic = {

            }
            for _, r in country.iterrows():
                in_dic[r['Year']] = {'color': r['color'], 'opacity': 0.8}
            style_dic[str(j)] = in_dic

        # Make a dataframe containing each country
        specific_ctry = combined_df[['geometry']]
        ctry_gdf = gpd.GeoDataFrame(specific_ctry)
        ctry_gdf = ctry_gdf.drop_duplicates().reset_index()

        # Create a slider map
        from folium.plugins import TimeSliderChoropleth
        m = folium.Map(min_zoom=2, max_bounds=True, tiles='cartodbpositron')

        # Plot Slider Map
        _ = TimeSliderChoropleth(
            data=ctry_gdf.to_json(),
            styledict=style_dic,
        ).add_to(m)
        _ = color_map.add_to(m)
        color_map.caption = "Log number of malaria cases"


        m.save("malaria/malaria_cumulative_stat_map.html")
        m = m._repr_html_()
        context = {
            'm': m
        }


        return render(request, 'malaria/malaria_cumulative_stat_map.html', context)

    elif obtained_feature == "Population_at_risk":
        slider_name_list = []
        slider_pop_list = []
        slider_lat_list = []
        slider_lon_list = []
        slider_year_list = []

        for m in Malaria.objects.all():
            slider_lat_list.append(m.Latitude)
            slider_lon_list.append(m.Longitude)
            slider_name_list.append(m.Country)
            slider_pop_list.append(m.Population_at_risk)
            year = str(m.Year)
            if year != '2010':
                year = year + '/12/31'
            slider_year_list.append(year)

        country_case = zip(slider_name_list, slider_pop_list, slider_year_list)
        slider_zipped_country_case = list(country_case)
        df_slider = pd.DataFrame(data=slider_zipped_country_case, columns=['Country', 'Population_at_risk', 'Year'])
        df_slider = df_slider[df_slider.Population_at_risk != 0]

        # sorting
        sorted_df = df_slider.sort_values(['Country',
                                           'Year']).reset_index(drop=True)

        # Combine data with the file
        country = gpd.read_file("/Users/benchiang/Desktop/countries.geojson")
        country = country.rename(columns={'ADMIN': 'Country'})
        combined_df = sorted_df.merge(country, on='Country')
        # print(combined_df)

        # Use Log to plot the cases
        combined_df['log_pop'] = np.log10(combined_df['Population_at_risk'])
        combined_df = combined_df[['Country', 'log_pop', 'Year', 'geometry']]
        # print(combined_df)

        combined_df['Year'] = pd.to_datetime(combined_df['Year']).astype(int) / 10 ** 9
        combined_df['Year'] = combined_df['Year'].astype(int).astype(str)

        # Construct color map
        max_color = max(combined_df['log_pop'])
        min_color = min(combined_df['log_pop'])
        color_map = cm.linear.YlOrRd_09.scale(min_color, max_color)
        combined_df['color'] = combined_df['log_pop'].map(color_map)
        # print(combined_df)

        # Construct style dictionary
        unique_country_list = combined_df['Country'].unique().tolist()
        ctry_index = range(len(unique_country_list))

        style_dic = {}
        for j in ctry_index:
            ctry = unique_country_list[j]
            country = combined_df[combined_df['Country'] == ctry]
            in_dic = {

            }
            for _, r in country.iterrows():
                in_dic[r['Year']] = {'color': r['color'], 'opacity': 0.8}
            style_dic[str(j)] = in_dic

        # Make a dataframe containing each country
        specific_ctry = combined_df[['geometry']]
        ctry_gdf = gpd.GeoDataFrame(specific_ctry)
        ctry_gdf = ctry_gdf.drop_duplicates().reset_index()

        # Create a slider map
        from folium.plugins import TimeSliderChoropleth
        m = folium.Map(min_zoom=2, max_bounds=True, tiles='cartodbpositron')
        _ = TimeSliderChoropleth(
            data=ctry_gdf.to_json(),
            styledict=style_dic,
        ).add_to(m)
        _ = color_map.add_to(m)
        color_map.caption = "Log Number of Population at Risk"

        m.save("malaria/malaria_cumulative_stat_map.html")
        m = m._repr_html_()
        context = {
            'm': m
        }
        return render(request, 'malaria/malaria_cumulative_stat_map.html',context)

    else:
        slider_name_list = []
        slider_death_list = []
        slider_lat_list = []
        slider_lon_list = []
        slider_year_list = []

        for m in Malaria.objects.all():
            slider_lat_list.append(m.Latitude)
            slider_lon_list.append(m.Longitude)
            slider_name_list.append(m.Country)
            slider_death_list.append(m.Deaths)
            year = str(m.Year)
            if year != '2010':
                year = year + '/12/31'
            slider_year_list.append(year)

        country_case = zip(slider_name_list, slider_death_list, slider_year_list)
        slider_zipped_country_case = list(country_case)
        df_slider = pd.DataFrame(data=slider_zipped_country_case, columns=['Country', 'Deaths', 'Year'])
        df_slider = df_slider[df_slider.Deaths != 0]

        # sorting
        sorted_df = df_slider.sort_values(['Country',
                                           'Year']).reset_index(drop=True)

        # Combine data with the file
        country = gpd.read_file("/Users/benchiang/Desktop/countries.geojson")
        country = country.rename(columns={'ADMIN': 'Country'})
        combined_df = sorted_df.merge(country, on='Country')
        # print(combined_df)

        # Use Log to plot the cases
        #combined_df['log_pop'] = np.log10(combined_df['Population_at_risk'])
        combined_df = combined_df[['Country', 'Deaths', 'Year', 'geometry']]
        # print(combined_df)

        combined_df['Year'] = pd.to_datetime(combined_df['Year']).astype(int) / 10 ** 9
        combined_df['Year'] = combined_df['Year'].astype(int).astype(str)

        # Construct color map
        max_color = max(combined_df['Deaths'])
        min_color = min(combined_df['Deaths'])
        color_map = cm.linear.YlOrRd_09.scale(min_color, max_color)
        combined_df['color'] = combined_df['Deaths'].map(color_map)
        # print(combined_df)

        # Construct style dictionary
        unique_country_list = combined_df['Country'].unique().tolist()
        ctry_index = range(len(unique_country_list))

        style_dic = {}
        for j in ctry_index:
            ctry = unique_country_list[j]
            country = combined_df[combined_df['Country'] == ctry]
            in_dic = {

            }
            for _, r in country.iterrows():
                in_dic[r['Year']] = {'color': r['color'], 'opacity': 0.8}
            style_dic[str(j)] = in_dic

        # Make a dataframe containing each country
        specific_ctry = combined_df[['geometry']]
        ctry_gdf = gpd.GeoDataFrame(specific_ctry)
        ctry_gdf = ctry_gdf.drop_duplicates().reset_index()

        # Create a slider map
        from folium.plugins import TimeSliderChoropleth
        m = folium.Map(min_zoom=2, max_bounds=True, tiles='cartodbpositron')
        _ = TimeSliderChoropleth(
            data=ctry_gdf.to_json(),
            styledict=style_dic,
        ).add_to(m)
        _ = color_map.add_to(m)
        color_map.caption = "Number of Deaths"

        m.save("malaria/malaria_cumulative_stat_map.html")
        m = m._repr_html_()
        context = {
            'm': m
        }
        return render(request, 'malaria/malaria_cumulative_stat_map.html', context)

    return render(request, 'malaria/malaria_cumulative_stat_map.html')

