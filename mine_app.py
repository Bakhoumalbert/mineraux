import streamlit as st
from mineraux import static_mineraux
from product import production
from documentation import documentation

# Fonction principale pour gérer la navigation
def main():

    st.set_page_config(page_title='Reporting Mineraux',  layout='wide', page_icon=":bar_chart:")
    st.sidebar.title("Menu de navigation")
    pages = {
        "Accueil": static_mineraux,
        "Statistique sur les productions": production,
        "Documentation": documentation
    }
    selection = st.sidebar.radio("", list(pages.keys()), index=0)

    page = pages[selection]
    page()

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
