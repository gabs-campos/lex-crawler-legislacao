import scrapy

class LegislacaoMunicipalSpider(scrapy.Spider):
    name = 'legislacao_municipal'
    allowed_domains = ['legislacao.prefeitura.sp.gov.br']
    start_urls = ['https://legislacao.prefeitura.sp.gov.br/busca/pg/1?ano-inicial=2024']

    def parse(self, response):
        # Extrair os links para as páginas de detalhes de cada legislação
        links = response.css('div.bx-resultado a::attr(href)').extract()
        for link in links:
            yield response.follow(link, self.parse_details)

        # Paginação
        next_page_title = response.xpath('/html/body/section/div/div[2]/div/div[2]/div/div[4]/ul/span[1]/text()').get()
        next_page = int(next_page_title[7:].split("de")[0].strip()) + 1 
        last_page = int(next_page_title[7:].split("de")[1].strip())
        next_url = f"https://legislacao.prefeitura.sp.gov.br/busca/pg/{next_page}?ano-inicial=2024"
        if next_page <= last_page:
            yield response.follow(next_url, self.parse)

    def parse_details(self, response):
        # Extrair informações detalhadas de cada página de legislação
        title = response.css("h4::text").get()
        div_law = response.xpath('/html/body/section/div/div[2]/div[2]/div/div[4]')
        text = ' '.join(div_law.css('*::text').extract()).strip()
        yield {
            'title': title,
            'text': text
        }