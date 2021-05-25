# Auther @RahulDubey 
# Blog: https://deviloper.in/crawl-videos-with-selenium-using-python

#importing required Libraries 
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from vimeo_downloader import Vimeo
import timeit
import urllib

#declaring variables
Output_file=r"path\to\output\folder\video_urls.xlsx"
xls_content=[]
genres=['fashion portrait']
url='https://www.pexels.com/search/videos/'
path = r'path\to\chrome\webdriver\chromedriver.exe'


def download_vimeo(vimeo_url,embedded_on,genre):
    v = Vimeo(vimeo_url, embedded_on) 
    stream = v.streams # List of available streams of different quality
    # >> [Stream(240p), Stream(360p), Stream(540p), Stream(720p), Stream(1080p)]
    
    filename=urllib.parse.unquote(genre)+"-"+vimeo_url.split('/')[-1]
    # Download best stream
    stream[-1].download(download_directory = 'video', filename = filename)


def extractingImages(driver,genre):
    print(f"Extracting {genre} Video URL after 10 secs....")
    sleep(10) # let it load the post properly
    images = driver.find_elements_by_tag_name('source')
    for image in images:
        src=image.get_attribute('src')
        vlink=src.split(".sd.mp4")[0].replace("https://player.vimeo.com/external/","https://player.vimeo.com/video/")
        temp={}
        temp['Genre']=(url+genre).split('/')[-1].replace("%20"," ").upper()
        temp['Image URL']=vlink
        xls_content.append(temp)
        download_vimeo(vlink,url,genre)

    


#loading genre using webdriver
def loadpage(driver,genre):
    driver.get(url+genre) #load the url
    sleep(10) # wait for 10 secs so that website loads properly
    
    # scrolling the page for 2 minutes
    starttime = timeit.default_timer()
    i=0
    while i<=120:
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        sleep(0.5)
        i= round(timeit.default_timer() - starttime)
        
    # extract the images from the page
    extractingImages(driver,genre)    
    
    

if __name__ =="__main__":
    
    #setting web driver
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
#     options.add_argument('headless')
    driver = webdriver.Chrome(options=options,executable_path = path)
    
    # looping through each keyword
    for genre in genres:
        genre=urllib.parse.quote(genre)
        loadpage(driver,genre)
        
    driver.close()   
    xls_data = pd.DataFrame(xls_content)
    xls_data.to_excel(Output_file, engine='xlsxwriter', index=False)
    


