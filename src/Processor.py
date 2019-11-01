class Processor:

    def changeUrl(self, links):
        i = 0
        while i < len(links):
            if links[i][0:5] == "https":
                links[i].replace("https", "http")
            i += 1
        return links

    def clearSubfix(self, links):
        # As links may have /index.html, /# , / at the end
        # all are the same link
        # please clear them
        processedLinks = []
        i = 0
        while i < len(links):
            j = 0
            count = 0
            while j < len(links[i]):
                if links[i][j:j + 1] == "/" and count == 2:
                    if len(links[i]) == (j + 11) and links[i][j:j + 11] == "/index.html":
                        processedLinks[i].append(links[i][0:j - 1])
                    elif len(links[i]) == (j + 2) and links[i][j:j + 2] == "/#":
                        processedLinks[i].append(links[i][0:j - 1])
                    elif len(links[i]) == (j + 1) and links[i][j:j + 1] == "/":
                        processedLinks[i].append(links[i][0:j - 1])
                elif links[i][j:j + 1] == "/" and count < 2:
                    count += 1
                    j += 1
            processedLinks[i].append(links[i])
            i += 1
        return processedLinks

    def clearUnwantedFiles(self, links):
        # limit the file such that no .pdf, no .png, no .jpg can be placed
        processedLinks = []
        i = 0
        while i < len(links):
            temp = len(links[i]) - 4
            if links[i][temp:temp + 3] != ".pdf" or \
                    links[i][temp:temp + 3] != ".png" or \
                    links[i][temp:temp + 3] != ".jpg":
                processedLinks.append(links[i])
            i += 1
        return processedLinks

    def clearDuplicate(self, links):
        # clear the duplicate links here
        processedLinks = []
        for url in links:
            if url not in processedLinks:
                processedLinks.append(url)
        return processedLinks


def process(links):
    processor = Processor()
    processedLinks = processor.clearUnwantedFiles(links)
    processedLinks = processor.clearSubfix(processedLinks)
    result = processor.clearDuplicate(processedLinks)

    return result
