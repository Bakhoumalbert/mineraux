import os
import pandas as pd
import streamlit as st
import plotly.express as px

def production():

    st.title(":joystick: Production minière")
    st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
    st.write("""
        Cette application vous permet de visualiser différentes données.
    """)
    
    # Chemin du dossier contenant les fichiers Excel
    folder_path = "/mount/src/mineraux/data/exploitation"

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
        st.success(f"{len(dfs)} fichiers Excel ont été chargés avec succès.")

        # Extraire les années des noms de fichiers
        years = [int(filename.split("_")[0]) for filename in os.listdir(folder_path) if filename.endswith(".xlsx")]

        # Créer une liste déroulante pour sélectionner l'année
        selected_year = st.selectbox("Sélectionner une année :", years)

        # Récupérer le DataFrame correspondant à l'année sélectionnée
        selected_df = dfs[years.index(selected_year)]

        st.write(df.loc[2])

        # Afficher les données correspondantes à l'année sélectionnée
        st.write(selected_df)

    
        # # Créer un diagramme en barres pour la répartition des minerais en fonction de la quantité
        # st.subheader('Répartition des minerais en fonction de la quantité')
        # bar_fig = px.bar(df.groupby('Substance')['Volume'].sum().reset_index(), x='Substance', y='Volume', 
        #                 labels={'Volume': 'Quantité', 'Substance': 'Minerai'})
        # st.plotly_chart(bar_fig)

        # # # Compter le total de la quantité par type de minerai
        # # total_quantity = df.groupby('Substance')['Volume'].sum()

        # st.subheader('Répartition des minerais (Diagramme circulaire)')
        # pie_fig = px.pie(names=df['Substance'].unique(), values=df.groupby('Substance')['Volume'].sum())
        # st.plotly_chart(pie_fig)

        # Ajouter les unités aux noms de substance
        df['Substance_with_unit'] = df['Substance'] + ' (' + df['Unit?'] + ')'

        # Créer un diagramme en barres pour la répartition des minerais en fonction de la quantité
        st.subheader('Répartition des minerais en fonction de la quantité')
        bar_fig = px.bar(df.groupby('Substance_with_unit')['Volume'].sum().reset_index(), x='Substance_with_unit', y='Volume', 
                        labels={'Volume': 'Quantité', 'Substance_with_unit': 'Minerai'})
        st.plotly_chart(bar_fig)

        st.write(df )
        df_dropnan =  df.dropna(subset=['Substance_with_unit'])
 
        # Créer un diagramme circulaire de la répartition des minerais
        st.subheader('Répartition des minerais (Diagramme circulaire)')
        pie_fig = px.pie(names=df_dropnan['Substance_with_unit'].unique(), values=df_dropnan.groupby('Substance_with_unit')['Volume'].sum())
        st.plotly_chart(pie_fig, use_container_width=True)


if __name__ == "__main__":
    production()