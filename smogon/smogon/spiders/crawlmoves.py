# -*- coding: utf-8 -*-

import scrapy
import time
from selenium import webdriver


class CrawlmovesSpider(scrapy.Spider):

    name = 'crawlmoves'
    allowed_domains = ['www.smogon.com']
    start_urls = ['https://www.smogon.com/dex/rs/moves/']

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

        while True:
            try:
                for movimento in driver.find_elements_by_xpath('//div[@class="MoveRow "]'):

                    golpe = movimento.find_element_by_xpath('./div[1]/a').text
                    elemento_golpe = movimento.find_element_by_xpath('./div[2]/a').text

                    categoria_extract = movimento.find_element_by_xpath('./div[3]/div').get_attribute('class').split()[
                        1].strip()

                    if categoria_extract == 'Physical':
                        categoria = 'Golpe Físico'
                    elif categoria_extract == 'Special':
                        categoria = 'Golpe Especial'
                    else:
                        categoria = 'Golpe sem dano'

                    poder = movimento.find_element_by_xpath('./div[4]/span').text

                    acuracia = movimento.find_element_by_xpath('./div[5]/span').text

                    golpes_disponiveis = movimento.find_element_by_xpath('./div[6]/span').text

                    descricao_golpe = movimento.find_element_by_xpath('./div[7]').text

                    dicionario = dict()
                    dicionario[golpe] = dict()

                    dicionario[golpe]['elemento'] = elemento_golpe
                    dicionario[golpe]['categoria'] = categoria
                    dicionario[golpe]['poder'] = poder
                    dicionario[golpe]['acuracia'] = acuracia
                    dicionario[golpe]['pp'] = golpes_disponiveis
                    dicionario[golpe]['descricao'] = descricao_golpe

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
