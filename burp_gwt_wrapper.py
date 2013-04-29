#!/usr/bin/env python

from gwtparse.GWTParser import GWTParser
from collections import defaultdict
from itertools import izip
from base64 import b64decode
from flask import Flask, render_template, request
from glob import iglob
from lxml import etree
import requests, re

app = Flask(__name__)

@app.route('/')
def list_xmls():
	return render_template('xmllist.html', xmls=iglob('*.xml'))

@app.route('/<filename>.xml/')
def list_methods(filename):
	bx = BurpXml(filename)
	return render_template('methodlist.html', methods=bx.get_methods())

@app.route('/<filename>.xml/form<int:reqnum>.html')
def display_form(filename, reqnum):
	bx = BurpXml(filename)
	return render_template('form.html', params=bx.get_params(reqnum), reqnum=reqnum)

@app.route('/<filename>.xml/submit<int:reqnum>.html', methods=['POST'])
def submit_form(filename, reqnum):
	bx = BurpXml(filename)
	params = [request.form['param{0}'.format(i)] for i in xrange(len(bx.get_params(reqnum)))]
	result = bx.send_request(reqnum, params)
	return render_template('result.html', result=result)

URL_TEXT_XPATH = etree.XPath('url/text()')
class BurpXml(object):
	def __init__(self, filename):
		self.items = etree.parse(filename + '.xml').getroot()
	
	def get_methods(self):
		retval = defaultdict(dict)
		for n, item in enumerate(self.items):
			_, data = item2request(item)
			m = re.search(r'service\.([A-Za-z0-9]+)\|([A-Za-z0-9]+)\|', data)
			retval[m.group(1)][m.group(2)] = n
		return retval

	def get_params(self, reqnum):
		_, data = item2request(self.items[reqnum])
		gp = GWTParser()
		gp.deserialize(data)
		return gp.parameters

	def send_request(self, reqnum, params):
		item = self.items[reqnum]
		headers, data = item2request(item)
		for orig, new in izip(self.get_params(reqnum), params):
			new = new.replace('\\', '\\\\').replace('|', r'\!')
			data = data.replace(orig.values[0], new)
		rows = headers.split('\r\n')
		headers = dict(row.split(': ', 1) for row in rows if
				any(row.lower().startswith(i) for i in ('x-', 'content-type', 'cookie')))
		r = requests.post(URL_TEXT_XPATH(item)[0], data=data, headers=headers, verify=False)
		return r.text

REQ_XPATH = etree.XPath('request')
def item2request(item):
	(req,) = REQ_XPATH(item)
	req_text = b64decode(req.text) if req.attrib.get('base64') == 'true' else req.text
	return req_text.split('\r\n\r\n', 1)

if __name__ == "__main__":
    app.run(debug=True)
