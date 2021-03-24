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
import pandas

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
    if request.GET.get("Year") and (request.GET.get("Country") != "World"):
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

    elif request.GET.get("Year") and (request.GET.get("Country") == "World"):
        year_selected = request.GET.get("Year")
        result = Malaria.objects.filter(Year=year_selected)

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

    return render(request, 'malaria/malaria_annual_stat_map.html')


def malaria_cumulative_stat_view(request):
    return render(request, 'malaria/malaria_cumulative_stat.html')


def malaria_cumulative_stat_map_view(request):
    obtained_feature = request.GET.get("Feature")
    obtained_country = request.GET.get("Country")

    if obtained_feature == "Cases":
        slider_name_list = []
        slider_case_list = []
        slider_lat_list = []
        slider_lon_list = []
        slider_year_list = []

        if obtained_country == "World":
            for m in Malaria.objects.all():
                slider_lat_list.append(m.Latitude)
                slider_lon_list.append(m.Longitude)
                slider_name_list.append(m.Country)
                slider_case_list.append(m.Cases)
                year = str(m.Year)
                if year != '2010':
                    year = year + '/12/31'
                slider_year_list.append(year)

        else:
            for m in Malaria.objects.filter(Country=obtained_country):
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

        if obtained_country == "World":
            for m in Malaria.objects.all():
                slider_lat_list.append(m.Latitude)
                slider_lon_list.append(m.Longitude)
                slider_name_list.append(m.Country)
                slider_pop_list.append(m.Population_at_risk)
                year = str(m.Year)
                if year != '2010':
                    year = year + '/12/31'
                slider_year_list.append(year)

        else:
            for m in Malaria.objects.filter(Country=obtained_country):
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
        return render(request, 'malaria/malaria_cumulative_stat_map.html', context)

    else:
        slider_name_list = []
        slider_death_list = []
        slider_lat_list = []
        slider_lon_list = []
        slider_year_list = []

        if obtained_country == "World":
            for m in Malaria.objects.all():
                slider_lat_list.append(m.Latitude)
                slider_lon_list.append(m.Longitude)
                slider_name_list.append(m.Country)
                slider_death_list.append(m.Deaths)
                year = str(m.Year)
                if year != '2010':
                    year = year + '/12/31'
                slider_year_list.append(year)
        else:
            for m in Malaria.objects.filter(Country=obtained_country):
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
        # combined_df['log_pop'] = np.log10(combined_df['Population_at_risk'])
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


def malaria_environmental_factor_view(request):
    return render(request, 'malaria/malaria_environmental_factor.html')


def malaria_rainfall_view(request):
    return render(request, 'malaria/malaria_rainfall.html')

def malaria_rainfall_scatterplot_view(request):
    return render(request, 'malaria/malaria_rainfall_scatterplot.html')


