import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import plotly.express as px

def config_map(df):


    st.subheader("Afficher les données :")
    st.write(df)
    
    # Calculer les pourcentages de pureté pour chaque minerai
    pourcentages_purete = df.groupby('MINERAL')['PURETE'].mean().reset_index()

    st.write("--------------------------------------------------")
    # Créer un diagramme à barres
    st.subheader('Pourcentages de Pureté par Minerai')
    fig = px.bar(pourcentages_purete, x='MINERAL', y='PURETE', color="PURETE", color_continuous_scale='viridis',
                labels={'MINERAL': 'Minerai', 'PURETE': 'Pourcentage de Pureté'})

    # Afficher le diagramme à barres
    st.plotly_chart(fig, use_container_width=True)
    

# Fonction pour afficher la page d'accueil
def static_mineraux():


    st.title(":gem: Gites Minéraux du Sénégal")
    st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
    st.write("""
        Cette application vous permet de visualiser la répartition des minerais du sénégal.
    """)
    #st.set_page_config(page_title="MFPAI Reporting", page_icon=":bar_chart:", layout="wide")


    df = pd.read_csv("data/correct_data.csv")

    

    # Create a map centered based on the entire dataset
    map_center = [df['LONGITUDE'].mean()+1, df['LATITUDE'].mean()-1]
    m = folium.Map(location=map_center, zoom_start=7.5)
    st.sidebar.write("-----------------------------------")
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

        # Add circles around locations of each mineral with tooltips
        for mineral, color in mineral_colors.items():
            mineral_locations = df[df['MINERAL'] == mineral][['LONGITUDE', 'LATITUDE']].values.tolist()
            for location in mineral_locations:
                tooltip_text = f"<b>{mineral}</b>"
                folium.Circle(location, radius=500, color=color, fill=True, fill_color=color,
                            tooltip=tooltip_text).add_to(m)

        # Add legend
        st.markdown("""<style>
        .sidebar .sidebar-content {
            width: 250px;
            top: 0px;
            right: 0px;
            position: fixed;
            padding: 10px;
        }
        </style>""", unsafe_allow_html=True)

        st.sidebar.subheader("Légende")
        for mineral, color in mineral_colors.items():
            st.sidebar.markdown(f'<span style="color:{color}">●</span> <b>{mineral}</b>', unsafe_allow_html=True)

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

    folium_static(m, width=600, height=600)
    st.write("--------------------------------------------------")

    # Affichage de la carte
    config_map(df)

if __name__ == "__main__":
    static_mineraux()
