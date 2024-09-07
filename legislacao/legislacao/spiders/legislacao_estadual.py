import scrapy
from legislacao.items import LegislacaoItem

class LegislacaoEstadualSpider(scrapy.Spider):
    name = "legislacao_estadual"
    allowed_domains = ["legislacao.prefeitura.sp.gov.br"]
    start_urls = [f'http://www.legislacao.sp.gov.br/legislacao/dg280202.nsf/Leis?OpenView&Start=1&Count=1000&Expand={secao}#{secao}' for secao in range(1, 25)]


    def parse(self, response):        
        # Extracting main information from the HTML arquivo
        table_rows = response.css('tr')

        for row in table_rows:
            table_cells = row.css('td')
            # print(table_cells.get())
            if len(table_cells) == 6:
                details_url = table_cells[2].css('font a::attr(href)').get()
                numero = table_cells[2].css('::text').get()
                data = table_cells[3].css('::text').get()
                ementa = table_cells[4].css('::text').get()
                
                retorno = {
                    'numero': numero,
                    'data': data,
                    'ementa': ementa
                }
                
                yield LegislacaoItem(
                    esfera='estadual',
                    numero=retorno['numero'],
                    ano=retorno['data'].split('/')[-1],
                    ementa= retorno['ementa'],
                    integra="",
                    url=response.url
                )
                # yield response.follow(details_url, self.parse_details, meta=retorno)


    def parse_details(self, response):
        # Extracting details from the HTML arquivo
        try:
            law_text_elements = response.xpath('//table[@width="100%"]//font[@size="4"]/text()').extract()
            law_text = ' '.join([element.strip() for element in law_text_elements if element.strip()])
            texto = response.css('body').get()
            final_item =  LegislacaoItem(
                esfera='estadual',
                numero=retorno['numero'],
                ano=retorno['data'].split('/')[-1],
                ementa= retorno['ementa'],
                integra=texto,
                url=response.url
            )
            yield final_item
        except Exception as e:
            print(f"An error occurred while extracting details: {str(e)}")
