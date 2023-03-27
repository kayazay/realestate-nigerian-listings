# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
import psycopg2
from datetime import datetime as dt
from itemadapter import ItemAdapter


class RealestatePipeline:

    def open_spider(self, item):
        QUERY = '''
        CREATE TABLE IF NOT EXISTS nglist (
            ref INTEGER PRIMARY KEY, url VARCHAR(255) NOT NULL, page INT,
            price_ngn INTEGER, period VARCHAR(16), bedroom SMALLINT, bathroom SMALLINT, toilet SMALLINT, parking SMALLINT, area_sqm SMALLINT,
            listdate DATE, listtype VARCHAR(32), details TEXT, address VARCHAR(100),
            marketer VARCHAR(128), contact VARCHAR(11)
        ); --16 columns in total '''
        executor(query=QUERY)
        

    def process_item(self, item, spider):
        values, percents = [], []
        for col in cols():
            if col in item:
                if col in ('ref','page','price_ngn','bedroom','bathroom','toilet','parking','area_sqm'):
                    item[col] = int(item[col])
                elif col in ('listdate'):
                    item[col] = dt.strptime(item[col], r'%d %b %Y').date()
                values.append(item[col])
            else:
                values.append(None) # handling null values
            percents.append('%s')
        QUERY = '''INSERT INTO nglist ({0}) VALUES ({1})
        ON CONFLICT DO NOTHING;
        '''.format(
            ','.join(cols()), ','.join(percents))
        executor(query=QUERY, extra=values)
        return item


# METHODS TO BE USED WITHIN THIS SCRIPT
def executor(query='', extra=''):
    with psycopg2.connect(
        host='localhost',
        port='5432',
        database='realestate',
        user='postgres',
    ) as conn:
        with conn.cursor() as curr:
            if query=='' and extra=='':
                curr.execute('select count(*) from nglist;')
                return curr.fetchone()[0]
            elif extra=='':
                curr.execute(query)
            else:
                curr.execute(query, extra)
        conn.commit()

def cols():
    return ['ref','url','page',
        'price_ngn','period','bedroom','bathroom','toilet','parking','area_sqm',
        'listdate','listtype','details','address',
        'marketer','contact',]

