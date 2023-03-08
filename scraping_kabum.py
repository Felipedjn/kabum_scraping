import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import math

#PESQUISA: SEMPRE SEPARAR COM -
pesquisa = 'mesa-gamer'

#URL BUSCA
url = f'https://www.kabum.com.br/busca/{pesquisa}'

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 OPR/89.0.4447.83"}

site = requests.get(url, headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')

#TRAZ A QUANTIDADE DE ITEM PESQUISADO
qtd_itens = soup.find('div', id='listingCount').get_text().strip()
index = qtd_itens.find(' ')
qtd = qtd_itens[:index]

#VERIFICA QUANTAS PAGINAS TEM
ultima_pagina = math.ceil(int(qtd)/ 20)

dic_produtos = {'marca':[], 'preco':[], 'imagem':[]}

for i in range(1, ultima_pagina+1): 
    url_pag = f'https://www.kabum.com.br/busca/{pesquisa}?page_number={i}&page_size=20&facet_filters=&sort=most_searched'
    site = requests.get(url_pag, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    produtos = soup.find_all('div', class_=re.compile('productCard'))

    for produto in produtos:
        marca = produto.find('span', class_=re.compile('nameCard')).get_text().strip()
        preco = produto.find('span', class_=re.compile('priceCard')).get_text().strip()
        imagem = str(produto.find('img', class_=re.compile('imageCard')))
        imagemsrc = []
        imagemsrc = re.findall('([https]{5}[:]{1}[//]{2}[a-z0-9._/-]+)', imagem, flags=re.I)
        
        print(marca, preco, imagemsrc)

        dic_produtos['marca'].append(marca)
        dic_produtos['preco'].append(preco)
        dic_produtos['imagem'].append(imagemsrc[0])

    print(url_pag)

df = pd.DataFrame(dic_produtos)
df.to_csv(f'{pesquisa}.csv', encoding='utf-16', sep=';')
