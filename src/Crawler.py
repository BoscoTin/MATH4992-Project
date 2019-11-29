import requests, sys, re, string
from bs4 import BeautifulSoup
from Processor import Processor
from Indexer import Indexer
from urlparse import urljoin
import string
import DBManager
db = DBManager.instance('wordcount')

from nltk.stem import PorterStemmer


class Crawler:

    def __init__(self, numOfLayer):
        self.num = numOfLayer;
        self.parent = []
        self.children = []
        self.handled = []
        self.Indexer = Indexer()
        self.Processor = Processor()
        self.Porter = PorterStemmer()
        self.db = []

        link = "http://www.cse.ust.hk/"
        self.parent.append(link)

    def handleLink(self, links):
        processedLinks = self.Processor.waiveUnrelatedDomain(links)
        processedLinks = self.Processor.clearSubfix(processedLinks)
        processedLinks = self.Processor.clearUnwantedFiles(processedLinks)
        processedLinks = self.Processor.changeUrl(processedLinks)

        return self.Processor.clearDuplicate(processedLinks)

    def getOnePage(self):
        parent = self.parent.pop(0)

        if parent not in self.handled:
            print ""
            print "Searching {}".format(parent)
            try:
                request = requests.get(parent, timeout=20)
                # check if the page can be connected successfully
                if request.status_code == requests.codes.ok:
                    soup = BeautifulSoup(request.text, 'html.parser')
                    # get all child links from the site
                    children = []
                    for link in soup.findAll('a', href=True):
                        children.append( urljoin( parent, link.get('href') ) )

                    children = self.handleLink(children)
                    for child in children:
                        try:
                            mynewstring = child.encode('ascii')
                            print mynewstring
                        except UnicodeEncodeError:
                            print("there are non-ascii characters in there")
                        self.children.append(child)

                    # words exist in database?
                    if parent not in self.db:
                        # get raw text and split it
                        rawtags = soup.find_all('p')
                        temp = []
                        for tag in rawtags:
                            temp = temp + tag.getText().split()
                        # replace punctuation by white space and split
                        words = []
                        for word in temp:
                            rawtext = word.encode('utf-8').strip()
                            rawtext = "".join(i for i in rawtext if ord(i)<128)
                            for c in string.punctuation:
                                rawtext = rawtext.replace(c, " ")
                            words += rawtext.split()
                        # process the words
                        processedWords = []
                        for word in words:
                            processedWords.append(self.Porter.stem(word))
                        # give the data to indexer
                        if len(processedWords) != 0:
                            self.Indexer.process(parent, processedWords, children)
                        else:
                            print "The document contains no word"

            except requests.exceptions.ConnectionError:
                print "Error in connecting the site."
            except requests.exceptions.Timeout:
                print "Timeout in connecting the site."

        self.handled.append(parent)


    # search by BFS
    def scrape(self):
        all = db.getAll()
        for instance in all:
            self.db.append(instance['url'])
        print len(self.handled)

        for i in range(self.num):
            self.parent = self.handleLink(self.parent)
            print ""
            print "Searching layer {}".format(i)

            if (len(self.parent) == 0):
                break

            for i in range(len(self.parent)):
                self.getOnePage()

            self.parent = self.children
            self.children = []
# Class Crawler ends

# exit function
def terminate():
    print "To run Crawler, type python [path]/Crawler.py [control] [parameter]... in your terminal"
    print "Parameter List:"
    print "-n [integer] : define number of child link explored by the Crawler"
    sys.exit()

# main function is here
def main():
    argv = sys.argv
    numOfLayer = 0
    if "-n" in argv:
        index = argv.index("-n")
        if(str.isdigit(argv[index + 1])):
            numOfLayer = int(argv[index + 1])
        else:
            terminate()
    else:
        terminate()

    crawler = Crawler(numOfLayer)
    crawler.scrape()

if __name__ == "__main__":
    main()
