symbols = ['AUD','BRL','BTC','GBP','CAD','EUR','JPY','MXN','NZD','RUB','CHF','NG','CL','XAU','XAG']

cot_futures = {
                  'AUD' : [ 'AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE',
                            'AUSTRALIAN DOLLARS - CHICAGO MERCANTILE EXCHANGE',
                            'AUSTRALIAN DOLLARS - INTERNATIONAL MONETARY MARKET'
                          ],
                  'BRL' : [ 'BRAZILIAN REAL - CHICAGO MERCANTILE EXCHANGE',
                            'BRAZILIAN REAL - INTERNATIONAL MONETARY MARKET'
                          ],
                  'BTC' : [ 'BITCOIN - CHICAGO MERCANTILE EXCHANGE' ],
                  'GBP' : [ 'BRITISH POUND STERLING - CHICAGO MERCANTILE EXCHANGE',
                            'POUND STERLING - CHICAGO MERCANTILE EXCHANGE',
                            'POUND STERLING - INTERNATIONAL MONETARY MARKET'
                          ],
                  'CAD' : [ 'CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE',
                            'CANADIAN DOLLAR - INTERNATIONAL MONETARY MARKET'
                          ],
                  'EUR' : [ 'EURO FX - CHICAGO MERCANTILE EXCHANGE',
                            'EURO FX - INTERNATIONAL MONETARY MARKET'
                          ],
                  'JPY' : [ 'JAPANESE YEN - CHICAGO MERCANTILE EXCHANGE',
                            'JAPANESE YEN - INTERNATIONAL MONETARY MARKET'
                          ],
                  'MXN' : [ 'MEXICAN PESO - CHICAGO MERCANTILE EXCHANGE',
                            'MEXICAN PESO - INTERNATIONAL MONETARY MARKET'
                          ],
                  'NZD' : [ 'NEW ZEALAND DOLLAR - CHICAGO MERCANTILE EXCHANGE',
                            'NEW ZEALAND DOLLARS - INTERNATIONAL MONETARY MARKET'
                          ],
                  'RUB' : [ 'RUSSIAN RUBLE - CHICAGO MERCANTILE EXCHANGE' ],
                  'CHF' : [ 'SWISS FRANC - CHICAGO MERCANTILE EXCHANGE',
                            'SWISS FRANC - INTERNATIONAL MONETARY MARKET'
                          ],
                  'NG'  : [ 'NATURAL GAS - NEW YORK MERCANTILE EXCHANGE' ],
                  'CL'  : [ 'CRUDE OIL, LIGHT SWEET - NEW YORK MERCANTILE EXCHANGE',
                            "CRUDE OIL, LIGHT 'SWEET' - NEW YORK MERCANTILE EXCHANGE"
                          ],
                  'XAU' : [ 'GOLD - COMMODITY EXCHANGE INC.' ],
                  'XAG' : [ 'SILVER - COMMODITY EXCHANGE INC.' ]
                }


cot_futures_list = [  'AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE',
                      'AUSTRALIAN DOLLARS - CHICAGO MERCANTILE EXCHANGE',
                      'AUSTRALIAN DOLLARS - INTERNATIONAL MONETARY MARKET',
                      'BRAZILIAN REAL - CHICAGO MERCANTILE EXCHANGE',
                      'BRAZILIAN REAL - INTERNATIONAL MONETARY MARKET',
                      'BITCOIN - CHICAGO MERCANTILE EXCHANGE',
                      'BRITISH POUND STERLING - CHICAGO MERCANTILE EXCHANGE',
                      'POUND STERLING - CHICAGO MERCANTILE EXCHANGE',
                      'POUND STERLING - INTERNATIONAL MONETARY MARKET',
                      'CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE',
                      'CANADIAN DOLLAR - INTERNATIONAL MONETARY MARKET',
                      'EURO FX - CHICAGO MERCANTILE EXCHANGE',
                      'EURO FX - INTERNATIONAL MONETARY MARKET',
                      'JAPANESE YEN - CHICAGO MERCANTILE EXCHANGE',
                      'JAPANESE YEN - INTERNATIONAL MONETARY MARKET',
                      'MEXICAN PESO - CHICAGO MERCANTILE EXCHANGE',
                      'MEXICAN PESO - INTERNATIONAL MONETARY MARKET',
                      'NEW ZEALAND DOLLAR - CHICAGO MERCANTILE EXCHANGE',
                      'NEW ZEALAND DOLLARS - INTERNATIONAL MONETARY MARKET',
                      'RUSSIAN RUBLE - CHICAGO MERCANTILE EXCHANGE',
                      'SWISS FRANC - CHICAGO MERCANTILE EXCHANGE',
                      'SWISS FRANC - INTERNATIONAL MONETARY MARKET',
                      'NATURAL GAS - NEW YORK MERCANTILE EXCHANGE',
                      'CRUDE OIL, LIGHT SWEET - NEW YORK MERCANTILE EXCHANGE',
                      "CRUDE OIL, LIGHT 'SWEET' - NEW YORK MERCANTILE EXCHANGE",
                      'GOLD - COMMODITY EXCHANGE INC.',
                      'SILVER - COMMODITY EXCHANGE INC.'
                    ]
