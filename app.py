from math import log
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

# Processing URL as status update in st.text_area
log_area = st.empty()
if "runner" in ss:
    for message in ss.runner.crawl():
        # log_area.text_area("Processing URL", message)
        log_area.text_area("Processing the following url ⏬⏬ ", message)











    
st.write(st.session_state)
