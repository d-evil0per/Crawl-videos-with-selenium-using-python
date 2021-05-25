Check my blog [Crawl videos with selenium using python ]() for more details

Let's code step by step. First, We will import all the required libraries and learn why we have used them.
```python
#importing required Libraries 

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from vimeo_downloader import Vimeo
import timeit
import urllib
```
-  [import pandas as pd](https://pandas.pydata.org/docs/getting_started/index.html)  - to create a data frame and save the data frame into the excel sheet.
-  [from selenium import webdriver](https://selenium-python.readthedocs.io/api.html) - Selenium WebDriver is an automated testing framework used for the validation of websites 
Selenium WebDriver for popular browsers can be downloaded from the links mentioned below:

| Browser           | DOWNLOAD LOCATION                                                     |
|-------------------|-----------------------------------------------------------------------|
| Firefox           | https://github.com/mozilla/geckodriver/releases                       |
| Chrome            | http://chromedriver.chromium.org/downloads                            |
| Internet Explorer | https://github.com/SeleniumHQ/selenium/wiki/InternetExplorerDriver    |
| Microsoft Edge    | https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/ |

-  [from selenium.webdriver.common.keys import Keys](https://www.geeksforgeeks.org/special-keys-in-selenium-python/) - allows pressing keys through keyboard such as ctrl+f, or shift+c+v, etc.
-  [from time import sleep](https://realpython.com/python-sleep/) - Add time delay in the code
-  [from vimeo_downloader import Vimeo](https://pypi.org/project/vimeo-downloader/) - for downloading the videos.
-  [import timeit](https://docs.python.org/3/library/timeit.html) - Measure execution time of small code snippets.
-  [import urllib](https://docs.python.org/3/library/urllib.html) - we have used the `urllib.parse.quote` & `urllib.parse.unquote` module to encode/decode the URL  in a proper format.

Now let's move forward and declare some variables.

```python
#declaring variables
Output_file=r"<path to output directory>\video_urls.xlsx"
xls_content=[]
genres=['fashion portrait']
url='https://www.pexels.com/search/videos/'
path = r'<path to Chrome driver directory>\chromedriver.exe'
```
here replace `<path to output directory>` to the absolute path of the directory where you want to store the excel file and replace `<path to Chrome driver directory>` with the absolute path of the Chrome Driver that you have downloaded from the above table.

Now let's create a [<code>if __name__ == "__main__"</code>](https://www.freecodecamp.org/news/if-name-main-python-example/) function to proceed further.

```python
if __name__ =="__main__":
    
    #setting web driver
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    driver = webdriver.Chrome(options=options,executable_path = path)
    
    # looping through each keyword
    for genre in genres:
        genre=urllib.parse.quote(genre)
        loadpage(driver,genre)
        
    driver.close()   
    xls_data = pd.DataFrame(xls_content)
    xls_data.to_excel(Output_file, engine='xlsxwriter', index=False)
```
In the above block of code we performed these steps shown below:
- created an object `driver` of the chrome `web driver with some options.
- Looped through each element in the genres list and did URL encoding in the genre name and passed it as an argument to the  function called `loadpage` along with web driver object
- closed the driver object with `driver.close()` statement.
- created the data frame from the list containing a list of video URLs and keywords.
- saved those list of data in an excel sheet.

Now, let's check what is this `loadpage` function is written for.

```python
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
``` 
In this function

- we are loading the URL by using `driver.get(url+genre)` and then waits for 10 secs so that the website gets loaded completely. 
- we are sending keypress `PAGE_DOWN` to scroll the web page for at least 2 mins to load more videos on the page. As videos are getting loaded from the javascript on scroll. we need to programmatically scroll the page with a delay of 0.5 secs for 2 minutes.
```python
starttime = timeit.default_timer()
 i=0
while i<=120:
    driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
    sleep(0.5)
    i= round(timeit.default_timer() - starttime)
```
where `starttime` contains the time at which we started scrolling and we keep on scrolling until we get **the difference of the current time and start time greater than 120 secs i.e 2 mins**

- then we call the **extractingImages** with driver and genre as arguments.

Let's define the function **extractingImages** and see how can we extract images.
```python
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
```
- at the starting, we are delaying the code by 10 secs to let the webpage load its contains properly.
- then we are finding the `source` tag from the website content and looping all matched results to extract the `src` attribute value from it.
- we are transforming the URL to the desired URL as discussed in our planning stage.
- next, we are creating a dictionary for each URL found along with the keyword and stored it in a list. so that we can save the records in the excel sheet under the main block.
- we have called another function named `download_vimeo` by passing the video link, page URL, and genre to download the videos.

Let's write the `download_vimeo` function and see how videos are getting downloaded from the links.

```python
def download_vimeo(vimeo_url,embedded_on,genre):
    v = Vimeo(vimeo_url, embedded_on) 
    stream = v.streams # List of available streams of different quality
    # >> [Stream(240p), Stream(360p), Stream(540p), Stream(720p), Stream(1080p)]
    
    filename=urllib.parse.unquote(genre)+"-"+vimeo_url.split('/')[-1]
    # Download best stream
    stream[-1].download(download_directory = 'video', filename = filename)
```
- In the above function we created an object of `Vimeo` class defined in `vimeo_downloader` package.
- listed all the available stream data of different quality from `v.streams` and stored it in a variable called `stream`.
- Now we are creating a filename by un-quoting the genre and by concatenating it with the id extracted from the video URL.
for example, `filename='Food photography'+"-"+"511722602"` i.e `Food photography-511722602`
- Now we are fetching the best available quality from last index from stream variable i.e `stream[-1]` and calls the download function with arguments like folder path and filename. It will download the file `Food photography-511722602.mp4` in folder name `video` under the current working directory. Like this, it will download all the files from the extracted video links.

Now let's check the output of the script when we execute it.
- it will open up a browser window and loads the content by keep scrolling for 2 mins. 

![selpge.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1621957005225/L6_xEvFWW.png)

- once it is done with the scrolling it will start downloading all the videos from the links 

![downloadlist.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1621957082758/5_2oj6NRh.png)

- you can check the `video` folder for the downloaded videos which will look something like this.


![dv.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1621957194870/oBCIzo2rl.png)

- finally, it will generate the excel sheet with the list of files and genres as shown below.


![vexcel.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1621957276307/nkxwYOPom.png)

## Bonus points

- your downloaded file count will depend on the number of videos loaded on the webpage so you can increase or decrease the scrolling duration to control the file counts.

- More the duration of scroll more videos it can download and more the time it will take.

- you can download multiple types of videos all you have to do is just add the keywords in the `genres` list in the script.

- scripts allows to opt for downloading the videos if you just want the list then just comment the `download_vimeo` function inside the `extractImages` function.
