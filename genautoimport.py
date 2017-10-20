#!/usr/bin/python

"""
Generate dialer autoimport csv file from leads pulled off of Web Callbacks API
"""

import requests
import csv
import argparse
import datetime

def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', help="API User Name", type=str, default='optimise')
    parser.add_argument('--password', help="API Password", type=str, default='end2endComm')
    parser.add_argument('--host', help="API base", type=str, default='localhost')
    parser.add_argument('--port', help="Optional non-standard port.", type=str, default='80')
    parser.add_argument('--pprg', help="Campaign to pull", type=str, default='ICAP')
    parser.add_argument('--path', help="AutoImport Path", type=str, default="U:\\unicore\\autoimport\\")
    parser.add_argument('--test', help="Test API, do not delete on pull", action='store_true')
    args = parser.parse_args()
    return args.user, args.password, args.host, args.port, args.pprg, args.path, args.test

def auto_dict(pprg, lead):
    """
    AutoImport Field Names and Order:

    `AREA_CODE`,`HOME_PHONE`,`FIRST_NAME`,`LAST_NAME`,`PPRG`,`ADDRESS`,`CITY`,`STATE`,`ZIP`,
    `PROMO_CODE`,`COMPANY`,`CONTACT`,`EMAIL`,`FAX`,`WORK_PHONE`,`TIMETOCALL`,`DATETOCALL`,
    `MAXCALLS`,`END_DATE`,`END_TIME`,`BETWCALLS`,`MISC1`,`MISC2`,`MISC3`,`MISC4`,`MISC5`,`MISC6`,
    `MISC7`,`MISC8`,`MISC9`,`MISC10`,`MISC11`,`MISC12`,`MISC13`,`MISC14`,`MISC15`,`MISC16`

    Returns a DICT with this format.
    """
    fieldnames = ['AREA_CODE','HOME_PHONE','FIRST_NAME','LAST_NAME','PPRG','ADDRESS','CITY','STATE','ZIP',
                'PROMO_CODE','COMPANY','CONTACT','EMAIL','FAX','WORK_PHONE','TIMETOCALL','DATETOCALL',
                'MAXCALLS','END_DATE','END_TIME','BETWCALLS','MISC1','MISC2','MISC3','MISC4','MISC5','MISC6',
                'MISC7','MISC8','MISC9','MISC10','MISC11','MISC12','MISC13','MISC14','MISC15','MISC16']
    new_dict = {}
    for field in fieldnames:
        new_dict[field] = ""

    new_dict["AREA_CODE"] = lead["phone"][:3]
    new_dict["HOME_PHONE"] = "{0}-{1}".format(lead["phone"][3:6], lead["phone"][6:])
    new_dict["EMAIL"] = lead["email"]
    new_dict["ADDRESS"] = lead["street"]
    new_dict["CITY"] = lead["city"]
    new_dict["STATE"] = lead["county"]
    new_dict["ZIP"] = lead["postCode"]
    new_dict["FIRST_NAME"] = lead["firstName"]
    new_dict["LAST_NAME"] = lead["lastName"]
    new_dict["MISC6"] = lead["leadID"]
    new_dict["MISC8"] = lead["dob"]
    new_dict["MISC10"] = lead["gender"]
    new_dict["MISC4"] = lead["received"]
    # new_dict["TIMETOCALL"]
    # new_dict["DATETOCALL"]
    new_dict["MAXCALLS"] = "10"
    # new_dict["END_DATE"]
    # new_dict["END_TIME"]
    new_dict["BETWCALLS"] = "300"
    new_dict["PPRG"] = pprg
    new_dict["PROMO_CODE"] = "{0} - {1}".format(pprg, datetime.datetime.strftime(datetime.datetime.now(), '%d-%m-%Y'))
    return new_dict


def main():
    user, password, host, port, pprg, path, test = arguments()
    leads = []
    datestring = datetime.datetime.strftime(datetime.datetime.now(), '%d-%m-%Y_%H-%M-%S-%f')
    import_file = "{0}-{1}.csv".format(pprg, datestring)
    api_url = "http://{0}:{1}/api/v1.0/webcallbacks/{2}".format(host, port, pprg)
    resp = requests.request("GET", api_url, auth=(user, password))
    if resp.status_code == 200:
        leads = resp.json()
    else:
        exit()
    auto_format = []
    for lead in leads:
        auto_format.append(auto_dict(pprg, lead))
    
    with open(path+import_file, 'w') as csvfile:
        fieldnames = ['AREA_CODE','HOME_PHONE','FIRST_NAME','LAST_NAME','PPRG','ADDRESS','CITY','STATE','ZIP',
                    'PROMO_CODE','COMPANY','CONTACT','EMAIL','FAX','WORK_PHONE','TIMETOCALL','DATETOCALL',
                    'MAXCALLS','END_DATE','END_TIME','BETWCALLS','MISC1','MISC2','MISC3','MISC4','MISC5','MISC6',
                    'MISC7','MISC8','MISC9','MISC10','MISC11','MISC12','MISC13','MISC14','MISC15','MISC16']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)

        writer.writeheader()
        for row in auto_format:
            writer.writerow(row)

    print("Leads successfully written to: {0}{1}".format(path, import_file))
    if not test:
        resp = requests.request("DELETE", api_url, auth=(user, password))


if __name__ == '__main__':
    main()

