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
1. Crawler to scrape the raw data from given webpages (90% completed)
2. Database management system to store the data (divide into several parts to fit different methods) (90% completed)
3. Ranker to work around with the data and calculate the values (20% completed)
4. Retriever to retrieve the values (10% completed)
5. Interface (0% completed)
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

As our program use MongoDB to store the website data, please install the following dependency to prevent the error happens

`sudo pip install mongodb`

Homebrew dependency:
`brew install mongodb-community`

then

`mkdir -p /data/db`

``sudo chown -R `id -un` /data/db``

run `mongod` to open MongoDB
