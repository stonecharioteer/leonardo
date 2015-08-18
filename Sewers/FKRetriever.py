#!usr/bin/
import datetime
import os
import glob
import urllib
import urllib2
from bs4 import BeautifulSoup
from Katana import getETA
from PyQt4 import QtCore

class FKRetriever(QtCore.QThread):
	sendData = QtCore.pyqtSignal(str,list,int,bool)

	def __init__(self,*args,**kwargs):
		super(FKRetriever,self).__init__(*args, **kwargs)
		self.allow_run = False
		self.fsn_list = None
		self.image_location = os.path.join("Images","Parent Images")
		self.data_list = None


	def run(self):
		while True:
			if self.allow_run:
				self.allow_run = False

	def __del__(self):
		pass

	def getFlipkartPageAsSoupFromFSN(self, fsn):
		"""Improve this method at a later stage."""
        url = "http://www.flipkart.com/search?q=" + fsn
        while True:
            try:
                html = urllib2.urlopen(url, timeout=120)
                break
            except urllib2.HTTPError:
                error = "Server response error for %s. Retrying" %fsn
                self.sendException.emit(error)
                continue
            except socket.error:
                error = "Socket error for %s. Retrying" %fsn
                self.sendException.emit(error)
                continue
            except httplib.BadStatusLine:
                error = "Bad status line error for %s. Retrying" %fsn
                self.sendException.emit(error)
                continue

        soup = BeautifulSoup(html)
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
        item_id_prefix_position = upload_link.find(r"/p/")
        if item_id_prefix_position > -1:
            item_id_start_position = item_id_prefix_position + len(r"/p/")
            item_id_length = 16
            item_id_end_position = item_id_start_position + item_id_length
            item_id = upload_link[item_id_start_position: item_id_end_position]
        else:
            item_id = None
        return item_id


	def downloadSpecTable(self, fk_page_soup):
        """Adapted from Swineherd"""
        #find the section in this thing.
        spec_section_area = fk_page_soup.find(class_ = "productSpecs specSection")
        #get model name
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
                            current_string_value = "Error Obtaining String Value"
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
        for column in self.required_data:
            if column in specifications.keys():
                self.return_data_set[self.fsn][column]=specifications[column]
            elif column not in ["WS Name","Brand","Image"]:
                #print self.return_data_set[self.fsn]
                self.return_data_set[self.fsn][column]="NA"
                
	def downloadProductImages(self, fk_page_soup):
		pass
