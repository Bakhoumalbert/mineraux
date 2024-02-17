import streamlit as st
import pandas as pd
import folium
import geopandas as gpd
import os
from streamlit_folium import folium_static
import plotly.express as px
from folium.plugins import MarkerCluster


def config_map(df):

    st.write(df)

    

    
    

# Fonction pour afficher la page d'accueil
def static_mineraux():

    # st.set_page_config(page_title="MFPAI Reporting", page_icon=":bar_chart:", layout="wide")

    st.title(":gem: MinerauxVisuaux")
    st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
    st.write("""
        Cette application vous permet de visualiser différentes données.
    """)


    df = pd.read_csv("data/correct_data.csv")

    # Affichage de la carte
    config_map(df)



    # Afficher la carte Folium dans Streamlit
    st.sidebar.subheader("Choisir la localisation en fonction du minerai")
    selected_minerai = st.selectbox("MINERAL", sorted(df['MINERAL'].unique()))

    map_center = [df[df['MINERAL'] == selected_minerai]['LONGITUDE'].mean(), df[df['MINERAL'] == selected_minerai]['LATITUDE'].mean()]
    m = folium.Map(location=map_center, zoom_start=7)
    # Create a MarkerCluster object
    marker_cluster = MarkerCluster().add_to(m)

    # Ajouter des marqueurs pour chaque emplacement
    for index, row in df[df['MINERAL'] == selected_minerai].iterrows():
        popup_text = f"<b>Minerai:</b> {row['MINERAL']}<br>" \
                    f"<b>Description:</b> {row['DESCRIPTION']}<br>" \
                    f"<b>Pureté (%):</b> {row['PURETE']}"
        marker = folium.Marker(location=[row['LONGITUDE'], row['LATITUDE']], 
                            popup=folium.Popup(popup_text, max_width=300))
        marker.add_to(marker_cluster)

    folium_static(m, width=920, height=600)



    st.write("---------------------------------------------------")

    # Create a map centered based on the entire dataset
    map_center = [df['LONGITUDE'].mean(), df['LATITUDE'].mean()]
    m = folium.Map(location=map_center, zoom_start=7)

    # Afficher la carte Folium dans Streamlit
    st.sidebar.subheader("Choisir la localisation en fonction du minerai")
    option = st.selectbox("MINERAL", ["Tout afficher"] + sorted(df['MINERAL'].unique()))

    # Create a MarkerCluster object
    marker_cluster = MarkerCluster().add_to(m)

    if option == "Tout afficher":
        # Define colors for each mineral
        mineral_colors = {
            'OR': 'yellow',
            'URANIUM': 'green',
            'PLOMB': 'blue',
            'NICKEL': 'red',
            'CUIVRE': 'orange',
            'MARBRE': 'purple',
            'DIAMANT': 'gray',
            'LITHIUM': 'pink',
            'ETAIN': 'brown',
            'FER': 'black'
        }

        # Add markers for all minerals with different colors
        for index, row in df.iterrows():
            popup_text = f"<b>Minerai:</b> {row['MINERAL']}<br>" \
                        f"<b>Description:</b> {row['DESCRIPTION']}<br>" \
                        f"<b>Pureté (%):</b> {row['PURETE']}"
            marker = folium.Marker(location=[row['LONGITUDE'], row['LATITUDE']],
                                popup=folium.Popup(popup_text, max_width=300),
                                icon=folium.Icon(color=mineral_colors.get(row['MINERAL'], 'gray')))
            marker.add_to(marker_cluster)

        # Add legend
        legend_html = """
        <div style="position: fixed; 
                    bottom: 50px; left: 50px; width: 160px; height: 120px; 
                    border:2px solid grey; z-index:9999; font-size:14px;
                    background-color:white;
                    ">&nbsp; <b>Légende</b> <br>
                    &nbsp; OR &nbsp; <i class="fa fa-map-marker fa-2x"
                                style="color:yellow"></i><br>
                    &nbsp; URANIUM &nbsp; <i class="fa fa-map-marker fa-2x"
                                style="color:green"></i><br>
                    &nbsp; PLOMB &nbsp; <i class="fa fa-map-marker fa-2x"
                                style="color:blue"></i><br>
                    &nbsp; NICKEL &nbsp; <i class="fa fa-map-marker fa-2x"
                                style="color:red"></i><br>
                    &nbsp; CUIVRE &nbsp; <i class="fa fa-map-marker fa-2x"
                                style="color:orange"></i><br>
                    &nbsp; MARBRE &nbsp; <i class="fa fa-map-marker fa-2x"
                                style="color:purple"></i><br>
                    &nbsp; DIAMANT &nbsp; <i class="fa fa-map-marker fa-2x"
                                style="color:gray"></i><br>
                    &nbsp; LITHIUM &nbsp; <i class="fa fa-map-marker fa-2x"
                                style="color:pink"></i><br>
                    &nbsp; ETAIN &nbsp; <i class="fa fa-map-marker fa-2x"
                                style="color:brown"></i><br>
                    &nbsp; FER &nbsp; <i class="fa fa-map-marker fa-2x"
                                style="color:black"></i>
        </div>
        """
        m.get_root().html.add_child(folium.Element(legend_html))

    else:
        # Filter data for selected mineral
        selected_df = df[df['MINERAL'] == option]

        # Add markers for selected mineral
        for index, row in selected_df.iterrows():
            popup_text = f"<b>Minerai:</b> {row['MINERAL']}<br>" \
                        f"<b>Description:</b> {row['DESCRIPTION']}<br>" \
                        f"<b>Pureté (%):</b> {row['PURETE']}"
            marker = folium.Marker(location=[row['LONGITUDE'], row['LATITUDE']],
                                popup=folium.Popup(popup_text, max_width=300))
            marker.add_to(marker_cluster)

    folium_static(m, width=920, height=600)
    
    st.markdown(
        """
        <style>
        .map-container {
            margin: auto;
            padding: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )



if __name__ == "__main__":
    static_mineraux()
