import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
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

    # # Create a map centered based on the entire dataset
    # map_center = [df['LONGITUDE'].mean(), df['LATITUDE'].mean()]
    # m = folium.Map(location=map_center, zoom_start=7)

    # # Afficher la carte Folium dans Streamlit
    st.sidebar.subheader("Choisir la localisation en fonction du minerai")
    option = st.selectbox("MINERAL", ["Tout afficher"] + sorted(df['MINERAL'].unique()))

    # # Create a MarkerCluster object
    # marker_cluster = MarkerCluster().add_to(m)

    # if option == "Tout afficher":
    #     # Define colors for each mineral
    #     mineral_colors = {
    #         'OR': 'yellow',
    #         'URANIUM': 'green',
    #         'PLOMB': 'blue',
    #         'NICKEL': 'red',
    #         'CUIVRE': 'orange',
    #         'MARBRE': 'purple',
    #         'DIAMANT': 'gray',
    #         'LITHIUM': 'pink',
    #         'ETAIN': 'brown',
    #         'FER': 'black'
    #     }

    #     # Add markers for all minerals with different colors
    #     for index, row in df.iterrows():
    #         popup_text = f"<b>Minerai:</b> {row['MINERAL']}<br>" \
    #                     f"<b>Description:</b> {row['DESCRIPTION']}<br>" \
    #                     f"<b>Pureté (%):</b> {row['PURETE']}"
    #         marker = folium.Marker(location=[row['LONGITUDE'], row['LATITUDE']],
    #                             popup=folium.Popup(popup_text, max_width=300),
    #                             icon=folium.Icon(color=mineral_colors.get(row['MINERAL'], 'gray')))
    #         marker.add_to(marker_cluster)

    #         # Add legend
    #         st.sidebar.subheader("Légende des minerais")
    #         for mineral, color in mineral_colors.items():
    #             st.sidebar.markdown(f'<i class="fa fa-map-marker fa-2x" style="color:{color}"></i> {mineral}', unsafe_allow_html=True)


    # else:
    #     # Filter data for selected mineral
    #     selected_df = df[df['MINERAL'] == option]

    #     # Add markers for selected mineral
    #     for index, row in selected_df.iterrows():
    #         popup_text = f"<b>Minerai:</b> {row['MINERAL']}<br>" \
    #                     f"<b>Description:</b> {row['DESCRIPTION']}<br>" \
    #                     f"<b>Pureté (%):</b> {row['PURETE']}"
    #         marker = folium.Marker(location=[row['LONGITUDE'], row['LATITUDE']],
    #                             popup=folium.Popup(popup_text, max_width=300))
    #         marker.add_to(marker_cluster)

    # folium_static(m, width=920, height=600)



    # Create a map centered based on the entire dataset
    map_center = [df['LONGITUDE'].mean(), df['LATITUDE'].mean()]
    m = folium.Map(location=map_center, zoom_start=7)

    # Afficher la carte Folium dans Streamlit
    # st.sidebar.subheader("Choisir la localisation en fonction du minerai")
    # option = st.selectbox("MINERAL", ["Tout afficher"] + sorted(df['MINERAL'].unique()))

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
            marker = folium.Marker(location=[row['LATITUDE'], row['LATITUDE']],
                                popup=folium.Popup(popup_text, max_width=300),
                                icon=folium.Icon(color=mineral_colors.get(row['MINERAL'], 'gray')))
            marker.add_to(marker_cluster)

        # Add circles around locations of each mineral
        for mineral, color in mineral_colors.items():
            mineral_locations = df[df['MINERAL'] == mineral][['LATITUDE', 'LONGITUDE']].values.tolist()
            for location in mineral_locations:
                folium.Circle(location, radius=500, color=color, fill=True, fill_color=color).add_to(m)

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

        # Add circles around locations of selected mineral
        mineral_locations = selected_df[['LATITUDE', 'LONGITUDE']].values.tolist()
        for location in mineral_locations:
            folium.Circle(location, radius=500, color='blue', fill=True, fill_color='blue').add_to(m)

    folium_static(m, width=920, height=600)

if __name__ == "__main__":
    static_mineraux()
