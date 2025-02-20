import streamlit as st
import geopandas as gpd
from streamlit_folium import st_folium
import folium

entry_file = st.sidebar.file_uploader('Selecione um arquivo de carbono')

entry_desmat = st.sidebar.file_uploader('Selecione um arquivo de desmatamento')

if entry_file and entry_desmat:
    @st.cache_resource
    def load_carbono():
        carbono = gpd.read_parquet(entry_file)
        return carbono

    gdf_carbono = load_carbono()

    @st.cache_resource
    def load_desmat():
        desmat = gpd.read_parquet(entry_desmat)
        return desmat

    gdf_desmat = load_desmat()

    st.title('📊Monitoramento de carbono')

    years = sorted(gdf_carbono['ano'].unique())

    selected_year = st.sidebar.slider('Selecione o ano',min_value=min(years),max_value=max(years),value=max(years))

    filtered_df = gdf_carbono[gdf_carbono['ano'] == selected_year]

    m = folium.Map(location=[-15.0,-52.0], zoom_start=5,control_scale=True,tiles='Esri World Imagery')

    filtered_df['intervalo'] = filtered_df['val'].apply(lambda x: 'baixo' if x <= 10 else
                                                        'medio' if 11 <= x <= 20 else
                                                        'alto' if 21 <= x <= 35 else
                                                        'muito_alto'
                                                        )
    
    color_mapping = {
    'muito_alto':'blue',
    'alto' : 'green',
    'medio' :'yellow',
    'baixo' : 'red'
    }

    def style_function_carbono(feature):

        classe = feature.get('properties', []).get('intervalo','')

        return{
            'fillColor' : color_mapping.get(classe,(0,0,0,255)),
            'color' : 'red',
            'weight' : 0,
            'fillOpacity' : 0.6
        }

    folium.GeoJson(
        filtered_df,
        style_function=style_function_carbono,
        tooltip=folium.features.GeoJsonTooltip(
        fields=['val'],
        aliases=['t/ha: '],
        localize=True
        )
    ).add_to(m)

    bounds = gdf_carbono.total_bounds

    m.fit_bounds([[bounds[1],bounds[0]],[bounds[3],bounds[2]]])

    st_folium(m,width="100%")

    total_carbon = gdf_carbono[gdf_carbono['ano'] == selected_year]['area'].sum()
    total_desmat = gdf_desmat[gdf_desmat['ano'] == selected_year]['st_area_ha'].sum()

    col1,col2=st.columns(2)

    with col1:
        st.metric(label=f"Toneladas de CO2 equivalente no solo ({selected_year})",value=f"{total_carbon:,.2f}")

        evolution = gdf_carbono.groupby('ano')[['area']].sum().reset_index()

        evolution.set_index('ano',inplace=True)

        st.line_chart(evolution)

    with col2:
        st.metric(label=f"Desmatamento ha ({selected_year})",value=f"{total_desmat:,.2f}")

        evolution_desmat = gdf_desmat.groupby('ano')[['st_area_ha']].sum().reset_index()

        evolution_desmat.set_index('ano',inplace=True)

        st.line_chart(evolution_desmat)