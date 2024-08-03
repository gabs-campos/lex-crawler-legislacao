import psycopg2

from scrapy.exceptions import DropItem
import numpy as np
from psycopg2.extensions import register_adapter, AsIs



class LegislacaoPipeline:
    def __init__(self):
        self.conn = psycopg2.connect(
            database="lex",
            user="postgres",
            password="123456",
            host="localhost",
            port="5432"
        )
     
        self.cur = self.conn.cursor()


    def process_item(self, item, spider):
        sql = f"""
            insert into legislacao 
            (esfera,numero,ano,ementa,integra,url,embedding) 
            values 
            (%s, %s, %s, %s ,%s, %s, %s);
        """

        dados = (item['esfera'],item['numero'],item['ano'],item['ementa'],item['integra'],item['url'],[float(x) for x in item['embedding']])

        try:
            self.cur.execute(sql, dados)
            self.conn.commit()
            return item
        except Exception as e:
            print(f"Erro ao inserir item: {e}")
            raise DropItem("Erro ao adicionar item  de legislacao ao banco de dados.")
        

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()


