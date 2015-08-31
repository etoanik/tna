# -*- coding: utf-8 -*-

import sys
import argparse
import StringIO
import requests
from lxml import etree

STATION_CODE = ['TPE', 'TSA', 'KHH', 'KIX', 'NRT', 'OKA', 'CTS', 'KHD', 'AKJ']


class Args():
    pass

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--departure', choices=STATION_CODE, default='TPE', help='Departure Station Code')
    parser.add_argument('-a', '--arrival', choices=STATION_CODE, default='KIX', help='Arrival Station Code')
    parser.add_argument('-t', '--date', default='2016/04/01', help='Departure Date (YYYY/MM/DD)')

    args = Args()
    parser.parse_args(namespace=args)

    # request service
    with requests.Session() as session:
        # 首頁
        response = session.post('http://gessl.tna.com.tw', params={'culture': 'zh-hant'})
        # 200
        assert response.status_code == 200

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
        assert response.status_code == 200
        
        # 解析HTML
        parser = etree.HTMLParser(encoding=response.encoding, remove_blank_text=True)
        root = etree.HTML(response.text, parser=parser)
        # result = etree.tostring(root, encoding=sys.stdout.encoding, pretty_print=True, method='html')
        # 查詢有結果
        if root.xpath("//table[@class='select_table table_type1']/tbody//input"):
            pass
        
        
