from html.parser import HTMLParser
import wikipediaapi
import sys
import numpy as np

class Parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.inHead = False
        self.skipData = False
        # self.skipHeaderList = {'history', 'references', 'further reading', 'external links', 'see also', 'controversy', 'notes', 'technique', 'profession', 'education'} # insert h2 headers to avoid here
        self.skipDataLevel = 100 # level > this will be skipped
        self.currDataLevel = 0
        self.levels = [1]

        # with open("skip_header_list.txt",'r') as f:
        # 	l = f.readlines()
        # 	l = [x.split('\n')[0] for x in l]
        # 	self.skipHeaderList = set(l)

        with open('skip_header_list.txt', 'r') as f:
    	    self.skipHeaderList = [line.strip() for line in f]

        with open('accept_header_list.txt', 'r') as f:
            self.acceptHeaderList = [line.strip() for line in f]

    def handle_starttag(self, tag, attrs):
        if tag == 'h2':
            self.inHead = True
            if self.skipDataLevel >= 2:
                self.skipDataLevel = 100
            while self.levels[-1] >= 2:
                self.levels.pop()
            self.levels.append(2)
            # self.skipDataLevel = 2 
            # self.currDataLevel = 2
        elif tag == 'h3':
            self.inHead = True
            if self.skipDataLevel >= 3:
                self.skipDataLevel = 100
            while self.levels[-1] >= 3:
                self.levels.pop()
            self.levels.append(3)
        elif tag == 'h4':   
            self.inHead = True
            if self.skipDataLevel >= 4:
                self.skipDataLevel = 100
            while self.levels[-1] >= 4:
                self.levels.pop()
            self.levels.append(4)
        else:
            return

    def handle_endtag(self, tag):
        if tag == 'h2' or tag == 'h3' or tag == 'h4':
            self.inHead = False
            # self.levels.pop()
        return
        print("End tag  :", tag)

    def handle_data(self, data):
        if self.inHead:
            # for item in self.skipHeaderList:
            #     print(item)
            if data.lower() in self.skipHeaderList:
                self.skipDataLevel = self.levels[-1]
                return
            elif data.lower() in self.acceptHeaderList:
                if self.skipDataLevel > self.levels[-1]:
                    print("**"+data+"**")
                return
            else:
                print("Accept Header? (y/n): " + data.lower(), file=sys.stderr)
                x = input()
                if x.lower() == 'y':
                    if self.skipDataLevel > self.levels[-1]:
                        print("**"+data+"**")
                    self.acceptHeaderList.append(data.lower())
                    return
                else:
                    self.skipDataLevel = self.levels[-1]
                    self.skipHeaderList.append(data.lower())
                    return


        if len(self.levels) == 0 or self.skipDataLevel <= self.levels[-1]:
            # if len(self.levels) != 0:
            #     self.levels.pop()
            return
        print(data,end=' ')

        return

    def save_dicts(self):
    	with open('skip_header_list.txt', 'w') as f:
    		for item in self.skipHeaderList:
        		f.write("%s\n" % item)
    	with open('accept_header_list.txt', 'w') as f:
    		for item in self.acceptHeaderList:
        		f.write("%s\n" % item)

wiki_html = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.HTML)


# pages = ['software_engineering']

# for page_title in pages:

# page_title = sys.argv[1]
# print(page_title)
page_title = 'https://en.wikipedia.org/wiki/Software_design'

page_title = page_title.replace('https://en.wikipedia.org/wiki/', '')

print(page_title)

sys.stdout = open('corpus/raw/'+page_title + '.txt', 'w')

page = wiki_html.page(page_title) # insert title here
print('***'+page_title.replace('_', ' ')+'***')
parser = Parser()
# with open('page.html') as f:
#     data = f.read()
parser.feed(page.text)
parser.save_dicts()