cot_futures_dict = {  'AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE'         : 'AUD',
                      'AUSTRALIAN DOLLARS - CHICAGO MERCANTILE EXCHANGE'        : 'AUD',
                      'AUSTRALIAN DOLLARS - INTERNATIONAL MONETARY MARKET'      : 'AUD',
                      'BRAZILIAN REAL - CHICAGO MERCANTILE EXCHANGE'            : 'BRL',
                      'BRAZILIAN REAL - INTERNATIONAL MONETARY MARKET'          : 'BRL',
                      'BITCOIN - CHICAGO MERCANTILE EXCHANGE'                   : 'BTC',
                      'BRITISH POUND STERLING - CHICAGO MERCANTILE EXCHANGE'    : 'GBP',
                      'POUND STERLING - CHICAGO MERCANTILE EXCHANGE'            : 'GBP',
                      'POUND STERLING - INTERNATIONAL MONETARY MARKET'          : 'GBP',
                      'CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE'           : 'CAD',
                      'CANADIAN DOLLAR - INTERNATIONAL MONETARY MARKET'         : 'CAD',
                      'EURO FX - CHICAGO MERCANTILE EXCHANGE'                   : 'EUR',
                      'EURO FX - INTERNATIONAL MONETARY MARKET'                 : 'EUR',
                      'JAPANESE YEN - CHICAGO MERCANTILE EXCHANGE'              : 'JPY',
                      'JAPANESE YEN - INTERNATIONAL MONETARY MARKET'            : 'JPY',
                      'MEXICAN PESO - CHICAGO MERCANTILE EXCHANGE'              : 'MXN',
                      'MEXICAN PESO - INTERNATIONAL MONETARY MARKET'            : 'MXN',
                      'NEW ZEALAND DOLLAR - CHICAGO MERCANTILE EXCHANGE'        : 'NZD',
                      'NEW ZEALAND DOLLARS - INTERNATIONAL MONETARY MARKET'     : 'NZD',
                      'RUSSIAN RUBLE - CHICAGO MERCANTILE EXCHANGE'             : 'RUB',
                      'SWISS FRANC - CHICAGO MERCANTILE EXCHANGE'               : 'CHF',
                      'SWISS FRANC - INTERNATIONAL MONETARY MARKET'             : 'CHF',
                      'NATURAL GAS - NEW YORK MERCANTILE EXCHANGE'              : 'NG',
                      'CRUDE OIL, LIGHT SWEET - NEW YORK MERCANTILE EXCHANGE'   : 'CL',
                      "CRUDE OIL, LIGHT 'SWEET' - NEW YORK MERCANTILE EXCHANGE" : 'CL',
                      'GOLD - COMMODITY EXCHANGE INC.'                          : 'XAU',
                      'SILVER - COMMODITY EXCHANGE INC.'                        : 'XAG'
}

oi_desc_symbol = { 
              'Australian Dollar Futures'     : 'AUD',
              'Bitcoin Futures'               : 'BTC',
              'Brazilian Real Futures'        : 'BRL',
              'British Pound Futures'         : 'GBP',
              'Canadian Dollar Futures'       : 'CAD',
              'Euro FX Futures'               : 'EUR',
              'Japanese Yen Futures'          : 'JPY',
              'Mexican Peso Futures'          : 'MXN',
              'New Zealand Dollar Futures'    : 'NZD',
              'Russian Ruble Futures'         : 'RUB',
              'Swiss Franc Futures'           : 'CHF',
              'Crude Oil Futures'             : 'CL',
              'Henry Hub Natural Gas Futures' : 'NG',
              'Gold Futures'                  : 'XAU',
              'Silver Futures'                : 'XAG'
            }

oi_symbol_desc = {
              'AUD' : 'Australian Dollar Futures',
              'BTC' : 'Bitcoin Futures',
              'BRL' : 'Brazilian Real Futures',
              'GBP' : 'British Pound Futures',
              'CAD' : 'Canadian Dollar Futures',
              'EUR' : 'Euro FX Futures',
              'JPY' : 'Japanese Yen Futures',
              'MXN' : 'Mexican Peso Futures',
              'NZD' : 'New Zealand Dollar Futures',
              'RUB' : 'Russian Ruble Futures',
              'CHF' : 'Swiss Franc Futures',
              'CL'  : 'Crude Oil Futures',
              'NG'  : 'Henry Hub Natural Gas Futures',
              'XAU' : 'Gold Futures',
              'XAG' : 'Silver Futures',
}

oi_mapping = {
              'AUD': 'forex',
              'BTC': 'equity',
              'BRL': 'forex',
              'GBP': 'forex',
              'CAD': 'forex',
              'EUR': 'forex',
              'JPY': 'forex',
              'MXN': 'forex',
              'NZD': 'forex',
              'RUB': 'forex',
              'CHF': 'forex',
              'CL': 'energy',
              'NG': 'energy',
              'XAU': 'metals',
              'XAG': 'metals'
            }

oi_report_types = {'equity': 4, 'agricultural': 2, 'energy': 7, 'forex': 3, 'metals': 8}
oi_report_url = 'https://www.cmegroup.com/CmeWS/exp/voiProductsViewExport.ctl?media=xls&tradeDate='
cot_report_url = 'https://www.cftc.gov/files/dea/history/'
###################################################################################################
#### init DB
###################################################################################################

#db_path = 'E:\\Forex\\cme_reports\\test\\trading.db'
#report_path = 'E:\\Forex\\cme_reports\\test'
db_path = 'E:\\Forex\\cme_reports\\trading.db'
report_path = 'E:\\Forex\\cme_reports'

headers = {'User-Agent': 'Mozilla/5.0'}