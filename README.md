# MATH4992 Capstone Project

### Topic: PageRank
---

### Improves accuracy by examining term similarity
Investigation on these methods:
1. Jaccard similarity
2. Variational auto encoder
3. Cosine similarity
4. Mix with PageRank

---

### Schedule
This week: Do testing on accuracy (by determining the rank) and complete the report

---

### Dependencies
- Python 2.7
- BeautifulSoup 4
- Requests
- MongoDB Community
- Numpy
- Scipy
- Matplotlib

---

### Command
1. Crawling websites
`python src/Crawler.py -n [integer]`
As our program use BFS Searching on websites, the integer represents the number of layers that the program would search (that is the maximum distance between parent website and most bottom children website)

2. Compute PageRank
`python src/ComputePR.py`
If this is not run after Crawler, we can't do testing and retriving on data by `-option pr`

3. Print all pages in database
`python src/printAllPages.py`
for debug purpose

4. Single search with keyword input
`python src/Retriever.py -option [parameter]`
provided with four options: `cos` `jac` `vae` `pr`

5. Testing program with plotting the graph
`python src/test.py -option [parameter]`
option same as above. This testing will make a regression curve on linear, cubic and quadratic
