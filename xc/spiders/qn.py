import scrapy
from xc.items import XcItem

class QnSpider(scrapy.Spider):
    name = 'qn'
    allowed_domains = ['hotel.qunar.com']

    base_url = 'https://hotel.qunar.com/cn/chongqing_city/?fromDate=2024-06-04&toDate=2024-06-05&cityName='

    # 城市列表
    page_list = ['北京', '成都', '广州', '杭州', '昆明', '青岛', '上海', '深圳', '西安', '重庆', '北海',
                 '大理', '大连', '东莞', '佛山', '福州', '贵阳', '桂林', '哈尔滨', '海口', '合肥', '惠州',
                 '济南', '嘉兴', '兰州', '丽江', '南昌', '南京', '南宁', '宁波', '黔东南', '秦皇岛', '泉州',
                 '三亚', '厦门', '沈阳', '石家庄', '苏州', '太原', '天津', '威海', '温州', '乌鲁木齐', '无锡',
                 '武汉', '西宁', '烟台', '长沙', '郑州', '珠海']

    def start_requests(self):
        # 使用列表推导式生成start_urls列表
        self.start_urls = [self.base_url + city for city in self.page_list]
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    '''
    一级界面操作：
        一级爬虫位置：
            hotel_name
            //p[@class="name"]/a/text()
            
            hotel_rating
            //p[@class="comm"]/span[@class="num"]/text()
            
            hotel_com_num
            //p[@class="comm"]/span[@class="total"]/text()
            
            hotel_price
            //p[@class="price_new"]/a/text()
            
        二级爬虫链接：
            level_two_url
            //p[@class="name"]/a/@href
        
    二级界面操作：
        二级爬虫位置
            com_title
            //p[@class="ct-title"]/text()
            
            com_rating
            //p[@class="num"]/text()
            
            com_yes
            //span[@class="like"]/span/text()
            
            com_com
            //a[@class="reply"]/span/text()
            
            com_content
            //p[@class="js_contentAll"]/text()
            
            com_info
            //p[@class="ct-extra"]/span[@class=""]
    '''


    def parse(self, response):
        print('response.encoding',response.encoding)
        print('response.text',response.text)

        '''
            一级界面操作：
        一级爬虫位置：
            hotel_name
            //p[@class="name"]/a/text()

            hotel_rating
            //p[@class="comm"]/span[@class="num"]/text()

            hotel_com_num
            //p[@class="comm"]/span[@class="total"]/text()

            hotel_price
            //p[@class="price_new"]/a/text()

        二级爬虫链接：
            level_two_url
            //p[@class="name"]/a/@href
        '''
        hotel_names = response.xpath('//p[@class="name"]/a/text()').extract()
        hotel_ratings = response.xpath('//p[@class="comm"]/span[@class="num"]/text()').extract()
        hotel_com_nums = response.xpath('//p[@class="comm"]/span[@class="total"]/text()').extract()
        hotel_prices = response.xpath('//p[@class="price_new"]/a/text()').extract()
        level_two_urls = response.xpath('//p[@class="name"]/a/@href').extract()

        # 找到最短的列表长度
        min_length = min(len(hotel_names), len(hotel_ratings), len(hotel_com_nums), len(hotel_prices),
                         len(level_two_urls))
        # print('hotel_names:', hotel_names, '\n')
        # print('hotel_ratings:', hotel_ratings, '\n')
        # print('hotel_com_nums:', hotel_com_nums, '\n')
        # print('hotel_prices:', hotel_prices, '\n')
        # print('level_two_urls:', level_two_urls, '\n')
        # 截断所有列表
        hotel_names = hotel_names[:min_length]
        hotel_ratings = hotel_ratings[:min_length]
        hotel_com_nums = hotel_com_nums[:min_length]
        hotel_prices = hotel_prices[:min_length]
        level_two_urls = level_two_urls[:min_length]

        for hotel_name,hotel_rating,hotel_com_num,hotel_price,level_two_url in zip(hotel_names,hotel_ratings,hotel_com_nums,hotel_prices,level_two_urls):
            meta_data = {
                'hotel_name' : hotel_name,
                'hotel_rating' : hotel_rating,
                'hotel_com_num' : hotel_com_num,
                'hotel_price' : hotel_price
            }
            if level_two_url is not None:
                yield response.follow(level_two_url,self.parse_level_two,meta=meta_data)

    def parse_level_two(self,response):
        '''
        二级界面操作：
            二级爬虫位置
                com_title
                //p[@class="ct-title"]/text()

                com_rating
                //p[@class="num"]/text()

                com_yes
                //span[@class="like"]/span/text()

                com_com
                //a[@class="reply"]/span/text()

                com_content
                //p[@class="js_contentAll"]/text()

                com_info
                //p[@class="ct-extra"]/span[@class=""]
        '''
        com_titles = response.xpath('//p[@class="ct-title"]/text()').extract()
        com_ratings = response.xpath('//p[@class="num"]/text()').extract()
        com_yess = response.xpath('//span[@class="like"]/span/text()').extract()
        com_coms = response.xpath('//a[@class="reply"]/span/text()').extract()
        com_contents = response.xpath('//p[@class="js_contentAll"]/text()').extract()
        com_infos = response.xpath('//p[@class="ct-extra"]/span[@class=""]').extract()

        # 找到最短的列表长度
        min_length = min(
            len(com_titles),
            len(com_ratings),
            len(com_yess),
            len(com_coms),
            len(com_contents),
            len(com_infos)
        )
        print('min_length',min_length)

        # 切片操作截断所有列表到最短长度
        com_titles = com_titles[:min_length]
        com_ratings = com_ratings[:min_length]
        com_yess = com_yess[:min_length]
        com_coms = com_coms[:min_length]
        com_contents = com_contents[:min_length]
        com_infos = com_infos[:min_length]  # 确保com_info也是列表形式

        for com_title,com_rating,com_yes,com_com,com_content,com_info in zip(com_titles,com_ratings,com_yess,com_coms,com_contents,com_infos):

            hotel_name = response.meta.get('hotel_name')
            hotel_rating = response.meta.get('hotel_rating')
            hotel_com_num = response.meta.get('hotel_com_num')
            hotel_price = response.meta.get('hotel_price')
            # 创建XcReviewItem对象并填充字段
            item = XcItem(
                com_title=com_title,
                com_rating=com_rating,
                com_yes=com_yes,
                com_com=com_com,
                com_content=com_content,
                com_info=com_info,
                hotel_name=hotel_name,
                hotel_rating=hotel_rating,
                hotel_com_num=hotel_com_num,
                hotel_price=hotel_price
            )
            yield item







