# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
import time

class CrawlabilitiesSpider(scrapy.Spider):
    name = 'crawlabilities'
    allowed_domains = ['smogon.com']
    start_urls = ['https://smogon.com/dex/rs/abilities/']

    def parse(self, response):

        driver = webdriver.Chrome()

        driver.get(response.url)

        # Maximizando a janela
        driver.maximize_window()

        SCROLL_PAUSE_TIME = 0.1

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        x = 0
        y = 600

        VALOR_SCROLL = 600

        driver.execute_script("window.scrollTo(0, 0);")

        # lista para evitar captura de dados duplicados
        habilidades = list()

        while True:
            try:
                for habilidade in driver.find_elements_by_xpath('//div[@class="AbilityRow "]'):

                    nome = habilidade.find_element_by_xpath('./div[1]/a').text
                    descricao = habilidade.find_element_by_xpath('./div[2]').text

                    if nome not in habilidades:

                        dicionario = dict()

                        dicionario[nome] = descricao

                        habilidades.append(nome)

                        yield dicionario

                if y > last_height:
                    break

                    # Scroll down to bottom
                driver.execute_script(f"window.scrollTo({x},{y});")  # 0, document.body.scrollHeight

                x += VALOR_SCROLL
                y += VALOR_SCROLL

                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)

            except Exception as err:
                print(type(err), err)
                x -= VALOR_SCROLL
                y -= VALOR_SCROLL

        driver.close()
