from PyPDF2 import PdfFileReader
 
 
def text_extractor(path):
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
 
        for i in range(19,809):    
            # get the first page
            page = pdf.getPage(i)
            # print(page)
            # print('Page type: {}'.format(str(type(page))))

            text = page.extractText()
            file1 = open("os_book_silberschatz.txt","a")#append mode 
            file1.write(text) 
            file1.write("\n")
            file1.close() 
            # print(text)
 
 
if __name__ == '__main__':
    path = 'os.pdf'
    text_extractor(path)

# import fitz

# pdf_document = "os.pdf"
# doc = fitz.open(pdf_document)
# # print ("number of pages: %i" % doc.pageCount)
# # print(doc.metadata)


# # print(page1text)

# for i in range(466,469):    
#             # get the first page
#             page1 = doc.loadPage(i)
#             page1text = page1.getText("text")
#             file1 = open("myfile.txt","a")#append mode 
#             file1.write(page1text) 
#             file1.close() 
