explore.py - This file contains the source code.

I ran explore.py with Python 3.5.2.

This program, starting from a given webpage, constructs a directed graph whose nodes are top-level domains and edges are links. The graph constructed represents a ball (in the graph "metric") whose radius is less than the value of MAX_DEPTH specified in explore.py. Even with a radius as small as 3, the constructed graph can be enormous.

Using Requests, we get a webpage as text. Using Beautiful Soup, we find all the links in the webpage. Using urlparse and get_tld, we find the top-level domains to which the links point. Recursively, we get the corresponding webpages and repeat.
