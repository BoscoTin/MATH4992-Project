import sys
import Retriever
import DBManager

option = 'pr'
desiredPage = 'http://www.cse.ust.hk'

db = DBManager.instance('wordcount')
record = db.findRecord({'url': desiredPage})
wordlist = record['words']


scores, time = Retriever.rank(option, wordlist)

Retriever.custom_print(option, scores)
