# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XcItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    com_title = scrapy.Field()  # 评论标题
    com_rating = scrapy.Field()  # 评论评级
    com_yes = scrapy.Field()    # 评论中的"是"的数量（可能需要根据实际情况定义）
    com_com = scrapy.Field()    # 评论数量
    com_content = scrapy.Field()  # 评论内容
    com_info = scrapy.Field()   # 评论的额外信息（如发布日期、地点等）
    # 使用meta.get获取的数据
    hotel_name = scrapy.Field()  # 酒店名称
    hotel_rating = scrapy.Field()  # 酒店评级
    hotel_com_num = scrapy.Field()  # 酒店的总评论数量
    hotel_price = scrapy.Field()   # 酒店价格
    pass
