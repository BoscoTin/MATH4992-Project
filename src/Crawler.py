import requests, sys, re, string
from bs4 import BeautifulSoup
import Processor
import Indexer


class Crawler:

    def __init__(self, numOfLayer):
        self.num = numOfLayer;
        self.parent = []
        self.children = []

        link = "http://www.cse.ust.hk/"

        self.parent.append(link)

    def getOnePage(self):
        parent = self.parent.pop(0)
        print ""
        print "Searching {}".format(parent)
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

        # get all child links from the site
        children = []
        for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
            children.append(link.get('href'))

        #children = Processor.process(children)
        for child in children:
            print "{}".format(child)
            self.children.append(child)

        # give the data to indexer
        Indexer.process(parent, words, children)

    # search by BFS
    def scrape(self):
        for i in range(self.num):
            print ""
            print "Searching layer {}".format(i)

            # clear duplicate brought by multithread
            #self.parent = Processor.process(self.parent)

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
