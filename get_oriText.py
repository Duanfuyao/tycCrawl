import os
import os.path as path
import selenium
import urllib
import time
from selenium import webdriver

class dataStoreClass():
    def __init__(self,dirPath):
        self.num=0
        self.dirPath=dirPath
        self.companyNameVisited=set()

    def storeData(self,data,title):
        if title in self.companyNameVisited:
            return
        else :
            self.companyNameVisited.add(title)
        start=int(self.num/100)*100+1
        end=int(self.num/100)*100+100
        subDirPath=self.dirPath+'/'+str(start)+'-'+str(end)
        if self.num%100==0:
            if not os.path.exists(subDirPath):
                os.mkdir(subDirPath)
        path=subDirPath+'/'+str(title).replace('/','&')+'.html'
        with open(path,'w') as f:
            f.write(str(data))
            f.close()
        self.num+=1

outPutClass=dataStoreClass('./data_ggzy_processed')

# This folder is custom
def get_allFileNames():
    d = path.dirname(__file__)
    rootdir = d+'/data_ggzy'
    all_fileName=[]
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            fn='file://'+parent+'/'+filename
            all_fileName.append(fn)
    return all_fileName

if __name__=='__main__':
    options = webdriver.FirefoxOptions()
    # options.add_argument("headless")
    options.add_argument('lang=zh_CN.UTF-8')
    # 更换头部
    options.add_argument(
        'user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')

    browser = webdriver.Firefox(executable_path='firefox_driver/geckodriver'
                                , firefox_options=options)
    filenames=get_allFileNames()
    for filename in filenames:
        try:
            browser.get(filename)
            content=browser.find_element_by_css_selector("div[class=detail]")
            title=content.find_element_by_css_selector("h4[class=h4_o]").text
            time=content.find_elements_by_css_selector("p[class=p_o]>span")[0].text
            allContent=content.find_element_by_css_selector("div[class=detail_content]").text
            outPutString= "title:\n"+title+'\ntime:\n'+time+'\ncontent:\n'+allContent
            outPutClass.storeData(outPutString,title)
        except:
            print(filename)
            continue
