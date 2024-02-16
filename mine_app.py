import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import plotly.express as px


def config_map(df):

    st.write(df)

    

    
    

# Fonction pour afficher la page d'accueil
def accueil():

    # st.set_page_config(page_title="MFPAI Reporting", page_icon=":bar_chart:", layout="wide")

    st.title(":bar_chart: MinerauxVisuaux")
    st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
    st.write("""
        Cette application vous permet de visualiser différentes données.
    """)


    df = pd.read_csv("mineraux_data.csv")

    # Affichage de la carte
    config_map(df)

    # Créer une carte Folium centrée sur les coordonnées moyennes des données
    ## Créer une carte Folium centrée sur les coordonnées moyennes des données
    map_center = [df['LATITUDE'].mean(), df['LONGITUDE'].mean()]
    m = folium.Map(location=map_center, zoom_start=7)

    # Afficher la carte Folium dans Streamlit
    st.sidebar.subheader("Choisir la localisation en fonction du minerai")
    selected_minerai = st.sidebar.selectbox("MINERAI", sorted(df['MINERAI'].unique()))

    # Ajouter des marqueurs pour chaque emplacement
    for index, row in df.iterrows():
        popup_text = f"<b>Minerai:</b> {row['MINERAI']}<br>" \
                    f"<b>Description:</b> {row['DESCRIPTION']}<br>" \
                    f"<b>Quantité (kg):</b> {row['QUANTITE']}<br>" \
                    f"<b>Pureté (%):</b> {row['PURETE']}"
        if row['MINERAI'] == selected_minerai:
            marker = folium.Marker(location=[row['LATITUDE'], row['LONGITUDE']], popup=folium.Popup(popup_text, max_width=300), icon=folium.Icon(color='green'))
        else:
            marker = folium.Marker(location=[row['LATITUDE'], row['LONGITUDE']], popup=folium.Popup(popup_text, max_width=300))
        marker.add_to(m)

    # Filtrer les données en fonction du minerai sélectionné
    filtered_data = df[df['MINERAI'] == selected_minerai]
    st.subheader(f"Localisation des gisements de {selected_minerai}")
    st.write(filtered_data)

    # Afficher la carte Folium statique dans Streamlit
    folium_static(m)

#----------------------------------------------------------------------------------------------------#
    # Créer un DataFrame pivot pour la répartition des minéraux par région
    pivot_df = df.pivot_table(index='MINERAI', columns='LOCALISATION', values='QUANTITE', aggfunc='sum')

    # Remplacer les valeurs NaN par 0
    pivot_df.fillna(0, inplace=True)

    # Transposer le DataFrame pivot
    pivot_df_transposed = pivot_df.transpose()
    
    # Créer un diagramme à barres empilées
    fig = px.bar(pivot_df_transposed, barmode='stack', title="Répartition des minéraux par région en fonction de la quantité")
    st.plotly_chart(fig)

#----------------------------------------------------------------------------------------------------#
    # Créer une liste déroulante pour sélectionner la région
    selected_region = st.selectbox('Sélectionner une région', df['LOCALISATION'].dropna().unique())
    
    # Affichage des deux statistiques en colonnes
    # Créer deux colonnes pour afficher les graphiques
    col1, col2 = st.columns(2)

    with col1:
        # Filtrer les données pour la région sélectionnée
        region_data = df[df['LOCALISATION'] == selected_region]

        # Créer un diagramme en barres pour la région sélectionnée
        fig_bar = px.bar(region_data, x='MINERAI', y='QUANTITE', color='QUANTITE',
                        title=f'Répartition de la quantité de minerais à {selected_region}',
                        labels={'QUANTITE': 'Quantité', 'MINERAI': 'Minerai'})
        fig_bar.update_layout(legend_title_text='Minerai', autosize=True, width=400)
        st.plotly_chart(fig_bar)

    with col2:
        # Créer un diagramme circulaire pour la répartition de la quantité de minerais
        fig_pie = px.pie(region_data, values='QUANTITE', names='MINERAI',
                        title=f'Répartition de la quantité de minerais à {selected_region}')
        fig_pie.update_layout(legend_title_text='Minerai', width=450)
        st.plotly_chart(fig_pie)
#     # Définition des couleurs pour les barres du graphique
#     couleurs = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']

#     # Créer une liste déroulante pour sélectionner la population (POP)
#     selected_pop = st.selectbox("Sélectionner le POP", df['NOM_POP'].unique())

#     # Filtrer les données en fonction de la population sélectionnée
#     filtered_data = df[df['NOM_POP'] == selected_pop]

#     # Créer la carte Folium
#     m = folium.Map(location=[filtered_data['LATITUDE'].mean(), filtered_data['LONGITUDE'].mean()], zoom_start=10)

#     # Ajouter les emplacements des centres sur la carte
#     for index, row in filtered_data.iterrows():
#         popup_text = f"<b>Nom du Centre:</b> {row['NOM_CENTRE']}<br><b>Nom du chef:</b> {row['NOM_CHEF']}<br><b>Nom du POP:</b> {row['NOM_POP']}<br>"
#         folium.Marker(location=[row['LATITUDE'], row['LONGITUDE']], popup=folium.Popup(popup_text, max_width=100)).add_to(m)

#     # Afficher la carte Folium dans Streamlit
#     folium_static(m)


#     # Liste déroulante pour sélectionner une POP
#     selected_pop = st.selectbox("Sélectionnez une POP", df['NOM_POP'].unique())

#     # Filtrer les centres en fonction de la POP sélectionnée
#     filtered_centers = df[df['NOM_POP'] == selected_pop][['NOM_CENTRE', 'NOM_CHEF']]

#     # Afficher la liste des centres correspondants avec le nom du chef
#     st.write("Centres correspondants à la POP sélectionnée :")
#     st.write(filtered_centers)



# # Fonction pour afficher la troisième page
# def page_3():
#     st.title("Page 3")
#     st.write("Contenu de la troisième page")


# Fonction principale pour gérer la navigation
def main():

    st.set_page_config(page_title='Reporting MFPAI',  layout='wide', page_icon=":bar_chart:")
    st.sidebar.title("Menu de navigation")
    accueil()
    st.markdown(
        """
        <style>
        .sidebar .block-container {
            display: flex;
            flex-direction: row;
            justify-content: space-around;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
