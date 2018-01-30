# Download the first image from Google Images for a given filename/keyword
# the keyword is taken from the home assistant media player component - its name is stored in 'mpc_name'
# this script is used for displaying media posters in home assistant using a local_file camera component

import os
import argparse
import json
import re
import yaml
import urllib.request
from urllib.request import Request, urlopen

# Downloading entire Web Document (Raw Page Content)
def download_page(url): 
	headers = {}
	headers[
		'User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
	req = urllib.request.Request(url, headers=headers)
	resp = urllib.request.urlopen(req)
	respData = str(resp.read())
	return respData

# Finding 'Next Image' from the given raw page
def get_image(s):
    start_line = s.find('rg_di')
    if start_line == -1:  # If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('"class="rg_meta"')
        start_content = s.find('"ou"', start_line + 1)
        end_content = s.find(',"ow"', start_content + 1)
        content_raw = str(s[start_content + 6:end_content - 1])
        return content_raw

if __name__ == '__main__':
	# Path where the image will be saved - your hass file camera shuold point here
	save_path = '/ram'
	# Name for the downloaded image - your hass file camera shuold look for this file
	file_name = 'movie_data'
	# Password for your hass instance - this is needed to get the filename from the mediaplayer component.
	hass_password = 'your_hass_password'
	# This is the name of the media player we'll track and provide images/posters
	mpc_name = 'mpclivingroom'
	
	# Get file name from home assistant api
	url = 'http://localhost:8123/api/states/media_player.{}?api_password={}'.format(mpc_name, hass_password)
	with urllib.request.urlopen(url) as wurl:
		data = json.loads(wurl.read().decode())
	search_keyword = data['attributes']['media_title']
	
	# Check if there is year in the filename and crop it from there
	match = re.match(r'.*([1-3][0-9]{3})', search_keyword)
	if match is not None:
		search_keyword = match.group(0)

	# Download Image Links
	search_term = search_keyword
	search = search_term.replace(' ', '%20')

	url = 'https://www.google.com/search?q=' + search + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
	raw_html = (download_page(url))

	items = get_image(raw_html)

	req = Request(items, headers={
		"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
	response = urlopen(req, None, 15)
	image_name = file_name
	
	output_file = open(save_path + "/" + image_name + ".jpg", 'wb')
	image_name = image_name + ".jpg"

	data = response.read()
	output_file.write(data)
	response.close()
	print("completed ====> " + image_name)