import streamlit as st

# Set up session state for page tracking
if 'page' not in st.session_state:
    st.session_state.page = 'home'

st.set_page_config(page_title="NHS Job Tools", page_icon="🔍")

# Sidebar navigation with unique keys
st.sidebar.title("📂 Navigation")
if st.sidebar.button("🏠 Home", key="sidebar_home"):
    st.session_state.page = "home"
    st.rerun()

if st.sidebar.button("🧰 Trac Job Scraper", key="sidebar_trac"):
    st.session_state.page = "trac"
    st.rerun()

if st.sidebar.button("💼 NHS Job Scraper", key="sidebar_nhs"):
    st.session_state.page = "nhs"
    st.rerun()

# Optional top navigation buttons with unique keys
st.markdown("### 🔗 Quick Navigation")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 Home", key="main_home"):
        st.session_state.page = "home"
        st.rerun()
with col2:
    if st.button("🧰 Trac", key="main_trac"):
        st.session_state.page = "trac"
        st.rerun()
with col3:
    if st.button("💼 NHS", key="main_nhs"):
        st.session_state.page = "nhs"
        st.rerun()

# Render content based on selected page
if st.session_state.page == "home":
    st.title("🏠 Welcome to the NHS Job Tools")
    st.markdown("""
Use this app to scrape and filter jobs from:

- 🧰 **Trac.jobs**
- 💼 **NHS Jobs**

Use the navigation buttons above or the sidebar to get started.
""")

elif st.session_state.page == "trac":
    st.title("🧰 Trac Job Scraper")
    import trac

elif st.session_state.page == "nhs":
    st.title("💼 NHS Job Scraper")
    import nhs