def malaria_rainfall_map_view(request):
    rainfall_list = []
    name_list = []
    case_map_list = []
    pop_map_list = []
    obtained_year = request.GET.get("Year")
    if request.GET.get("Feature") == "Rainfall_gauge":

        for m in Malaria.objects.filter(Year=obtained_year):
            name_list.append(m.Country)
            case_map_list.append(m.Cases)
            pop_map_list.append(m.Population_at_risk)
            rainfall_list.append(m.Rainfall_gauge)

        latlon = zip(name_list, rainfall_list)
        zipped_latlon = list(latlon)

        df = pd.DataFrame(data=zipped_latlon, columns=['Country', 'Rainfall_gauge'])


        map_demo = folium.Map(min_zoom=2, max_bounds=True,
                              tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery'
                                    '/MapServer/tile/{z}/{y}/{x}', attr='My Map Data Attribution')

        geojson = "/Users/benchiang/Desktop/countries.geojson"
        g = folium.GeoJson(
            geojson,
            name=geojson
        ).add_to(map_demo)

        # Choropleth Map 1
        folium.Choropleth(
            geo_data=geojson,
            name="choropleth",
            data=df,
            columns=["Country", "Rainfall_gauge"],
            key_on="feature.properties.ADMIN",
            fill_color="Set2",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name="Annual Rainfall Gauge (mm)",
            bins=6,
            reset=True,

        ).add_to(map_demo)

        folium.LayerControl().add_to(map_demo)
        map_demo.save("malaria/malaria_rainfall_map.html")
        map_demo = map_demo._repr_html_()
        context = {
            'map_demo': map_demo
        }
        return render(request, 'malaria/malaria_rainfall_map.html', context)

    elif request.GET.get("Feature") == "Population_at_risk":
        for m in Malaria.objects.filter(Year=obtained_year):
            name_list.append(m.Country)
            pop_map_list.append(m.Population_at_risk)

        latlon = zip(name_list, pop_map_list)
        zipped_latlon = list(latlon)

        df = pd.DataFrame(data=zipped_latlon, columns=['Country', 'Population_at_risk'])
        df['Population_at_risk'] = np.log10(df['Population_at_risk'])

        map_demo = folium.Map(min_zoom=2, max_bounds=True,
                              tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery'
                                    '/MapServer/tile/{z}/{y}/{x}', attr='My Map Data Attribution')

        geojson = "/Users/benchiang/Desktop/countries.geojson"
        g = folium.GeoJson(
            geojson,
            name=geojson
        ).add_to(map_demo)

        # Choropleth Map 1
        folium.Choropleth(
            geo_data=geojson,
            name="choropleth",
            data=df,
            columns=["Country", "Population_at_risk"],
            key_on="feature.properties.ADMIN",
            fill_color="Set2",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name="Population at risk in log scale",
            bins=6,
            reset=True,

        ).add_to(map_demo)

        folium.LayerControl().add_to(map_demo)
        map_demo.save("malaria/malaria_rainfall_map.html")
        map_demo = map_demo._repr_html_()
        context = {
            'map_demo': map_demo
        }
        return render(request, 'malaria/malaria_rainfall_map.html', context)

    else:
        for m in Malaria.objects.filter(Year=obtained_year):
            name_list.append(m.Country)
            case_map_list.append(m.Cases)

        latlon = zip(name_list, case_map_list)
        zipped_latlon = list(latlon)

        df = pd.DataFrame(data=zipped_latlon, columns=['Country', 'Cases'])


        map_demo = folium.Map(min_zoom=2, max_bounds=True, tiles='cartodbpositron')

        geojson = "/Users/benchiang/Desktop/countries.geojson"
        g = folium.GeoJson(
            geojson,
            name=geojson
        ).add_to(map_demo)

        # Choropleth Map 1
        folium.Choropleth(
            geo_data=geojson,
            name="choropleth",
            data=df,
            columns=["Country", "Cases"],
            key_on="feature.properties.ADMIN",
            fill_color="Set2",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name="Cases",
            bins=6,
            reset=True,

        ).add_to(map_demo)

        folium.LayerControl().add_to(map_demo)
        map_demo.save("malaria/malaria_rainfall_map.html")
        map_demo = map_demo._repr_html_()
        context = {
            'map_demo': map_demo
        }
        return render(request, 'malaria/malaria_rainfall_map.html', context)

    return render(request, 'malaria/malaria_rainfall_map.html')


def malaria_socioeconomic_factor_view(request):
    return render(request, 'malaria/malaria_socioeconomic_factor.html')


