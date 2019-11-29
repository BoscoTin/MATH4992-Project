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
            if "cse.ust.hk" in links[i] and "http" == links[i][0:4]:
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
        filetypes = [".mpeg", ".mpg", ".py", ".js", ".sql", ".csv", ".zip", ".tar", ".gz", ".tif", ".apk", ".rar", ".pdf", ".png", ".svg", ".ps", ".ai", ".wav", ".mp3", ".mp4", ".wmv", ".avi", ".bmp", ".jpg", ".jpeg", "#", "?", ".ppt", ".xls", ".doc", ".bib", ".cgi"]
        i = 0
        while i < len(links):
            link = links[i].lower()
            isDelete = False
            for file in filetypes:
                if file in link:
                    isDelete = True
                    break
            if isDelete != True:
                processedLinks.append(links[i])
            i += 1
        return processedLinks

    def clearDuplicate(self, links):
        # clear the duplicate links here
        processedLinks = []
        annoying = ""
        for url in links:
            annoying = url + "/"
            annoying2 = url[:-1]
            if url not in processedLinks and annoying not in processedLinks and annoying2 not in processedLinks:
                processedLinks.append(url)
        return processedLinks
