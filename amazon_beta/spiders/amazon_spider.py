from datetime import datetime
import re

import scrapy
from scrapy.loader import ItemLoader

from amazon_beta.items import AmazonBetaItem


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ["www.amazon.co.uk"]

    target = ('B078K2N54C',)
    target_urls = [
        "https://www.amazon.co.uk/product-reviews/" + id + "/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&showViewpoints=1&sortBy=recent&pageNumber=1"
        for id in target]

    start_urls = target_urls

    def parse(self, response):
        #  提取数据
        for reviews in response.css('.a-section .review'):
            # 星级
            star = reviews.css(".a-section .celwidget .a-link-normal .a-icon-alt::text").extract_first()[0]
            # 评论作者
            author = reviews.css('span.a-size-base.a-color-secondary.review-byline .author::text').extract_first()
            # 评论作者的个人空间地址
            org_author_href = reviews.css(
                'span.a-size-base.a-color-secondary.review-byline .author::attr(href)').extract_first()
            author_href = 'https://www.amazon.co.uk' + org_author_href
            # 获取customerID
            # customerId = parse_customerId()

            # 评论发布日期
            org_pub_date = reviews.css('span.a-size-base.a-color-secondary.review-date::text').extract_first()
            # ['19', 'March', '2018']
            org_pub_date = re.split('[ ]', org_pub_date)[1:]
            # '19/March/2018'
            pub_date = '{0}/{1}/{2}'.format(*org_pub_date)
            isVP = reviews.css('span.a-size-mini.a-color-state.a-text-bold::text').extract_first()
            if isVP:
                isVP = 'VP'
            else:
                isVP = 'Not VP'
            # 评价链接
            org_href = reviews.css(
                'a.a-size-base.a-link-normal.review-title.a-color-base.a-text-bold::attr(href)').extract_first()
            href = 'https://www.amazon.co.uk' + org_href
            # 获取ASIN
            asin = re.findall("ASIN=(\w+)", org_href, re.S)[0]

            # 是否VP
            # is_VP =
            loader = ItemLoader(item=AmazonBetaItem(), response=response)

            loader.add_value('star', star)
            loader.add_value('author', author)
            loader.add_value('pub_date', pub_date)
            loader.add_value('isVP', isVP)
            loader.add_value('updated_time', str(datetime.now()))
            loader.add_value('href', href)
            loader.add_value('author_href', author_href)
            loader.add_value('asin', asin)
            # 进入下一层获取customerId
            request = scrapy.Request(author_href, meta={'data': loader}, callback=self.parse2)
            # yield loader.load_item()
            yield request

        # 判断是否有下一页

        # 获取下一页链接

        next_page = response.css('#cm_cr-pagination_bar > ul > li.a-last a::attr(href)').extract_first()
        # 判断链接是否有效 有效则传递链接 并做一个递归
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    # 第二层 获取 customeID social network information!
    def parse2(self, response):
        data_page = response.body.decode("utf-8")
        customerId = \
            re.findall("\"locale\":\"en-GB\"\,\"customerId\":\"(\w+)\"\,\"viewName\"", data_page,
                       re.S)[0]

        loader = response.meta['data']
        loader.add_value('customerId', customerId)

        # 获取social 账号 facebook, twitter, pinterest, instagram, youtube
        facebook = re.findall("\"type\"\:\"facebook\"\,\"url\"\:\"(.+?)\"\,\"iconUrl\"", data_page, re.S)
        twitter = re.findall("\"type\"\:\"twitter\"\,\"url\"\:\"(.+?)\"\,\"iconUrl\"", data_page, re.S)
        pinterest = re.findall("\"type\"\:\"pinterest\"\,\"url\"\:\"(.+?)\"\,\"iconUrl\"", data_page, re.S)
        instagram = re.findall("\"type\"\:\"instagram\"\,\"url\"\:\"(.+?)\"\,\"iconUrl\"", data_page, re.S)
        youtube = re.findall("\"type\"\:\"youtube\"\,\"url\"\:\"(.+?)\"\,\"iconUrl\"", data_page, re.S)
        social_account_dict = {
            'facebook': facebook,
            'twitter': twitter,
            'pinterest': pinterest,
            'instagram': instagram,
            'youtube': youtube,
        }
        for key in social_account_dict:
            if social_account_dict[key]:
                loader.add_value(key, social_account_dict[key][0])
            else:
                loader.add_value(key, '用户未填写')

        return loader.load_item()