def malaria_gdp_per_capita_view(request):
    if request.GET.get("GraphType") == "Scatterplot":
        country_filter = request.GET.get("Country")
        result = Malaria.objects.filter(Q(Country=country_filter))

        # Prepare data for the graphs
        population_list = []
        cases_list = []
        deaths_list = []
        gdp_list = []

        for population in result.values_list('Population_at_risk'):
            population_list.append(population)

        for case in result.values_list('Cases'):
            cases_list.append(case)

        for death in result.values_list('Deaths'):
            deaths_list.append(death)

        for gdp in result.values_list('GDP_per_capita'):
            gdp_list.append(gdp)

        # Line graph for gdp per capita over the years
        year_list_gdp = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']
        plot_gdp = figure(title="GDP per capita in " + country_filter, x_range=year_list_gdp,
                          plot_width=800, plot_height=400)
        plot_gdp.left[0].formatter.use_scientific = False
        plot_gdp.line(year_list_gdp, gdp_list, line_width=2)
        script_gdp, div_gdp = components(plot_gdp)

        # Scatter plot for population at risk vs gdp
        x_scatter_gdp = gdp_list
        y_scatter_pop = population_list

        scatter_plot_1 = figure(plot_width=700, plot_height=700, x_axis_label='GDP per capita',
                                y_axis_label='Number of population at risk in ' + country_filter)
        scatter_plot_1.circle(x_scatter_gdp, y_scatter_pop, size=10, line_color="navy", fill_color="orange",
                              fill_alpha=0.5)
        scatter_plot_1.left[0].formatter.use_scientific = False

        # Best-fit Line for population at risk vs gdp
        d = pandas.DataFrame(x_scatter_gdp)
        d1 = pandas.DataFrame(y_scatter_pop)
        x = np.array(d[0])
        y = np.array(d1[0])

        par = np.polyfit(x, y, 1, full=True)
        slope = par[0][0]
        intercept = par[0][1]
        y_predicted_pop = [slope * i + intercept for i in x]
        scatter_plot_1.line(x, y_predicted_pop, color='red')
        script_pop, div_pop = components(scatter_plot_1)

        ####### Split Line
        # Scatter plot for case vs gdp
        x_scatter_gdp = gdp_list
        y_scatter_case = cases_list

        scatter_plot_2 = figure(plot_width=700, plot_height=700, x_axis_label='GDP per capita',
                                y_axis_label='Number of cases in ' + country_filter)
        scatter_plot_2.circle(x_scatter_gdp, y_scatter_case, size=10, line_color="navy", fill_color="orange",
                              fill_alpha=0.5)
        scatter_plot_2.left[0].formatter.use_scientific = False

        # Best-fit Line for population at risk vs gdp
        d = pandas.DataFrame(x_scatter_gdp)
        d1 = pandas.DataFrame(y_scatter_case)
        x = np.array(d[0])
        y = np.array(d1[0])

        par = np.polyfit(x, y, 1, full=True)
        slope = par[0][0]
        intercept = par[0][1]
        y_predicted_case = [slope * i + intercept for i in x]
        scatter_plot_2.line(x, y_predicted_case, color='red')
        script_case, div_case = components(scatter_plot_2)

        ####### Split Line
        # Scatter plot for deaths vs gdp
        x_scatter_gdp = gdp_list
        y_scatter_death = deaths_list

        scatter_plot_3 = figure(plot_width=700, plot_height=700, x_axis_label='GDP per capita',
                                y_axis_label='Number of deaths in ' + country_filter)
        scatter_plot_3.circle(x_scatter_gdp, y_scatter_death, size=10, line_color="navy", fill_color="orange",
                              fill_alpha=0.5)
        scatter_plot_3.left[0].formatter.use_scientific = False

        # Best-fit Line for population at risk vs gdp
        d = pandas.DataFrame(x_scatter_gdp)
        d1 = pandas.DataFrame(y_scatter_death)
        x = np.array(d[0])
        y = np.array(d1[0])

        par = np.polyfit(x, y, 1, full=True)
        slope = par[0][0]
        intercept = par[0][1]
        y_predicted_death = [slope * i + intercept for i in x]
        scatter_plot_3.line(x, y_predicted_death, color='red')
        script_death, div_death = components(scatter_plot_3)

        context = {'Malaria': result, 'script_pop': script_pop, 'div_pop': div_pop, 'script_case': script_case,
                   'div_case': div_case,
                   'script_death': script_death, 'div_death': div_death, 'script_gdp': script_gdp, 'div_gdp': div_gdp
                   }

        return render(request, 'malaria/malaria_gdp_per_capita.html', context)
    elif request.GET.get("GraphType") == "Map":
        return render(request, 'malaria/malaria_gdp_per_capita.html')
    return render(request, 'malaria/malaria_gdp_per_capita.html')


