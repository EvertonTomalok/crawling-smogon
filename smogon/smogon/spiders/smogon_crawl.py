# -*- coding: utf-8 -*-

import scrapy
from selenium import webdriver
import time


class SmogonCrawlSpider(scrapy.Spider):
    name = 'smogon_crawl'
    allowed_domains = ['www.smogon.com']
    start_urls = ['https://www.smogon.com/dex/rs/pokemon/']

    def parse(self, response):

        driver = webdriver.Chrome()
        
        driver.get(response.url)

        # Maximizando a janela
        driver.maximize_window()

        SCROLL_PAUSE_TIME = 0.1

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        hrefs = []
        x = 0
        y = 500

        valor = 500

        driver.execute_script("window.scrollTo(0, 0);")

        while True:
            try:
                for elemento in driver.find_elements_by_xpath('//*[@class="PokemonAltRow-name"]'):
                    h = elemento.find_element_by_xpath('./a').get_attribute('href')
                    if h not in hrefs:
                        hrefs.append(h)
                        print(h)
                        # yield {
                        #     'url': h
                        # }

                if y > last_height:
                    break

                # Scroll down to bottom
                driver.execute_script(f"window.scrollTo({x},{y});")  # 0, document.body.scrollHeight

                x += valor
                y += valor

                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)

                # Calculate new scroll height and compare with last scroll height
                # new_height = driver.execute_script("return document.body.scrollHeight")

            except Exception:
                x -= valor
                y -= valor

        driver.close()

        for href in hrefs:

            yield scrapy.Request(url=href, callback=self.get_info)

    def get_info(self, response):

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options)

        driver.get(response.url)

        pokemon = driver.find_element_by_xpath('//h1[@data-reactid=".0.1.1.1"]').text

        tipo = []
        for t in driver.find_elements_by_xpath('//div[@class="PokemonSummary-types"]/ul/li/a'):
            tipo.append(t.text)

        #habilidades = []
        links_habilidade = []
        for element in driver.find_elements_by_xpath('//ul[@class="AbilityList"]/li/a'):
            #habilidades.append(element.text)
            links_habilidade.append((element.text, element.get_attribute('href')))

        atributos = []

        for t in driver.find_elements_by_xpath('//table[@class="PokemonStats"]/tbody/tr'):
            name = t.find_element_by_xpath('./th').text
            number = t.find_element_by_xpath('./td[1]').text
            atributos.append((name, number))

        evolucoes = []

        for evolucao in driver.find_elements_by_xpath('//ul[@class="PokemonFamily"]/li/div/a/span/span[2]'):
            evolucoes.append(evolucao.text)

        movimentos = list()

        for movimento in driver.find_elements_by_xpath('//div[@class="MoveRow "]'):

            golpe = movimento.find_element_by_xpath('./div[1]/a').text

            tipo = movimento.find_element_by_xpath('./div[2]/a').text

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

            dicionario[golpe]['tipo'] = tipo
            dicionario[golpe]['categoria'] = categoria
            dicionario[golpe]['poder'] = poder
            dicionario[golpe]['acuracia'] = acuracia
            dicionario[golpe]['pp'] = golpes_disponiveis
            dicionario[golpe]['descricao'] = descricao_golpe

            movimentos.append(dicionario)

        driver.close()

        yield {
            'pokemon': pokemon,
            'habilidades': links_habilidade,
            'atributos': atributos,
            'evolucoes': evolucoes,
            'movimentos': movimentos
        }
