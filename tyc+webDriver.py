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
        start=int(self.num/100)+1
        end=int(self.num/100)+100
        subDirPath=self.dirPath+'/'+str(start)+'-'+str(end)
        if self.num%100==0:
            if not os.path.exists(subDirPath):
                os.mkdir(subDirPath)
        path=subDirPath+'/'+str(title).replace('/','&')+'.html'
        with open(path,'w') as f:
            f.write(str(data))
            f.close()
        self.num+=1



outPutClass=dataStoreClass('./data')

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
    companyList=loadCompanyName('./data/companyName.txt')
    mainUrl='https://www.tianyancha.com/search/t301?key='
    BrowserGetUrl(mainUrl + 'test')
    time.sleep(100)
    for name in companyList:
        print(name)
        nameQuote=urllib.parse.quote(name)
        BrowserGetUrl(mainUrl+nameQuote)
        pageUrl=[]
        footerlist=browser.find_elements_by_css_selector("ul[class=pagination]>li")
        for ele in footerlist:
            pageUrl.append(ele.find_element_by_css_selector("a").get_attribute('href'))
        for i in range(min(10,len(pageUrl))):
            BrowserGetUrl(pageUrl[i])
            aimList=browser.find_elements_by_css_selector("div[class=result-list]>div[class=search_result_type]")
            titles=[]
            hrefs=[]
            for ele in aimList:
                e=ele.find_element_by_css_selector("div[class=filter_risk]>div[class=risk-title]>a")
                title=e.text
                #if title.find(u'招标') == -1: continue
                #if title.find(u'二次') != -1: continue
                href=e.get_attribute('href')
                titles.append(title)
                hrefs.append(href)
            for i in range(len(titles)):
                try:
                    BrowserGetUrl(hrefs[i])
                    ee = browser.find_element_by_css_selector("div[class=subheading]>a")
                    href = ee.get_attribute('href')
                    downloadUrl(hrefs[i], titles[i])
                except:
                    i-1
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
