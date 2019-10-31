import requests
import sys
import re
import threading
from bs4 import BeautifulSoup
import Processor


class Crawler:

    def __init__(self, numOfLayer):
        self.num = numOfLayer;
        self.parent = []
        self.children = []

        link = "https://www.cse.ust.hk/ug/comp1991"

        self.parent.append(link)

    def getOnePage(self):
        link = self.parent.pop(0)
        request = requests.get(link)

        # check if the page can be connected successfully
        if request.status_code == requests.codes.ok:
            soup = BeautifulSoup(request.text, 'html.parser')

        # print(soup.get_text())

        # get all child links from the site
        children = []
        for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
            children.append(link.get('href'))

        children = Processor.process(children)
        for link in children:
            print "{}".format(link)
            self.children.append(link)


    # search by BFS
    def scrape(self):
        for i in range(self.num):
            print "Searching layer {}".format(i)

            # clear duplicate brought by multithread
            self.parent = Processor.process(self.parent)

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
    print "-numOfLayer [integer] : define number of child link explored by the Crawler"
    sys.exit()

# main function is here
def main():
    argv = sys.argv
    numOfLayer = 0
    if "-numOfLayer" in argv:
        index = argv.index("-numOfLayer")
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
