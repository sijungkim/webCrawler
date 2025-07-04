make reusable crawler/scraper
- use streamlit to get the base url to define the scope and boundary
- capture output just in case of any failure, so, I can import the output file to restart or analyze
- think how to simplify the data exchange between each step of work inside streamlit (it's basically stateless unless session_state)

functions to have:
1. crawl entire web page
    crawl
    result_output (discovered_url and unavailable_url)
        - next phase: what each page is about
    depth of the pages to crawl
        - need to remember the current depth
    restart from where it's left off

2. scrape necessary data
    option to select the scope (current page? or entire page?)
    option to select resource type
    how the output should be displayed?
    select the location of TEXT where it appears (url and identifiable block)