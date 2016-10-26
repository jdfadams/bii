# Thinking of the internet as a directed graph, we draw a ball of a given radius.
# For our purposes, vertices are top-level domains, and directed edges are links.
# There is a "distance" induced by following directed edges.
# Starting from center = "somewebsite.com", we follow links to other top-level domains.
# We build a directed graph consisting of websites less than MAX_DEPTH away from center.
# We output the resulting graph.

# To make the rendered graph look prettier, one might call, for example, "neato -Tpdf -Gsplines=true -Goverlap=scale -O [file.gv]".

from bs4 import BeautifulSoup # for finding links in websites
from tld import get_tld # for finding top-level domains
from urllib.parse import urlparse # for checking whether a link is "http://website.com/subpath" or "/subpath"
import requests # for getting a webpage

from graphviz import Digraph # for drawing directed graphs

MAX_DEPTH = 2 # the radius around the center
visited = {}

# This function allows us to print to the screen in a "nested" way.
def printWithDepth(text, depth):
 space = ""

 # Put depth spaces.
 for i in range(depth):
  space += " "

 # Print text with the added spaces.
 print(space + text)


# Get all the top-level domains to which website links.
# website should of the form "somewebsite.com"
def get_all_links(website):
 # Get website using requests.get.
 try:
  r = requests.get("http://" + website)
 except:
  print("<<<requests.get threw an exception>>>")
  return []

 links = [] # This will be the list of top-level domains to which website links.

 # Extract all the links using BeautifulSoup.
 soup = BeautifulSoup(r.text, "lxml") # If we don't specify "lxml" or some other parser, we'll get a warning.
 for link in soup.find_all("a"):
  href = link.get("href")

  # Make sure that href is suitable for urlparse.
  if type(href) is not str:
   print("<<<href is not a string!>>>")
   continue

  # Check whether the link goes to another domain or to a subdomain.
  # We don't want to bother with href="/subdomain".
  to_url = urlparse(href)
  if to_url.netloc == '':
   continue

  # Get the top-level domain.
  try:
   to_website = get_tld(href)
  except:
   print("<<<tld threw an exception>>>")
   continue

  # We don't want to record that a website links to itself.
  if to_website == website:
   continue

  # At this point, we have a valid link that goes some other domain.
  # Record it.
  if to_website not in links:
   links.append(to_website)

 return links


# This is the starting point of our web exploration.
# website should be of the form "somewebsite.com".
# When the user calls explore, depth should be 0.
def explore(website, depth = 0):
 printWithDepth("explore(\"" + website + "\", " + str(depth) + ")", depth)
 if depth < MAX_DEPTH:
  if website in visited:
   printWithDepth("We already visited " + website, depth + 1)
  else:
   printWithDepth("Exploring " + website, depth + 1)
   visited[website] = get_all_links(website)
   for link in visited[website]:
    explore(link, depth + 1)
 else:
  printWithDepth("Maximum depth exceeded before we could explore " + website, depth + 1)


# This where we start doing things.
center = "python.org" # The center of our ball in the internet.
explore(center)

# Build a graph, and render it.
file_name = center + ".gv"
dg = Digraph(comment = "A ball in the internet, centered at " + center + ", with radius <" + str(MAX_DEPTH))

# Let's shorten the names of the vertices.
# We will record the website that each vertex represents.
v = {}
count = 0
for a in visited:
 if a not in v:
  v[a] = "v" + str(count)
  count += 1
  dg.node(v[a], a) # Vertex v[a] has label a.

# Draw all the directed edges.
for a in visited:
 for b in visited[a]:
  # Only draw b if it leads to another vertex in our graph.
  if b in visited:
   dg.edge(v[a], v[b])

dg.render(file_name, view = True) # Output the GraphViz source, a PDF rendering, and view the PDF.

print("Finished rendering " + file_name) # Tell the user we've finished.
