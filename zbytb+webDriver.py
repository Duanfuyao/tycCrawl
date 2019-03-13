import selenium
import urllib
import os
import time
from selenium import webdriver
numThread=1
options = webdriver.FirefoxOptions()
#options.add_argument("headless")
options.add_argument('lang=zh_CN.UTF-8')
# 更换头部
options.add_argument('user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')

browser  = webdriver.Firefox(executable_path='firefox_driver/geckodriver'
                            ,firefox_options=options)
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



outPutClass=dataStoreClass('./data_zbytb')

def loadCompanyName(path):
    companyRet=[]
    f = open(path)#"companyName.txt"
    line = f.readlines()
    for l in line:
        companyRet.append(l)
    f.close()
    return companyRet

def BrowserGetUrl(url):
    try:
        browser.get(url)
        time.sleep(2)
    except:
        browser.refresh()
        browser.get(url)
        time.sleep(10)

def downloadUrl(url,title):
    BrowserGetUrl(url)
    html = browser.execute_script("return document.documentElement.outerHTML")
    outPutClass.storeData(html,title)


if __name__=='__main__':
    #companyList=loadCompanyName('./data/companyName.txt')
    mainUrl='https://www.zbytb.com/gongcheng'
    BrowserGetUrl(mainUrl)
    time.sleep(30)
    for x in range(2500):
        print(x)
        u=mainUrl+'-'+str(x+1)+'.html'
        print(u)
        #nameQuote=urllib.parse.quote(name)
        BrowserGetUrl(u)
        titles = []
        hrefs = []
        footerlist=browser.find_elements_by_css_selector("table[class=zblist_table]>tbody>tr[class=hover_tr]")
        for ele in footerlist:
            e=ele.find_element_by_css_selector("td[class=zblist_xm]>a")
            titles.append(e.text)
            hrefs.append(e.get_attribute('href'))
        for i in range(len(titles)):
            try:
                downloadUrl(hrefs[i], titles[i])
                time.sleep(5)
            except:
                i - 1
                time.sleep(10)
                continue
#options = webdriver.ChromeOptions()
#options.add_argument("headless")
#options.add_argument('lang=zh_CN.UTF-8')
# 更换头部
#options.add_argument('user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')

#browser  = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
 #                           ,chrome_options=options
 #                           )

#def crawlCompanyData(oriData,url,index):
