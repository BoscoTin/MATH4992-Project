import requests, sys, re, string
from bs4 import BeautifulSoup
from Processor import Processor
from Indexer import Indexer

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

        link = "http://www.cse.ust.hk/"

        self.parent.append(link)

    def handleLink(self, parent, links):
        processedLinks = self.Processor.startWithParents(parent, links)
        processedLinks = self.Processor.waiveUnrelatedDomain(processedLinks)
        processedLinks = self.Processor.clearSubfix(processedLinks)
        processedLinks = self.Processor.clearUnwantedFiles(processedLinks)
        processedLinks = self.Processor.changeUrl(processedLinks)

        return self.Processor.clearDuplicate(processedLinks)

    def getOnePage(self):
        parent = self.parent.pop(0)

        if parent not in self.handled:
            self.handled.append(parent)
            print ""
            print "Searching {}".format(parent)
            try:
                request = requests.get(parent)
                # check if the page can be connected successfully
                if request.status_code == requests.codes.ok:
                    soup = BeautifulSoup(request.text, 'html.parser')

                    # get raw text and split it
                    rawtags = soup.find_all('p')
                    temp = []
                    for tag in rawtags:
                        temp = temp + tag.getText().split()

                    # replace punctuation by white space and split
                    words = []
                    for word in temp:
                        rawtext = word.encode('utf-8').strip()
                        for c in string.punctuation:
                            rawtext = rawtext.replace(c, " ")
                        words += rawtext.split()

                    # process the words
                    processedWords = []
                    for word in words:
                        processedWords.append(self.Porter.stem(word))

                    for word in processedWords:
                        print word

                    # get all child links from the site
                    children = []
                    for link in soup.findAll('a', href=True):
                        children.append(link.get('href'))

                    children = self.handleLink(parent, children)
                    for child in children:
                        try:
                            mynewstring = child.encode('ascii')
                            print mynewstring
                        except UnicodeEncodeError:
                            print("there are non-ascii characters in there")
                        self.children.append(child)

                    # give the data to indexer
                    self.Indexer.process(parent, processedWords, children)

            except requests.exceptions.ConnectionError:
                print "Error in connecting the site."


    # search by BFS
    def scrape(self):
        for i in range(self.num):
            self.parent = self.handleLink("", self.parent)
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
