class Processor:
    def clearSubfix(self, links):
        # As links may have /index.html, /# , / at the end
        # all are the same link
        # please clear them
        processedLinks = []
        return processedLinks

    def clearUnwantedFiles(self, links):
        # limit the file such that no .pdf, no .png, no .jpg can be placed
        processedLinks = []
        return processedLinks

    def clearDuplicate(self, links):
        # clear the duplicate links here
        processedLinks = []
        return processedLinks

def process(links):
    processor = Processor()
    processedLinks = processor.clearUnwantedFiles(links)
    processedLinks = processor.clearSubfix(processedLinks)
    result = processor.clearDuplicate(processedLinks)

    return result
