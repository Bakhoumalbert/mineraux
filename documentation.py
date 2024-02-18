import streamlit as st
import json

def documentation():
    st.title(":books: Documentation")
    st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

    with open("data/documentation/minerais.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    
    # Afficher le titre de la page
    st.title("Documentation des Minerais")
    st.subheader("""
        Vous aurez des informations sur chaque minerai présent au Sénégal
    """)


    for minerai, details in data.items():
        # Diviser l'espace en colonnes
        col1, _ ,col2 = st.columns([1, 0.5 ,3])

        with col1:
            st.title(minerai)
            if "Image" in details and details["Image"]:
                st.image(details["Image"], use_column_width=True)
        with col2:
            if "Description" in details and details["Description"]:
                st.subheader("Description:")
                st.write(details["Description"])
            if "Usages" in details and details["Usages"]:
                st.subheader("Usages:")
                if "Usages" in details:
                    usages_data = details["Usages"]
                    if isinstance(usages_data, dict):
                        for usage, pourcentage in usages_data.items():
                            st.write(f"{usage}: {pourcentage}")
                    elif isinstance(usages_data, list):
                        for usage_item in usages_data:
                            st.write(usage_item)
                    else:
                        st.warning("Le format des données 'Usages' n'est pas pris en charge.")
                else:
                    st.warning("Aucune donnée d'usages n'a été trouvée.")
            if "use_image" in details and details["use_image"]:
                st.write("Cas d'usage")
                # Créer un ensemble pour stocker les URL des images déjà affichées
                displayed_images = set()

                # Parcourir toutes les images
                for image_url in details['use_image']:
                    # Vérifier si l'image a déjà été affichée
                    if image_url not in displayed_images:
                        # Ajouter l'image à l'ensemble des images déjà affichées
                        displayed_images.add(image_url)
                        # Afficher l'image
                        st.image(image_url, width=100)
        st.write("-------------------------------------------------------------------")
        
if __name__ == "__main__":
    documentation()