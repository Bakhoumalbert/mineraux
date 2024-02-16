import streamlit as st

def documentation():
    st.title(":books: Documentation")
    st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
    st.write("""
        Cette application vous permet de visualiser différentes données.
    """)


if __name__ == "__main__":
    documentation()