import streamlit as st

def documentation():
    st.title(":books: Documentation")
    st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
    st.write("""
        Cette application vous permet de visualiser différentes données.
    """)

    folder_img = "data/img/"
    # Définition des informations sur chaque minerai
    minerais = [
        {
            "nom": "OR",
            "photo": folder_img + "or.jpg",
            "description": "L'or est l'élément chimique de numéro atomique 79, de symbole Au. Ce symbole, choisi par Berzelius, est formé des deux premières lettres du mot latin aurum (de même sens)."
        },
        {
            "nom": "URANIUM",
            "photo": folder_img + "uranium.jpg",
            "description": "L'uranium est un élément chimique de symbole U et qui porte le numéro atomique 92. L'uranium naturel est constitué de trois isotopes : l'uranium 238, le plus lourd et le plus abondant, l'uranium 235 et l'uranium 234. L'uranium 235 est le seul isotope fissile."
        },
        {
            "nom": "FER",
            "photo": folder_img + "fer.jpg",
            "description": "Le fer est un oligo-élément qui entre dans la composition de l'hémoglobine des globules rouges, de la myoglobine des muscles, et de nombreuses réactions enzymatiques nécessaires à la respiration des cellules."
        },
        {
            "nom": "Lithium",
            "photo": folder_img + "lithium.jpg",
            "description": "Le lithium est l'élément chimique de numéro atomique 3, de symbole Li. C'est un métal alcalin, situé dans le premier groupe du tableau périodique des éléments. Très réactif, le lithium n'existe pas à l'état natif dans le milieu naturel, mais uniquement sous la forme de composés ioniques."
        },
        # Ajoutez des informations sur les autres minerais
    ]

    # Afficher le titre de la page
    st.title("Documentation des Minerais")

    for minerai in minerais:
        
        # Diviser l'espace en colonnes
        col1, col2 = st.columns([1, 3])

        # Dans la première colonne, afficher l'image
        with col1:
            st.image(minerai["photo"], width=200)

        # Dans la deuxième colonne, afficher la description
        with col2:
            st.subheader(minerai["nom"])
            st.write(minerai["description"])
        st.write("-------------------------------------------------------------------")

if __name__ == "__main__":
    documentation()