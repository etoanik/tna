# -*- coding: utf-8 -*-
import sys
import argparse
import StringIO
import smtplib
import requests
from email.mime.text import MIMEText
from lxml import etree


class Args():
    pass


if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', dest='arrival', choices=['KIX', 'NRT', 'OKA', 'CTS', 'KHD', 'AKJ'], required=True, help='Arrival Station Code')
    parser.add_argument('-d', dest='date', metavar='YYYY/MM/DD', required=True, help='Departure Date')
    parser.add_argument('-m', dest='mail', metavar='Mail', help='Mail Account')

    args = parser.parse_args(namespace=Args())
    
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
            'SearchFlights[0].DepartureStationCode': 'TPE',
            # 抵達地
            'SearchFlights[0].ArrivalStationCode': args.arrival,
            # 出發日期
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
        # 查詢結果
        if root.xpath("//table[contains(@class,'select_table')]/tbody//input"):
            message = '查詢結果已可購票! 請盡速至官網訂購機票!'
        elif root.xpath("//table[@class='select_table table_type1']/tbody//td[text()='%s']" % u'查無航班請重新選擇'):
            message = '查無航班請重新選擇'
            sys.exit()
        else:
            message = '查詢結果異常!\n\n' + etree.tostring(root, encoding='utf-8', pretty_print=True, method='html')

        # 寄送信件
        if args.mail:
            try:
                # 信件內容
                text = MIMEText(message)
                text['Subject'] = '復興航空早鳥查票程式'
                text['From'] = 'service@tna.com.tw'
                text['To'] = args.mail
                # 登入伺服器
                server = smtplib.SMTP(host='msa.hinet.net')
                server.sendmail('service@tna.com.tw', args.mail, text.as_string())
            finally:
                # 離開
                server.quit()
        else:
            sys.exit()
        
        
