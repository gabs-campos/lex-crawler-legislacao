import scrapy
from legislacao.items import LegislacaoItem
import sentence_transformers
from transformers import AutoTokenizer, AutoModel
import re

class LegislacaoMunicipalSpider(scrapy.Spider):
    name = 'legislacao_municipal'
    allowed_domains = ['legislacao.prefeitura.sp.gov.br']
    start_urls = ['https://legislacao.prefeitura.sp.gov.br/busca/pg/1?ano-inicial=2024']
    

    def parse(self, response):
        # Extrair os links para as páginas de detalhes de cada legislação
        links = response.css('div.bx-resultado a::attr(href)').extract()
        for link in links:
            yield response.follow(link, self.parse_full_text)

        # Paginação
        next_page_title = response.xpath('/html/body/section/div/div[2]/div/div[2]/div/div[4]/ul/span[1]/text()').get()
        next_page = int(next_page_title[7:].split("de")[0].strip()) + 1 
        last_page = int(next_page_title[7:].split("de")[1].strip())
        next_url = f"https://legislacao.prefeitura.sp.gov.br/busca/pg/{next_page}?ano-inicial=2024"
        if next_page <= last_page:
            yield response.follow(next_url, self.parse)

    def parse_full_text(self, response):
        # Extrair informações detalhadas de cada página de legislação
        title = response.css("h4::text").get()
        div_law = response.xpath('/html/body/section/div/div[2]/div[2]/div/div[4]')
        text = ' '.join(div_law.css('*::text').extract()).strip()
        details_url = response.xpath("//ul[@class='bx-btn']/li/a/@href").extract_first()
        yield response.follow(details_url, self.parse_details, meta={'title': title, 'text': text})

    def parse_details(self, response):
        # Extrair informações detalhadas de cada página de legislação
        title = response.meta['title']
        text = response.meta['text']
        rows = response.xpath("//table/tbody/tr")
        item = {'title': title, 'text': text}
        for row in rows:
            key = row.xpath('td[@class="nameMeta"]/text()').get().strip()
            value = row.xpath('td[2]//text()').getall()
            item[key] = value
            
            
        yield LegislacaoItem(
            esfera='municipal',
            title=item.get('title', ''),
            numero=self.parse_numero(item.get('Número', '')),
            ano=item.get('Data de publicação', '')[0].split('/')[-1],
            ementa=item.get('Ementa', ''),
            integra=item.get('text', ''),
            url=response.url,
            embedding=self.embedding(item.get('text', ''))
        )


    def embedding(self, doc: str):
        model = sentence_transformers.SentenceTransformer('all-MiniLM-L6-v2')
        vector = model.encode(doc)
        return vector

    def parse_numero(self, numero):
        numero = re.sub(r"\d+\.\d+", numero)
        return numero.group() if numero else None

    