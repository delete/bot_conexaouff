# coding: utf-8

import json
import cookielib
import mechanize


class Navegador(object):

    def __init__(self):                

        self.url = None
        self.__username = None
        self.__password = None
        self.__loginFileName = 'auth'

        self.__browser = mechanize.Browser()

        cj = cookielib.LWPCookieJar()
        self.__browser.set_cookiejar(cj)

        self.__browser.set_handle_equiv(True)
        self.__browser.set_handle_gzip(False)
        self.__browser.set_handle_redirect(True)
        self.__browser.set_handle_referer(True)
        self.__browser.set_handle_robots(False)
        self.__browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        self.__browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11;\
                                U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615\
                                Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    def login(self):
        self.__getAuth()
        try:
            self.__browser.select_form(nr=0)
            self.__browser.form['iduff'] = self.__username
            self.__browser.form['senha'] = self.__password

            self.__browser.submit()
        except mechanize.BrowserStateError, e:
            raise e

    def __getAuth(self):
        try:
            with open(self.__loginFileName) as file:
                content = file.read()            
        except IOError, e:
            raise e

        data_json = json.loads(content)
        self.__username = data_json['username']
        self.__password = data_json['password']

    def setLoginFile(self, filename):
        self.__loginFileName = filename

    def setUrl(self, url):
        self.url = url
        self.__browser.open(self.url)

    def getContent(self):        
        try:
            content = self.__browser.response().read()
        except Exception:
            content = None
        return content


    def exit(self):
        self.__browser.clear_history()
        self.__browser.close()