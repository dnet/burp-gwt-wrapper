Burp Suite GWT wrapper
======================

Usage
-----

 - Install dependencies listed below.
 - Start the service by entering `python burp_gwt_wrapper.py` in a terminal.
 - Save the request(s) you'd like to scan in Burp Suite to XML files in the same directory as `burp_gwt_wrapper.py`.
 - Open http://localhost:5000/ in a browser.
 - Select the XML file and the request you'd like to scan.
 - Use your favorite tool (intuition, Burp Suite Scanner, sqlmap, etc.) to scan the service.

Dependencies
------------

 - Python 2.5+ (tested on Python 2.7.3)
 - `gwtparse` from https://github.com/GDSSecurity/GWT-Penetration-Testing-Toolset
 - Flask (Debian/Ubuntu package: `python-flask`)
 - Requests (Debian/Ubuntu package: `python-requests`)
 - LXML (Debian/Ubuntu package: `python-lxml`)

License
-------

The whole project is available under MIT license.

Known limitations
-----------------

 - GWT RPC protocol support depends on `gwtparse`, so version 6 works, but for everything else YMMV
