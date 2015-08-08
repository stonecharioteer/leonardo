##Leonardo
Leonardo is a tool that'll be used to get images from Flipkart, add appropriate icons as dictated by catalogue requirements, and build a presentable image for customer consumption.
###Functions
The following are a list of functions:
* App-Friendly USP Image Creation
 * Leonardo does this in steps. This is, currently, its main purpose. Later, I'll expand this to do a lot more.
* Bunk Image Downloading
 * I have a plan where I can change this to use the Flipkart API instead of scraping the website for images. Currently, it uses BeautifulSoup4.
* Watermarking
* Removal of background color
----
##Requirements
* Python 2.7
* Pip
* PIL (through Pillow) (For most of the image processing.)
* Numpy (It's used to handle the image array information so that I can find and remove unnecessary color information)
* Pandas (Right now, I'm not doing anything with Pandas, but I hope to replace Numpy with it.)
* BeautifulSoup4 (For scraping and bulk-image downloading.)
* PyQt4.11 (For the UI)
----
##History
I had the idea for Leonardo when tasked with batch processing watermarks. It's part of the OINK Report Management system, but exists separately since it's essence is entirely unique. I'll integrate it into the [OINK](www.github.com\oink) repository later.