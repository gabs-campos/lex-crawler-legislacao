import scrapy


class LegislacaoEstadualSpider(scrapy.Spider):
    name = "legislacao_estadual"
    allowed_domains = ["legislacao.prefeitura.sp.gov.br"]
    start_urls = ["https://legislacao.prefeitura.sp.gov.br/busca/pg/1?ano-inicial=2024"]

    def parse(self, response):
        pass
