import argparse
from tabulate import tabulate
from termcolor import colored
import os
import json
import requests
from dotenv import dotenv_values
from models.quickassessmodel import QuickAssessModel
from datetime import date

api_url = "https://jackyzhang.pro/assess/quick/"


def getData(excel_file):
    data = QuickAssessModel(
        excels=[excel_file]).dict()
    data = data['facts']
    return_data = {
        "basic": {
            "dob": data['dob'].strftime("%Y-%m-%d"),
            "email": "jacky@gmail.com",
            "phone": "7783215110",
            "lastName": "Zhang",
            "firstName": "Jacky",
            "birthCity": "Nanjing",
            "birthCountry": "China"
        },
        "language": {
            "date": date.today().strftime('%Y-%m-%d'),
            "reading": data['reading'],
            "writting": data['writting'],
            "speaking": data['speaking'],
            "listening": data['listening'],
            "testFormat": data['test_format']
        },
        "education": {
            "level": data['level'],
            "country": data['edu_country'],
            "province": data['edu_province'],
            "institute": "NJU",
            "graduateDate": data['graduate_date'].strftime('%Y-%m-%d')
        },
        "family": [
            {
                "dob": data['relative_dob'].strftime("%Y-%m-%d"),
                "city": "Vancouver",
                "name": "Li",
                "province": data['relative_province'],
                "canadaStatus": data['canada_status'],
                "relationship": data['relationship']
            }
        ],
        "assets": {
            "liquidAssets": data['liquid_assets'],
            "netWorth": data['net_worth']
        },
        "workExperience": {
            "startDate": data['start_date'].strftime('%Y-%m-%d'),
            "endDate": data['end_date'].strftime('%Y-%m-%d'),
            "noc": data['work_noc'],
            "term": data['term'],
            "country": data['work_country'],
            "jobTitle": data['job_title'],
            "province": data['work_province'],
            "sharePercentage": data['share_percentage']
        },
        "adaptation": {
            "noc": data['joboffer_noc'],
            "title": "Hotel Front desk",
            "jobOffer": data['job_offer'],
            "province": data['joboffer_province']
        }
    }
    return return_data


def getSolutions(data):
    config = dotenv_values()
    token = config['TOKEN']
    headers = {
        'Authorization': f"Token {token}",
        'Content-Type': 'application/json'
    }
    response = requests.post(api_url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(
            f' Response status code is {response.status_code}, and there is no feedback')


def showData(solutions,args):
    print(colored('You may be qualified for the Canadian immigration programs as the following\n', 'green'))
    for prog in solutions:
        print(colored("* {program} *".format(**prog), 'green'))
        print(colored("Stream: ","green"),colored("{stream}".format(**prog), 'white'))
        if args.description: print(colored("Description: ","green"),colored("{description}".format(**prog), 'white'))
        if args.remark: print(colored("Remark: ","green"),colored("{remark}".format(**prog), 'white'))


def main():
    parser = argparse.ArgumentParser(
        description="used for processing everything noc related")
    parser.add_argument("-e", "--excel", help="input excel file")
    parser.add_argument(
        "-j", "--json", help="print json data ", action='store_true')
    parser.add_argument(
        "-d", "--description", help="print program description data ", action='store_true')
    parser.add_argument(
        "-r", "--remark", help="print program remark data ", action='store_true')

    args = parser.parse_args()

    if args.excel:
        data = getData(args.excel)
        solutions=getSolutions(data)
        showData(solutions,args)
        if args.json:
            print(json.dumps(data, indent=3))


if __name__ == "__main__":
    main()
