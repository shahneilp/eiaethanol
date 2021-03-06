# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 17:47:13 2020

@author: Neil
"""
import os
from datetime import datetime

import pandas as pd
import pytz
from flask import Flask

app = Flask(__name__)


@app.route("/")
def eia():
    timestamp = datetime.now(tz=pytz.timezone('US/Central')).strftime('%m/%d/%Y-%H:%M:%S')

    # Overall Stats
    blendurl = 'https://api.grainstats.com/eia/blended_ethanol.json'
    importurl = 'https://api.grainstats.com/eia/ethanol_imports.json'
    produrl = 'https://api.grainstats.com/eia/ethanol_production.json'
    stocksurl = 'https://api.grainstats.com/eia/ethanol_stocks.json'
    gasurl = 'https://api.grainstats.com/eia/gasoline_demand.json'

    prod = pd.read_json(produrl, orient='index')
    stocks = pd.read_json(stocksurl, orient='index')
    blend = pd.read_json(blendurl, orient='index')
    gas = pd.read_json(gasurl, orient='index')
    imports = pd.read_json(importurl, orient='index')
    survey = prod.loc['survey date'][0]
    last_updated = str(prod.loc['last updated'][0])

    col_names = ['Production', 'Stocks', 'Blend', 'Gasoline', 'Imports']
    df_list = [prod, stocks, blend, gas, imports]
    df = pd.concat(df_list, axis=1)
    df.columns = col_names
    df.drop(['country', 'uom', 'region', 'statistic', 'last_week', 'location', 'last updated'], axis=0, inplace=True)
    df.reindex(['value', 'week_change'])
    df = df.reindex(['value', 'week_change'])
    # Production Granular

    padd1produrl = 'https://api.grainstats.com/eia/ethanol_production_padd_1.json'
    padd2produrl = 'https://api.grainstats.com/eia/ethanol_production_padd_2.json'
    padd3produrl = 'https://api.grainstats.com/eia/ethanol_production_padd_3.json'
    padd4produrl = 'https://api.grainstats.com/eia/ethanol_production_padd_4.json'
    padd5produrl = 'https://api.grainstats.com/eia/ethanol_production_padd_5.json'

    padd1prod = pd.read_json(padd1produrl, orient='index')
    padd2prod = pd.read_json(padd2produrl, orient='index')
    padd3prod = pd.read_json(padd3produrl, orient='index')
    padd4prod = pd.read_json(padd4produrl, orient='index')
    padd5prod = pd.read_json(padd5produrl, orient='index')

    prod_names = ['Total', 'PADD1', 'PADD2', 'PADD3', 'PADD4', 'PADD5']

    df_list = [prod, padd1prod, padd2prod, padd3prod, padd4prod, padd5prod]
    proddf = pd.concat(df_list, axis=1)
    proddf.columns = prod_names
    proddf.drop(['country', 'uom', 'region', 'statistic', 'last_week', 'location', 'last updated'], axis=0,
                inplace=True)
    proddf.reindex(['value', 'week_change'])
    proddf = proddf.reindex(['value', 'week_change'])

    # Stocks

    padd1stocksurl = 'https://api.grainstats.com/eia/ethanol_stocks_padd_1.json'
    padd2stocksurl = 'https://api.grainstats.com/eia/ethanol_stocks_padd_2.json'
    padd3stocksurl = 'https://api.grainstats.com/eia/ethanol_stocks_padd_3.json'
    padd4stocksurl = 'https://api.grainstats.com/eia/ethanol_stocks_padd_4.json'
    padd5stocksurl = 'https://api.grainstats.com/eia/ethanol_stocks_padd_5.json'

    padd1stocks = pd.read_json(padd1stocksurl, orient='index')
    padd2stocks = pd.read_json(padd2stocksurl, orient='index')
    padd3stocks = pd.read_json(padd3stocksurl, orient='index')
    padd4stocks = pd.read_json(padd4stocksurl, orient='index')
    padd5stocks = pd.read_json(padd5stocksurl, orient='index')

    stocks_names = ['Total', 'PADD1', 'PADD2', 'PADD3', 'PADD4', 'PADD5']

    df_list = [stocks, padd1stocks, padd2stocks, padd3stocks, padd4stocks, padd5stocks]
    stocksdf = pd.concat(df_list, axis=1)
    stocksdf.columns = stocks_names
    stocksdf.drop(['country', 'uom', 'region', 'statistic', 'last_week', 'location', 'last updated'], axis=0,
                  inplace=True)
    stocksdf.reindex(['value', 'week_change'])
    stocksdf = stocksdf.reindex(['value', 'week_change'])

    overall = df.transpose().to_html(justify='center')
    production = proddf.transpose().to_html()
    stocks = stocksdf.transpose().to_html()
    style = '<style> table {text-align: center;} table thead th {text-align: center;} </style>'
    title = '<head>' + '<title>' + 'Weekly EIA Ethanol Survey ' '</title> ' + '</head>'
    body = '<h2> EIA Ethanol Breakdown  for week of ' + str(
        survey) + '</h2>' + overall + ' <h2> Production Breakdown </h2> ' \
        + production + '<h2> Stocks Breakdown </h2>' + stocks
    update = '<br>' + 'Last Updated: ' + last_updated + '<br>'
    foot = 'Powered by: <a href="https://twitter.com/GrainStats">GrainStats</a> and Made by: <a ' \
           'href="https://twitter.com/shah_neil">Neil Shah</a> '
    html = title + '<center>' + style + body + update + foot + '<br>' + 'Loaded ' + timestamp + '</center>'
    return html


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
