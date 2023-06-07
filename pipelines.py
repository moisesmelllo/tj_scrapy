# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy_tjsp.settings import XLSX_PATH
import openpyxl

CAMPOS = ['NUMERO DO PROCESSO', 'CIFRA', 'VALOR', 'PARTE', 'SITUAÇÃO']


class TjspPipeline:
    planilha = None
    sheet = None

    def open_spider(self, item):
        self.planilha = openpyxl.Workbook()
        self.sheet = self.planilha.active
        self.sheet.append(CAMPOS)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        parte = str(adapter.get('PARTE')).replace(':', '').strip() if adapter.get('PARTE') is not None else ''
        self.sheet.append([str(adapter.get('NUMERO DO PROCESSO')).strip(),
                           str(adapter.get('CIFRA')).strip(),
                           str(adapter.get('VALOR')).strip('[]').replace("'", ''),
                           parte,
                           str(adapter.get('SITUAÇÃO')).strip('[]').replace("'", '')])

        return item

    def close_spider(self, spider):
        self.planilha.save(XLSX_PATH)

