# MATH4992 Capstone Project

### Topic: PageRank
---

### Scope 1: Improves accuracy by examining term similarity
Tentative methods:
1. Jaccard similarity
2. Latent semantic indexing
3. Word mover's distance
4. Variational auto encoder
5. Cosine similarity

### Scope 2: Improves efficiency by investigating how to fine the eigenvalue of PageRank matrix
Tentative approaches:
1. Dynamic systems
2. Linear algebra
3. Probabilistic point of view
---

### Components
1. Crawler to scrape the raw data from given webpages
2. Database management system to store the data (divide into several parts to fit different methods)
3. Reducer to work around with the data and calculate the values
4. Retriever to retrieve the values
5. Interface
---

### Schedule
This week: Implement Retriever and Ranker, investigate LSI, word movers and variational auto encoder

---

### Instruction to Andy
Install BeautifulSoup and Requests for your python using pip, or else you cannot run.

Follow the commands here:

`sudo easy_install pip`

`sudo pip install bs4`

`sudo pip install requests`

`sudo pip install mongodb`

Homebrew dependency:
`brew install mongodb`
