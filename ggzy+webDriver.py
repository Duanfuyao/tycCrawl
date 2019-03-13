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



outPutClass=dataStoreClass('./data_ggzy')

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

def downloadUrl1(url,title):
    BrowserGetUrl(url)
    ele=browser.find_element_by_css_selector("div[class=detailShow]>iframe")
    url2=ele.get_attribute("src")
    downloadUrl(url2,title)

def downloadUrl(url,title):
    BrowserGetUrl(url)
    html = browser.execute_script("return document.documentElement.outerHTML")
    outPutClass.storeData(html,title)

def ignorePage(num):
    for page in range(num):
        pages = browser.find_element_by_link_text("下一页")
        browser.execute_script("arguments[0].click();", pages)
        time.sleep(2)
        #browser.find_elements_by_css_selector("div[class=paging]>a[class=a_righta]")[1].click()

if __name__=='__main__':
    #companyList=loadCompanyName('./data/companyName.txt')
    mainUrl='http://deal.ggzy.gov.cn/ds/deal/dealList.jsp?HEADER_DEAL_TYPE=01'
    BrowserGetUrl(mainUrl)
    time.sleep(30)
    ignoredPage=20
    ignorePage(ignoredPage)
    for x in range(ignoredPage,403):
        '''
        browser = webdriver.Chrome()
        browser.get('https://www.baidu.com')
        browser.execute_script('window.open()')

        print(browser.window_handles)  # 获取所有的选项卡
        browser.switch_to_window(browser.window_handles[1])
        browser.get('https://www.taobao.com')
        time.sleep(10)
        browser.switch_to_window(browser.window_handles[0])
        browser.get('https://www.sina.com.cn')
        browser.close()
        '''
        try:
            print(x)
            titles = []
            hrefs = []
            footerlist=browser.find_elements_by_css_selector("div[class=publicont]")
            for ele in footerlist:
                e=ele.find_element_by_css_selector("div>h4>a")
                titles.append(e.text)
                hrefs.append(e.get_attribute('href'))
            print("len: "+str(len(titles)))
            t_start=time.time()
            for i in range(len(titles)):
                try:
                    browser.execute_script('window.open()')
                    print(browser.window_handles)
                    browser.switch_to.window(browser.window_handles[1])
                    downloadUrl1(hrefs[i], titles[i])
                    browser.close()
                    browser.switch_to.window(browser.window_handles[0])
                    time.sleep(5)
                except:
                    i - 1
                    time.sleep(10)
                    continue
            t_end = time.time()
            print("total time : "+str(t_end-t_start))
            #a=browser.find_element_by_css_selector("div[class=paging]>a[class=a_righta]")
            ignorePage(1)
        except:
            print("ignore this page")
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
