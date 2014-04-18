# crawler.py
# Build the corpus pre-query

###
### crawler.py
###

from webcorpus import WebCorpus
from getpage import get_page
from bs4 import BeautifulSoup

def get_all_links(page):
    soup = BeautifulSoup(page)
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    return links

def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)
        
def add_to_index(index, keyword, url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]
    
def crawl_web(seed): # returns index, graph of inlinks
    tocrawl = set([seed])
    crawled = []
    wcorpus = WebCorpus()
    while tocrawl: 
        url = tocrawl.pop() # changed page to url - clearer name
        if url not in crawled:
            content = get_page(url)
            outlinks = get_all_links(content)
            for outlink in outlinks:
                wcorpus.add_link(url, outlink) 
            for word in content.split():
                wcorpus.add_word_occurrence(url, word)
            tocrawl.update(outlinks)
            crawled.append(url)
    return wcorpus

def compute_ranks(wcorpus, d = 0.8, numloops = 10):
    """compute page ranks for the input web index.  d is the damping factor."""
    ranks = {}
    graph = wcorpus.graph
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank = newrank + d * (ranks[node] / len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    wcorpus.ranks = ranks
