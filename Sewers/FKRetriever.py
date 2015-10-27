#!usr/bin/python
from __future__ import division
import datetime
import os
import glob
import urllib
import urllib2
import httplib
import time
import math
import socket
from bs4 import BeautifulSoup
from Katana import getETA
from PyQt4 import QtCore

class FKRetriever(QtCore.QThread):
    #status, data_set, progress_value, completion_status, eta
    sendData = QtCore.pyqtSignal(str, dict, int, list, bool, datetime.datetime) 
    #error_msg
    sendException = QtCore.pyqtSignal(str)
    sendMessage = QtCore.pyqtSignal(str)
    def __init__(self,repo_path,*args,**kwargs):
        super(FKRetriever,self).__init__(*args, **kwargs)
        self.repo_path = repo_path
        self.allow_run = False
        self.fsn_list = None
        self.image_location = os.path.join(self.repo_path,"Parent Images")
        self.data_list = None
        self.mutex = QtCore.QMutex()
        self.condition = QtCore.QWaitCondition()
        if not self.isRunning():
            self.start(QtCore.QThread.LowPriority)

    def run(self):
        while True:
            if self.allow_run:
                #process_events
                error = "Retrieved %d FSNs."%(len(self.fsn_list))
                self.sendException.emit(error)
                counter = 0
                self.data_list = {}
                total = len(self.fsn_list)
                start_time = datetime.datetime.now()
                completed_fsns = []
                pending_fsns = []
                failed_fsns = []
                for fsn in self.fsn_list:
                    success = False
                    loop_counter = 0
                    error = "Processing %s, %d of %d FSNs, started thread at %s."%(fsn, counter+1, len(self.fsn_list), start_time)
                    self.sendException.emit(error)
                    while not success:
                        loop_counter +=1
                        fk_page_soup, success = self.getFlipkartPageAsSoupFromFSN(fsn, counter+1, len(self.fsn_list), start_time)
                        if not success:
                            error = "Unable to fetch the right page for %s. (Trial %d)"%(fsn,loop_counter)
                            self.sendException.emit(error)
                            time.sleep(5)
                        else:
                            print success
                        if loop_counter >5:
                            error = "Tried fetching the page for %s and failed %d times. Giving up."%(fsn,loop_counter)
                            self.sendException.emit(error)
                            break


                    if success:
                        completed_fsns.append(fsn)
                        pending_fsns = [fsn_ for fsn_ in self.fsn_list if fsn_ not in completed_fsns]
                        error = "Retrieved the page for %s, %d of %d FSNs, started thread at %s."%(fsn, counter+1, len(self.fsn_list), start_time)
                        self.sendException.emit(error)
                        if self.imagesNotAvailable(fsn):
                            self.downloadProductImages(fsn, fk_page_soup)
                        else:
                            error = "Skipping fetching of images for %s since I've already got them."%fsn
                            self.sendException.emit(error)
                        try:
                            spec_table = self.downloadSpecTable(fk_page_soup)
                            self.data_list[fsn] = spec_table
                        except:
                            with open(os.path.join("cache","%s.html"%fsn), "w") as file_handle:
                                file_handle.write(fk_page_soup.prettify())
                            error = "Error retrieving specification table for %s. Dumped Soup to file."% fsn
                            self.sendException.emit(error)
                            self.data_list[fsn] = {}
                        counter += 1
                        status = "Completed %d of %d." % (counter, total)
                        data_set = self.data_list
                        progress_value = int(math.ceil(counter/total*100))
                        progress_list = [completed_fsns, pending_fsns, failed_fsns]
                        completion_status = False
                        eta = getETA(start_time, counter, total)
                        self.sendData.emit(status, data_set, progress_value, progress_list, completion_status, eta)
                    else:
                        failed_fsns.append(fsn)
                        error = "Failed in retrieving the page for %s: %d of %d FSNs, started thread at %s."%(fsn, counter+1, len(self.fsn_list), start_time)
                        self.sendException.emit(error)
                completion_status = True
                progress_value = 100
                data_set = self.data_list
                eta = datetime.datetime.now()
                self.sendData.emit(status, data_set, progress_value, progress_list, completion_status, eta)
                self.allow_run = False

    def __del__(self):
        self.mutex.lock()
        self.condition.wakeOne()
        self.mutex.unlock()
        self.wait()

    def getFlipkartPageAsSoupFromFSN(self, fsn, counter, total, start_time):
        """Improve this method at a later stage."""
        url = "http://www.flipkart.com/search?q=" + fsn
        count = 0
        while True:
            count +=1
            try:
                html = urllib2.urlopen(url, timeout=3)
                error = "Retrieved the html for %s (%d of %d. Started at %s)." %(fsn, counter, total, start_time)
                break
            except urllib2.HTTPError:
                error = "Server response error for %s (%d of %d. Started at %s). Retry #%d" %(fsn, counter, total, start_time, count)
                pass
            except socket.error:
                error = "Socket error for %s (%d of %d. Started at %s). Retry #%d" %(fsn, counter, total, start_time, count)
                pass
            except httplib.BadStatusLine:
                error = "Bad status line error for %s (%d of %d. Started at %s). Retry #%d" %(fsn, counter, total, start_time, count)
                pass
            except httplib.IncompleteRead:
                error = "Incomplete Read error for %s (%d of %d. Started at %s). Retry #%d" %(fsn, counter, total, start_time, count)
                pass
            except Exception, e:
                error = "Encountered [%s] for %s (%d of %d. Started at %s). Retry #%d" %(repr(e), fsn, counter, total, start_time, count)
                pass
            self.sendException.emit(error)
        soup = BeautifulSoup(html, "html.parser")
        #validate the soup.
        try:
            item_id = self.getItemIDFromHTML(html)
            success = True
        except:
            success = False
            pass
        if item_id is None:
            success = False
        return soup, success

    def getItemIDFromHTML(self, html_object):
        """Takes an urllib2 html object, gets the current url from geturl and then extracts the item id."""
        upload_link = html_object.geturl()
        #The item id is a 16 character string found after /p/. Its presence shows that a page has correctly loaded.
        item_id_prefix_position = upload_link.find(r"/p/") 
        if item_id_prefix_position > -1:
            item_id_start_position = item_id_prefix_position + len(r"/p/")
            item_id_length = 16
            item_id_end_position = item_id_start_position + item_id_length
            item_id = upload_link[item_id_start_position: item_id_end_position]
        else:
            item_id = None
        return item_id

    def imagesNotAvailable(self, fsn):
        images_path = self.image_location
        images_list = glob.glob(os.path.join(images_path,"*.jpeg"))
        valid_image_counter = 0
        for image_name in images_list:
            if fsn in os.path.basename(image_name):
                return False
        #Get here only if it doesn't find any image with the fsn as the name.
        return True


    def downloadSpecTable(self, fk_page_soup):
        """Adapted from Swineherd"""
        #find the section in this thing.
        spec_section_area = fk_page_soup.find(class_ = "productSpecs specSection")
        #get model name
        if spec_section_area is None:
            raise Exception("Didn't find a section that has the class 'productSpecs specSection' in the HTML for this FSN.")

        specTables = spec_section_area.find_all(class_ = "specTable")
        groupHeads_list = []
        specsKeys_list = []
        specsValues_list = []
        empty_counter = 0
        specifications = {}
        counter = 1
        last_found_entity = None
        last_found_string_value = None
        current_group_head = None
        for specTable in specTables:
            #Stupid Failkart tables aren't formatted properly. There will be more than one "spectable", 
            #and what's more, each row may or may not have a header cell. I need to circumvent all this
            #or I need to rewrite this for the Console. Eventually, that'll be the best method.

            #step 1: loop through each row.
            spec_table_rows = specTable.find_all("tr")
            #step 2: loop through each of these rows.
            for spec_row in spec_table_rows:
                #step 3: determine what that row has: a groupHead, a specKey or specValue.
                for spec_subrow in spec_row:
                    try:
                        current_class = str(spec_subrow["class"][0])
                        try:
                            current_string_value = str(spec_subrow.string).strip()
                        except:
                            current_string_value = "Error Obtaining String Value From Flipkart Page"
                        if counter >1:
                            if (last_found_entity == "specsKey") and (current_class == "specsValue"):
                                if (len(last_found_string_value) > 0) and (last_found_string_value != ""):
                                    specifications[last_found_string_value] = current_string_value
                                else:
                                    specifications[current_group_head] = current_string_value
                            elif (last_found_string_value == "groupHead") and (current_class == "specsValue"):
                                specifications[last_found_string_value] = current_string_value
                            elif (last_found_string_value == "specsKey") and ((current_class == "groupHead") or (current_class == "specsKey")):
                                specifications[last_found_string_value] = None
                            elif current_class == "groupHead":
                                current_group_head = str(spec_subrow.string).strip()
                        last_found_entity = current_class
                        try:
                            last_found_string_value = str(spec_subrow.string).strip()
                        except:
                            last_found_string_value = "Error Obtaining String Value"
                        counter += 1
                    except TypeError:
                        pass
        return specifications
                
    def downloadProductImages(self, fsn, fk_page_soup):
        "Adapted from OINK.SwineHerd"
        #Assume success happens.
        success = True
        #Get all image urls in a list.
        image_urls = []
        #First, get the current productImage.
        image_tag = fk_page_soup.findAll("img", {"class":"productImage  current"})
        if len(image_tag)==0:
            success = False
            error = "Couldn't find the image tags in the HTML for %s. Skipping it for now."%fsn
            self.sendException.emit(error)
        else:
            image_attributes = image_tag[0].attrs
            try:
                image_url = image_attributes["data-zoomimage"]
            except:
                error = "%s doesn't have zoomed-in image. Extracting original from thumbnail."%fsn
                self.sendException.emit(error)
                image_url = image_attributes["data-src"]
                image_url = image_url.replace("400x400","original")
            image_urls.append(image_url)

            #Next, get the remaining productImages.
            image_tags = fk_page_soup.findAll("img", {"class":"productImage "})
            for image_tag in image_tags:
                image_attributes = image_tag.attrs
                try:
                    image_url = image_attributes["data-zoomimage"]
                except:
                    error = "Product page doesn't have zoomed-in image. Extracting original from thumbnail."
                    self.sendException.emit(error)
                    image_url = image_attributes["data-src"]
                    image_url = image_url.replace("400x400","original")
                image_urls.append(image_url)
            #Prepare save options.
            image_name = fsn #Save images as FSNGOESHERE_1.jpeg
            counter = 0
            delimiter = "_"
            image_extension = ".jpeg"
            current_save_location = self.image_location
            if not(os.path.exists(current_save_location)):
                os.makedirs(current_save_location)
            image_save_name = os.path.join(current_save_location, image_name)
            image_counter = 0
            for image_url in image_urls:
                image_counter += 1
                trial_counter = 0
                while True:
                    try:
                        trial_counter += 1
                        image_save_final_name = image_save_name + delimiter + "%2d"%image_counter + image_extension
                        urllib.urlretrieve(image_url, image_save_final_name)
                        if int(os.stat(image_save_final_name).st_size)>1000:
                            break
                        else:
                            error = "Extracted image is less than 1kb. Retrying again."
                            self.sendException.emit(error)
                            if trial_counter < 10:
                                continue
                            else:
                                error = "No image available, or obtained image is too small."
                                self.sendException.emit(error)
                                success = False
                                break
                    except urllib.ContentTooShortError:
                        error = "Failed retrieving the image. Retrying."
                        self.sendException.emit(error)
                        continue
        return success
