import os
import pandas as pd
import streamlit as st
import plotly.express as px

def production():

    st.title(":joystick: Production minière")
    st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
    st.subheader("""
        Visualisation de la production annuelle de minerais
    """)
    
    # Chemin du dossier contenant les fichiers Excel
    folder_path = "data/exploitation"

    # Liste pour stocker les DataFrames de chaque fichier
    dfs = []

    # Parcourir tous les fichiers dans le dossier
    # Parcourir les fichiers dans le dossier
    for filename in os.listdir(folder_path):
        if filename.endswith(".xlsx"):
            try:
                # Lire le fichier Excel et ajouter le DataFrame à la liste
                df = pd.read_excel(os.path.join(folder_path, filename), header=1)
                dfs.append(df)
            except FileNotFoundError:
                st.error(f"Fichier {filename} non trouvé. Veuillez vérifier le chemin d'accès.")
            except Exception as e:
                st.success(f"Une erreur s'est produite lors de la lecture du fichier {filename} : {e}")
        

    # Vérifier si des fichiers ont été trouvés
    if len(dfs) == 0:
        st.error("Aucun fichier Excel trouvé dans le dossier spécifié.")
    else:
        #st.success(f"{len(dfs)} fichiers Excel ont été chargés avec succès.")

        # Extraire les années des noms de fichiers
        years = [int(filename.split("_")[0]) for filename in os.listdir(folder_path) if filename.endswith(".xlsx")]

        # Créer une liste déroulante pour sélectionner l'année
        selected_year = st.selectbox("Sélectionner une année pour voir la production annuelle :", years)

        # Récupérer le DataFrame correspondant à l'année sélectionnée
        selected_df = dfs[years.index(selected_year)]

        st.write(selected_df)
        # Afficher les données correspondantes à l'année sélectionnée
        #st.write(selected_df)

    
        # Ajouter les unités aux noms de substance
        selected_df['Substance_with_unit'] = selected_df['Type du minerai'] + ' (' + selected_df['Unité'] + ')'

        st.write("------------------------------------------------------------------------")
        col1, col2 = st.columns(2)
        
        selected_df = selected_df.dropna(subset=['Substance_with_unit'])

        print(selected_df)

        df_Tonne = selected_df[selected_df['Substance_with_unit'].str.contains('Tonne')]
        df_Once = selected_df[selected_df['Substance_with_unit'].str.contains('Once')]


        with col1:
            # Créer un diagramme en barres pour la répartition des minerais en fonction de la quantité
            st.subheader('Répartition des minerais en fonction de la production totale (En Tonne)')
            bar_fig = px.bar(df_Tonne.groupby('Substance_with_unit')['Production totale'].sum().reset_index(), x='Substance_with_unit', y='Production totale', color="Production totale", color_continuous_scale='viridis',
                            labels={'Production totale': 'Quantité', 'Substance_with_unit': 'Minerai'})
            st.plotly_chart(bar_fig)
        
        with col2:
            # Créer un diagramme en barres pour la répartition des minerais en fonction de la quantité
            st.subheader('Répartition des minerais en fonction de la production totale (En Once)')
            bar_fig = px.bar(df_Once.groupby('Substance_with_unit')['Production totale'].sum().reset_index(), x='Substance_with_unit', y='Production totale', color="Production totale", color_continuous_scale='viridis',
                            labels={'Production totale': 'Quantité', 'Substance_with_unit': 'Minerai'})
            st.plotly_chart(bar_fig)    

        # st.write(df )
        df_dropnan =  selected_df.dropna(subset=['Substance_with_unit'])
 
        # Créer un diagramme circulaire de la répartition des minerais
        st.subheader('Répartition des minerais (Diagramme circulaire)')
        pie_fig = px.pie(names=df_dropnan['Substance_with_unit'].unique(), values=df_dropnan.groupby('Substance_with_unit')['Production totale'].sum())
        st.plotly_chart(pie_fig, use_container_width=True)


if __name__ == "__main__":
    production()