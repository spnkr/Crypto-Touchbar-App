#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2,json,sys

coin_ticker = "{{coin_ticker}}" if "{{coin_ticker}}"[0] != "{" else "BTC"
fiat_ticker = "{{fiat_ticker}}" if "{{fiat_ticker}}"[0] != "{" else "USD"
fiat_symbol = "{{fiat_symbol}}" if "{{fiat_symbol}}"[0] != "{" else  "$"
num_format = "{{format}}" if "{{format}}"[2:8] != "format" else  "{}"
mod_percent = float("{{percent}}") if "{{percent}}"[0] != "{" else float(0)
output_type = "{{output_type}}" if "{{output_type}}"[0] != "{" else  "no"
api_type = "{{apiSelector}}" if "{{apiSelector}}"[0] != "{" else  "live"
extraOptions = "{{{extraOptions}}}" if "{{{extraOptions}}}"[0] != "{" else  "&limit=1&aggregate=1&toTs=1514376000"

try:
    if (api_type == 'live'):

        url = "https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms={}".format(coin_ticker, fiat_ticker)

        data = urllib2.urlopen(url)
        obj=json.load(data)

        raw_current = float(obj["RAW"][coin_ticker][fiat_ticker]["PRICE"])
        raw_opening = float(obj["RAW"][coin_ticker][fiat_ticker]["OPEN24HOUR"])
        raw_high = float(obj["RAW"][coin_ticker][fiat_ticker]["HIGHDAY"])
        raw_low = float(obj["RAW"][coin_ticker][fiat_ticker]["LOWDAY"])
        raw_mktcap = int(obj["RAW"][coin_ticker][fiat_ticker]["MKTCAP"])
        current = num_format.format(raw_current)
        opening = num_format.format(raw_opening)
        high = num_format.format(raw_high)
        low = num_format.format(raw_low)

        if (raw_mktcap > 1000000):
            mktcap = str("{:,}".format(raw_mktcap / 1000000)) + " M"
        else:
            mktcap = "{:,}".format(raw_mktcap)

        if (raw_current > raw_opening):
            trend = "▲"
        else:
            trend = "▼"

        if (output_type is "no"):
            print(fiat_symbol + current)
        elif (output_type is "simple"):
            print(fiat_symbol + current + " " + trend)
        elif (output_type is "mktcap"):
            print(fiat_symbol + current + " (" + fiat_symbol + mktcap + ")")
        elif (output_type is "absolute"):
            print(fiat_symbol + current + " (L: " + fiat_symbol + low + " H: " + fiat_symbol + high + ")")
        elif (output_type is "relative"):
            print(fiat_symbol + current + " (L: -" + fiat_symbol + str(raw_current - raw_low) + " H: +" + fiat_symbol + str(raw_high - raw_current) + ")")
        elif (output_type is "current-percentage"):
            print(fiat_symbol + current + " (" + str(round (((raw_current - raw_opening) / raw_current) * 100)) + "%)")
        elif (output_type is "range-percentage"):
            print(fiat_symbol + current + " (L: -" + str(round (((raw_current - raw_low) / raw_current) * 100)) + "% H: +" + str(round (((raw_high - raw_current) / raw_current) * 100)) + "%)")
        elif (output_type is "user-percentage"):
            print(fiat_symbol + current + " (L: " + fiat_symbol + str(raw_current - (raw_current * mod_percent)) + " H: " + fiat_symbol + str(raw_current + (raw_current * mod_percent)) + ")")

    elif (api_type == 'historical'):
        url = "https://min-api.cryptocompare.com/data/histohour?fsym={}&tsym={}" + extraOptions
        url = url.format(coin_ticker, fiat_ticker)

        data = urllib2.urlopen(url)
        obj=json.load(data)

        raw_high = float(obj["Data"][1]["high"])
        high = num_format.format(raw_high)

        print(fiat_symbol + high)

except urllib2.URLError, e:
    print('Unable to get data from API: %s' % e)
except ValueError, e:
    print('There was an error formatting the output: %s' % e)
# Please submit any issues https://github.com/chrislennon/Crypto-Touchbar-App/issues with the above script