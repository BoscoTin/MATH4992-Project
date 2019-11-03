class Processor:

    def changeUrl(self, links):
        i = 0
        while i < len(links):
            if links[i][0:5] == "https":
                links[i] = "http" + links[i][5:]
            i += 1
        return links

    def waiveUnrelatedDomain(self, links):
        # Waive all the link which are not in .ust.hk domain
        processedLinks = []
        i = 0
        while i < len(links):
            if "ust.hk" in links[i]:
                processedLinks.append(links[i])
            i += 1
        return processedLinks

    def clearSubfix(self, links):
        # As links may have /index.html, /# , / at the end
        # all are the same link
        # please clear them
        processedLinks = []
        i = 0
        while i < len(links):
            if "index.html" in links[i]:
                links[i].replace("/index.html", "")
            elif "/#" in links[i]:
                links[i].replace("/#", "")
            elif "/" in links[i]:
                links[i].replace("/", "")
            processedLinks.append(links[i])
            i += 1
        return processedLinks

    def clearUnwantedFiles(self, links):
        # limit the file such that no .pdf, no .png, no .jpg can be placed
        processedLinks = []
        i = 0
        while i < len(links):
            if ".pdf" not in links[i] and ".png" not in links[i] and ".jpg" not in links[i]:
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
