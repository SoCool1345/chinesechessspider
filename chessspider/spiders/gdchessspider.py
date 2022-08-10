import scrapy
from scrapy.selector import Selector
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from scrapy.settings import Settings
from scrapy.http import Request
import sys
from chessspider.items import ChessDataItem



sys.path.append("../..")



class GdChessDataSpider(scrapy.Spider):
    name = "gdchessdataspider"
    # 设置下载延时
    download_delay = 1
    allowed_domains = ["www.zgxqds.com"]

    start_urls = [
        "http://www.zgxqds.com/xqpk_list.asp?page=1&bigclass=&midclass=&smallclass=&namekey=&xq_red=&xq_black=&qishou=&sortStr=&radiobutton=&xq_date="
    ]

    # def parse(self, response):
    #     hxs = Selector(response)
    #     title = hxs.xpath("//title/text()")[0].extract()
    #     iframes = hxs.xpath("//iframe/@name").extract()
    #
    #     is_item = False
    #     for iframe in iframes:
    #         item = self.parse_item(title, iframe)
    #         if len(item["move_list"]) > 0:
    #             is_item = True
    #             item["url"] = response.url
    #             yield item
    #
    #     if not is_item and response.url.find("/chess/HTML/") < 0:
    #         for url in hxs.xpath("//a/@href").extract():
    #             if url.find("chess") >= 0 and url.find(".asp") <= 0:
    #                 print("ok url:", url)
    #                 if url.find("http://game.onegreen.net") >= 0:
    #                     yield Request(url, callback=self.parse)
    #                 else:
    #                     yield Request("http://game.onegreen.net" + url, callback=self.parse)
    #             else:
    #                 print("error url:", url)
    flag = True

    def parse(self, response):
        url = "http://www.zgxqds.com/xqpk_list.asp?page={}&bigclass=&midclass=&smallclass=&namekey=&xq_red=&xq_black=&qishou=&sortStr=&radiobutton=&xq_date="
        if self.flag:
            for i in range(1517):
                print("ok url:", url.format(i))
                yield Request(url.format(i), callback=self.parse)
            self.flag = False


        hxs = Selector(response)
        title = hxs.xpath("//title/text()")[0].extract()
        iframes = hxs.xpath("//iframe/@name").extract()

        is_item = False
        for iframe in iframes:
            item = self.parse_item(title, iframe)
            if len(item["move_list"]) > 0:
                is_item = True
                item["url"] = response.url
                yield item

        if not is_item:
            for url in hxs.xpath("//a/@href").extract():
                if url.find("qiju_info.asp") >= 0:
                    print("ok url:", url)
                    yield Request("http://www.zgxqds.com/" + url, callback=self.parse)
                else:
                    print("error url:", url)




    def get_Data(self, data, pattern):
        result = []
        start_index = 0
        for _ in range(10):
            start = data.find("[{}]".format(pattern), start_index, len(data))

            if start < 0:
                break
            start += len("[{}]".format(pattern))
            end = data.find("[/{}]".format(pattern), start_index, len(data))
            if start < end:
                result.append(data[start:end])
            start_index = end + len("[/{}]".format(pattern))
        if len(result) == 0:
            return ""
        return max(result, key=lambda k: len(result))

    def parse_item(self, title, data):
        item = ChessDataItem()
        item["move_list"] = self.get_Data(data, "DhtmlXQ_movelist")
        item["title"] = self.get_Data(data, "DhtmlXQ_title")
        item["name_black"] = self.get_Data(data, "DhtmlXQ_black")
        item["name_red"] = self.get_Data(data, "DhtmlXQ_red")
        item["desc"] = self.get_Data(data, "DhtmlXQ_event")
        item["result"] = self.get_Data(data, "DhtmlXQ_result")
        item["init"] = self.get_Data(data, "DhtmlXQ_binit")
        if len(item["title"]) == 0:
            item["title"] = title
        return item


if __name__ == '__main__':
    print("*************************** \n\nmain function")
    settings = Settings({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    runner = CrawlerRunner(settings)

    d = runner.crawl(GdChessDataSpider)
    reactor.run()  # the script will block here until the crawling is finished

