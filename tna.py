# -*- coding: utf-8 -*-

import sys
import argparse
import requests

STATION_CODE = ['TPE', 'KIX']


class Args():
    pass

if __name__ == '__main__':

    args = Args()
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--departure', choices=STATION_CODE, default='TPE', help='Departure Station Code')
    parser.add_argument('-a', '--arrival', choices=STATION_CODE, required=True, help='Arrival Station Code')
    parser.add_argument('-t', '--date', required=True, help='Departure Date (YYYY/MM/DD)')

    parser.parse_args(namespace=args)

    # request service
    with requests.Session() as session:
        # 首頁
        response = session.post('http://gessl.tna.com.tw', params={'culture': 'zh-hant'})
        # 200
        assert  response.status_code == 200

        # 查詢航班
        response = session.post('http://gessl.tna.com.tw/Search/Search', params={
            # 單程
            'SearchFlights[0].Direction': 'OneWay',
            # 起程地
            'SearchFlights[0].DepartureStationCode': args.departure,
            # 抵達地
            'SearchFlights[0].ArrivalStationCode': args.arrival,
            # '出發日期
            'SearchFlights[0].DepartureDate': args.date,
            # 成人
            'PassengerTypes[0].Key': 'Adult',
            # 人數
            'PassengerTypes[0].Value': '1',
            # 兒童
            'PassengerTypes[1].Key': 'Child',
            # 人數
            'PassengerTypes[1].Value': '0',
            # 搭乘艙級
            'CabinType': 'Economy',
            # 折扣序號
            'PromoCode': '',
        })
        # 200
        assert  response.status_code == 200

        # 析HTML
        print response.text

        