def malaria_pct_agri_pop_view(request):
    if request.GET.get("GraphType") == "Scatterplot":
        country_filter = request.GET.get("Country")
        result = Malaria.objects.filter(Q(Country=country_filter))

        # Prepare data for the graphs
        population_list = []
        cases_list = []
        deaths_list = []
        pct_list = []

        for population in result.values_list('Population_at_risk'):
            population_list.append(population)

        for case in result.values_list('Cases'):
            cases_list.append(case)

        for death in result.values_list('Deaths'):
            deaths_list.append(death)

        for pct in result.values_list('Rural_pop_pct'):
            pct_list.append(pct)

        # Line graph for percentage of agricultural population over the years
        year_list_pct = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']
        plot_pct = figure(title="GDP per capita in " + country_filter, x_range=year_list_pct,
                          plot_width=800, plot_height=400)
        plot_pct.left[0].formatter.use_scientific = False
        plot_pct.line(year_list_pct, pct_list, line_width=2)
        script_pct, div_pct = components(plot_pct)

        # Scatter plot for population at risk vs percentage of agricultural population
        x_scatter_pct = pct_list
        y_scatter_pop = population_list

        scatter_plot_1 = figure(plot_width=700, plot_height=700,
                                x_axis_label='Percentage of Agricultural Population (Percentage)',
                                y_axis_label='Number of population at risk in ' + country_filter)
        scatter_plot_1.circle(x_scatter_pct, y_scatter_pop, size=10, line_color="navy", fill_color="orange",
                              fill_alpha=0.5)
        scatter_plot_1.left[0].formatter.use_scientific = False

        # Best-fit Line for population at risk vs gdp
        d = pandas.DataFrame(x_scatter_pct)
        d1 = pandas.DataFrame(y_scatter_pop)
        x = np.array(d[0])
        y = np.array(d1[0])

        par = np.polyfit(x, y, 1, full=True)
        slope = par[0][0]
        intercept = par[0][1]
        y_predicted_pop = [slope * i + intercept for i in x]
        scatter_plot_1.line(x, y_predicted_pop, color='red')
        script_pop, div_pop = components(scatter_plot_1)

        ####### Split Line
        # Scatter plot for case vs gdp
        x_scatter_pct = pct_list
        y_scatter_case = cases_list

        scatter_plot_2 = figure(plot_width=700, plot_height=700,
                                x_axis_label='Percentage of Agricultural Population (Percentage)',
                                y_axis_label='Number of cases in ' + country_filter)
        scatter_plot_2.circle(x_scatter_pct, y_scatter_case, size=10, line_color="navy", fill_color="orange",
                              fill_alpha=0.5)
        scatter_plot_2.left[0].formatter.use_scientific = False

        # Best-fit Line for population at risk vs gdp
        d = pandas.DataFrame(x_scatter_pct)
        d1 = pandas.DataFrame(y_scatter_case)
        x = np.array(d[0])
        y = np.array(d1[0])

        par = np.polyfit(x, y, 1, full=True)
        slope = par[0][0]
        intercept = par[0][1]
        y_predicted_case = [slope * i + intercept for i in x]
        scatter_plot_2.line(x, y_predicted_case, color='red')
        script_case, div_case = components(scatter_plot_2)

        ####### Split Line
        # Scatter plot for deaths vs Percentage of Agricultural Population (Percentage)
        x_scatter_pct = pct_list
        y_scatter_death = deaths_list

        scatter_plot_3 = figure(plot_width=700, plot_height=700,
                                x_axis_label='Percentage of Agricultural Population (Percentage)',
                                y_axis_label='Number of deaths in ' + country_filter)
        scatter_plot_3.circle(x_scatter_pct, y_scatter_death, size=10, line_color="navy", fill_color="orange",
                              fill_alpha=0.5)
        scatter_plot_3.left[0].formatter.use_scientific = False

        # Best-fit Line for population at risk vs gdp
        d = pandas.DataFrame(x_scatter_pct)
        d1 = pandas.DataFrame(y_scatter_death)
        x = np.array(d[0])
        y = np.array(d1[0])

        par = np.polyfit(x, y, 1, full=True)
        slope = par[0][0]
        intercept = par[0][1]
        y_predicted_death = [slope * i + intercept for i in x]
        scatter_plot_3.line(x, y_predicted_death, color='red')
        script_death, div_death = components(scatter_plot_3)

        context = {'Malaria': result, 'script_pop': script_pop, 'div_pop': div_pop, 'script_case': script_case,
                   'div_case': div_case,
                   'script_death': script_death, 'div_death': div_death, 'script_gdp': script_pct, 'div_gdp': div_pct
                   }

        return render(request, 'malaria/malaria_pct_agri_pop.html', context)
    elif request.GET.get("GraphType") == "Map":
        return render(request, 'malaria/malaria_pct_agri_pop.html')
    return render(request, 'malaria/malaria_pct_agri_pop.html')
