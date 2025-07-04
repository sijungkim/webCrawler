import streamlit as st
from webCrawler import Crawler

ss = st.session_state

col1, col2 = st.columns(2)

with col1:
    ss.mode_selector = {'Crawler':Crawler, 'Scraper':'Scraper'}
    ss.mode = st.selectbox("SELECT MODE", ss.mode_selector.keys())
with col2:
    ss.url = st.text_input("please enter url to start off, then ENTER")
with col1:
    with st.spinner("Crawling in PROGRESS"):
        if st.button(f"Start {ss.mode} on '{ss.url}'"):
            ss.runner = ss.mode_selector[ss.mode](ss.url)
            ss.runner.crawl()






    
st.write(st.session_state)
