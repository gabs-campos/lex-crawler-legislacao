import scrapy


class LegislacaoEstadualSpider(scrapy.Spider):
    name = "legislacao_estadual"
    allowed_domains = ["legislacao.prefeitura.sp.gov.br"]
    start_urls = ["http://www.legislacao.sp.gov.br/legislacao/dg280202.nsf/Leis?OpenView"]

    def parse(self, response):
        pass
