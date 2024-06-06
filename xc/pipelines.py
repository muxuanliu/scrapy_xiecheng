# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class XcPipeline:
    def open_spider(self, spider):
        self.fp = open('travel.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        self.fp.write((str(item)))
        return item

    def close_spider(self, spider):
        self.fp.close()


# CREATE TABLE IF NOT EXISTS xc_items (
#     com_title VARCHAR(255),  -- 评论标题
#     com_rating FLOAT,           -- 评论评级
#     com_yes INT,              -- 评论中的"是"的数量
#     com_com INT,               -- 评论数量
#     com_content TEXT,          -- 评论内容
#     com_info VARCHAR(255),    -- 评论的额外信息，如发布日期、地点等
#     hotel_name VARCHAR(255),  -- 酒店名称
#     hotel_rating FLOAT,         -- 酒店评级
#     hotel_com_num VARCHAR(255),        -- 酒店的总评论数量
#     hotel_price DECIMAL(10, 2) -- 酒店价格，假设最多有10位数字，其中2位是小数
# );


import pymysql
from scrapy.exceptions import DropItem

class MysqlPipeline():
    def open_spider(self, spider):
        self.db = pymysql.connect(
            host='localhost',
            user='root',
            password='passwd',  # 请替换为您的密码
            db='travel',  # 替换为您的数据库名称
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor  # 使用字典游标
        )
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        # 检查Item是否包含XcItem类定义的字段
        required_fields = [
            'com_title', 'com_rating', 'com_yes', 'com_com', 'com_content', 'com_info',
            'hotel_name', 'hotel_rating', 'hotel_com_num', 'hotel_price'
        ]
        if all(item.get(field) for field in required_fields):
            data = {
                'com_title': item['com_title'],
                'com_rating': item['com_rating'],
                'com_yes': item['com_yes'],
                'com_com': item['com_com'],
                'com_content': item['com_content'],
                'com_info': item['com_info'],
                'hotel_name': item['hotel_name'],
                'hotel_rating': item['hotel_rating'],
                'hotel_com_num': item['hotel_com_num'],
                'hotel_price': item['hotel_price']
            }
            # 根据字段创建插入语句
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))  # 为每个字段创建一个占位符
            sql = f"INSERT INTO your_table_name ({columns}) VALUES ({placeholders})"  # 替换为你的表名
            try:
                self.cursor.execute(sql, tuple(data.values()))
                self.db.commit()
            except pymysql.MySQLError as e:
                print(f"MySQL Error {e.args[0]}: {e.args[1]}")
                self.db.rollback()
                return DropItem('Database error, item dropped')
            except Exception as ex:
                print(f"An error occurred: {ex}")
                self.db.rollback()
                return DropItem('An unexpected error occurred')
        else:
            return DropItem('Missing fields in XcItem')
        return item