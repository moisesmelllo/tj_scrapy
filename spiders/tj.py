from scrapy.http import FormRequest
import scrapy
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from interface import interface
import PySimpleGUI as sg


class TjspspiderSpider(scrapy.Spider):
    name = "tjspfinalversion"
    allowed_domains = ["esaj.tjsp.jus.br"]

    def start_requests(self):
        start_urls = ['https://esaj.tjsp.jus.br/cpopg/open.do']
        for urls in start_urls:
            yield scrapy.Request(url=urls, callback=self.login)

    def login(self, response):
        yield FormRequest.from_response(response,
                                        formdata={
                                            'cbPesquisa': 'DOCPARTE',
                                            'dadosConsulta.valorConsulta': interface()
                                        },
                                        callback=self.parse
                                        )

    def parse(self, response, **kwargs):
        processos = response.xpath("//div[@class='row unj-ai-c home__lista-de-processos']")

        for processo in processos:
            window.refresh()
            parte_processo = processo.xpath(".//label[@class='unj-label tipoDeParticipacao']/text()").get()
            link_processo = processo.xpath(".//a[@class='linkProcesso']//@href").get()
            link_processo_url = 'https://esaj.tjsp.jus.br' + link_processo
            yield scrapy.Request(link_processo_url, callback=self.parse_processo_page,
                                 meta={'parte_processo': parte_processo})

        next_page = response.xpath("//a[@title='Próxima página']//@href").get()

        if next_page is not None:
            next_page_url = 'https://esaj.tjsp.jus.br' + next_page
            yield response.follow(next_page_url, callback=self.parse)

    def parse_processo_page(self, response, **kwargs):
        parte_processo = response.meta.get('parte_processo', None)
        valor_do_processo = response.xpath(".//div[@id='valorAcaoProcesso']/text()").get()
        valor_do_processo_separado = valor_do_processo.split(' ')
        cifra = valor_do_processo_separado[0]
        apenas_valor = valor_do_processo_separado[9].split()
        yield {
            'NUMERO DO PROCESSO': response.xpath(".//span[@id='numeroProcesso']/text()").get(),
            'CIFRA': cifra,
            'VALOR': apenas_valor,
            'PARTE': parte_processo,
            'SITUAÇÃO': response.xpath(".//span[@class='unj-tag']/text()").getall(),
        }


def run_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl(TjspspiderSpider)
    process.start()


if __name__ == '__main__':
    window = sg.Window('Tela de Consulta', [[sg.Text('Clique em "Consultar" para iniciar a consulta.')],
                                            [sg.Button('Consultar')]])
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Consultar':
            run_spider()
            window.close()
    window.close()
