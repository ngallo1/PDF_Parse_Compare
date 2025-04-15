import streamlit as st

st.set_page_config(
    page_title="Compare Parsers",
    layout="wide"
)
# st.logo("images/horizontal_blue.png", icon_image="images/icon_blue.png")

home_page = st.Page(
    page="src/streamlit/home.py",
    title="Home",
    icon=":material/home:"
)

# Define data and model
compare_page = st.Page(
    page="src/streamlit/compare.py",
    title="Compare Parsers",
    icon=":material/table_edit:"
)

pages = {
    "Home":
        [home_page],
    "Compare":
        [compare_page],
}

pg = st.navigation(
    pages=pages,
    expanded=True,
)
pg.run()
