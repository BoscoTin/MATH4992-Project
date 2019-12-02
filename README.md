MATH4992 Capstone Project
=========================

### Topic: PageRank accuracy enhancement

A python program to help the project calculations with hundred or thousand times of search. We have tried to merge PageRank with other text similarity measures but not very accurate and not professional enough. However, I think it is a good practice to implement a search engine.

---

### Dependencies

-	Python 2.7
-	BeautifulSoup 4
-	Requests
-	MongoDB Community
-	Numpy
-	Scipy
-	Matplotlib

---

### Command

-	Crawling websites

`python src/Crawler.py -n [integer]`

As our program use BFS Searching on websites, the integer represents the number of layers that the program would search (that is the maximum distance between parent website and most bottom children website)

-	Compute PageRank

`python src/ComputePR.py`

If this is not run after Crawler, we can't do testing and retriving on data by `-option pr`

-	Print all pages in database

`python src/printAllPages.py`

for debug purpose

-	Single search with keyword input

`python src/Retriever.py -option [parameter]`

provided with four options:

`cos` `jac` `vae` `pr` `mix`

-	Testing program with plotting the graph

`python src/test.py -option [parameter]`

option same as above. This testing will make a regression curve on linear, quadratic, cubic and poly fit curve on max 32-dimensions (consider the number of keywords in the desired page is how many)
