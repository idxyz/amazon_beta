# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from openpyxl import Workbook
from scrapy.exceptions import DropItem


class AmazonBetaPipeline(object):

    def open_spider(self, spider):
        self.r = 2
        self.wb = Workbook()
        self.excelname = 'amazon_part4.xlsx'
        self.ws1 = self.wb.active
        self.ws1.title = 'amazon_review'
        info = ['资料更新时间', 'asin', '星级', '顾客',  '顾客ID', '评论日期', 'isVP', '评论链接','顾客主页', 'facebook', 'twitter', 'pinterest', 'instagram', 'youtube']
        for i in range(1, len(info) + 1):
            r = 1
            c = i
            v = info[i - 1]
            self.ws1.cell(row=r, column=i, value=v)

    def close_spider(self, spider):
        self.wb.save(filename=self.excelname)

    def process_item(self, item, spider):
        if item is not None:
            data = dict(item)
            rr = str(self.r)
            self.ws1['A' + rr] = data['updated_time'][0]
            self.ws1['B' + rr] = data['asin'][0]
            self.ws1['C' + rr] = data['star'][0]
            self.ws1['D' + rr] = data['author'][0]
            self.ws1['E' + rr] = data['customerId'][0]
            self.ws1['F' + rr] = data['pub_date'][0]
            self.ws1['G' + rr] = data['isVP'][0]
            self.ws1['H' + rr] = data['href'][0]
            self.ws1['I' + rr] = data['author_href'][0]
            self.ws1['J' + rr] = data['facebook'][0]
            self.ws1['K' + rr] = data['twitter'][0]
            self.ws1['L' + rr] = data['pinterest'][0]
            self.ws1['M' + rr] = data['instagram'][0]
            self.ws1['N' + rr] = data['youtube'][0]

            self.r = self.r + 1
            return item
        else:
            raise DropItem('Missing data in %s' % item)
