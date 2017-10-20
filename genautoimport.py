"""
Generate dialer autoimport csv file from leads pulled off of Web Callbacks API
"""

import requests
import csv
import argparse

def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', help="API User Name", type=str, default='optimise')
    parser.add_argument('--pass', help="API Password", type=str, default='end2endComm')
    parser.add_argument('--host', help="API base", type=str, default='localhost')
    parser.add_argument('--port', help="Optional non-standard port.", type=str, default='80')
    parser.add_argument('--pprg', help="Campaign to pull", type=str, default='ICAP')
    parser.add_argument('--path', help="AutoImport Path", type=str, default='U:\unicore\autoimport\')
    parser.add_argument('--test', help="Test API, do not delete on pull", type=bool, default=False)
    args = parser.parse_args()
    return args.user, args.pass, args.host, args.port, args.pprg, args.path, args.test

def main():
    user, pass, host, port, pprg, path, test = arguments()
    api_url = "http://{0}:{1}/api/v1.0/webcallbacks/{2}".format(host, port, pprg)
    leads = requests.request("GET", api_url, auth=(user, pass))
    
    

