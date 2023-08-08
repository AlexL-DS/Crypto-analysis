import requests
import pandas as pd
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
def on_button_click():
    exchange1 = exchange1_var.get()
    exchange2 = exchange2_var.get()
    if exchange1 == "Binance" and exchange2 == "Exmo" or exchange1 == "Exmo" and exchange2 == "Binance":
        def on_button_click():
            coin_name = coin_var1.get()
            time_interval1 = coin_var2.get()
            binance_market = coin_name
            tick_interval = time_interval1
            binance_url = 'https://api.binance.com/api/v3/klines?symbol=' + binance_market + '&interval=' + tick_interval
            binance_data = requests.get(binance_url).json()
            binance_df = pd.DataFrame(binance_data)
            binance_df.columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time',
                                  'Quote asset volume',
                                  'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume',
                                  'Ignore']
            binance_df['time'] = pd.to_datetime(binance_df['Open time'], unit='ms')
            number1 = binance_df['Open time'].iat[-1]
            number2 = binance_df['Open time'].iat[0]
            print(777)
            print(binance_df)
            binance_df = binance_df[['Open', 'Close', 'High', 'Low', 'Volume', 'time']]
            binance_df['Open'] = pd.to_numeric(binance_df['Open'], errors='coerce')
            binance_df['High'] = pd.to_numeric(binance_df['High'], errors='coerce')
            binance_df['Low'] = pd.to_numeric(binance_df['Low'], errors='coerce')
            binance_df['Close'] = pd.to_numeric(binance_df['Close'], errors='coerce')
            binance_df['Volume'] = pd.to_numeric(binance_df['Volume'], errors='coerce')
            print(number1)
            print(number2)
            unix_time1 = number1 // 1000
            unix_time2 = number2 // 1000
            print(unix_time1)
            print(unix_time2)
            coin_name = coin_name.replace("USDT", "_USDT")
            coin_name = "_".join(coin_name.split(" "))
            print(coin_name)
            tick_interval2 = {"5m":"5","30m": "30", "1h": "60","2h": "120","4h": "240","1d": "D", "1w": "W","1M": "M"}[tick_interval]
            # 5, 15, 30, 45, 60, 120, 180, 240, D, W, M
            print(tick_interval2)
            exmo_url = f'https://api.exmo.com/v1.1/candles_history?symbol={coin_name}&resolution={tick_interval2}&from={unix_time2}&to={unix_time1}'
            exmo_data = requests.get(exmo_url).json()
            print(exmo_data)
            df = pd.DataFrame(exmo_data)
            print(df)
            df = pd.DataFrame.from_dict(exmo_data['candles'])
            df['time'] = pd.to_datetime(df['t'], unit='ms')
            df['Open'] = pd.to_numeric(df['o'], errors='coerce')
            df['High'] = pd.to_numeric(df['h'], errors='coerce')
            df['Low'] = pd.to_numeric(df['l'], errors='coerce')
            df['Close'] = pd.to_numeric(df['c'], errors='coerce')
            df['Volume'] = pd.to_numeric(df['v'], errors='coerce')
            df = df[['Open', 'Close', 'High', 'Low', 'Volume', 'time']]
            print(df)
            diff = df['Close'] - binance_df['Close']
            print(diff)
            result = (diff / df['Close']) * 100
            print(result)
            df1 = pd.DataFrame(result)
            print(df1)
            df2 = pd.concat([df['time'], df1['Close']], axis=1)
            print(df2)
            print(df.iloc[-1]['Close'])
            print(binance_df.iloc[-1]['Close'])
            spr = (df2.iloc[-1]['Close'])
            spr1 = round(spr,9)
            print(spr1)
            ax = df2.plot(x='time', y='Close')
            plt.title('спред')
            plt.grid(True)
            plt.show()
            # style = mpf.make_mpf_style(base_mpf_style='nightclouds', gridcolor='red')
            plt.plot(df['time'], df['Close'], color='blue', label='exmo')
            plt.plot(binance_df['time'], binance_df['Close'], color='red', label='binance')
            plt.title('графики цены')
            plt.xlabel('дата')
            plt.ylabel('цена')
            plt.legend()
            plt.grid(True)
            plt.show()
            resultat = spr1
            text.insert(tk.END, "spred % :" + str(resultat) + "\n")
            resultat1 = df.iloc[-1]['Close']
            text.insert(tk.END, "exmo:" + str(resultat1) + "\n")
            resultat2 = binance_df.iloc[-1]['Close']
            text.insert(tk.END, "binance:" + str(resultat2) + "\n")
        def search_coin(*args):
            print("Searching for", coin_var1.get())
        root = tk.Tk()
        root.geometry("300x700+50+260")
        label1 = tk.Label(root, text="select coin name:")
        label1.pack()

        coin_var1 = tk.StringVar(root)
        coin_var1.set("BTCUSDT")
        coin_options1 = ["BTCUSDT", "ETHUSDT", "GMTUSDT", "ALGOUSDT", "BCHUSDT", "ADAUSDT", "DASHUSDT", "DOTUSDT",
                         "ETCUSDT", "NEARUSDT", "SHIBUSDT", "XRPUSDT", "UNIUSDT", "YFIUSDT", "DOGEUSDT", "SUIUSDT",
                         "FLOKIUSDT", "LINKUSDT"]
        option_menu1 = tk.OptionMenu(root, coin_var1, *coin_options1)
        option_menu1.pack()
        coin_var1.trace("w", search_coin)
        label2 = tk.Label(root, text="select interval")
        label2.pack()
        coin_var2 = tk.StringVar(root)
        coin_var2.set("1d")
        coin_options2 = ["5m", "30m", "1h", "2h", "4h","1d", "1w", "1M"]
        option_menu2 = tk.OptionMenu(root, coin_var2, *coin_options2)
        # entry1.pack()
        option_menu2.pack()
        button = tk.Button(root, text="START", command=on_button_click)
        button.pack()
        text = tk.Text(root)
        text.pack()
    elif exchange1 == "Binance" and exchange2 == "Bitget" or exchange1 == "Bitget" and exchange2 == "Binance":
        def on_button_click():
            coin_name = coin_var1.get()
            time_interval1 = coin_var2.get()
            binance_market = coin_name
            tick_interval = time_interval1
            binance_url = 'https://api.binance.com/api/v3/klines?symbol=' + binance_market + '&interval=' + tick_interval
            binance_data = requests.get(binance_url).json()
            binance_df = pd.DataFrame(binance_data)
            binance_df.columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time',
                                  'Quote asset volume',
                                  'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume',
                                  'Ignore']
            binance_df['time'] = pd.to_datetime(binance_df['Open time'], unit='ms')
            number1 = binance_df['Open time'].iat[-1]
            number2 = binance_df['Open time'].iat[299]
            print(777)
            print(binance_df)
            binance_df = binance_df[['Open', 'Close', 'High', 'Low', 'Volume', 'time']]
            binance_df['Open'] = pd.to_numeric(binance_df['Open'], errors='coerce')
            binance_df['High'] = pd.to_numeric(binance_df['High'], errors='coerce')
            binance_df['Low'] = pd.to_numeric(binance_df['Low'], errors='coerce')
            binance_df['Close'] = pd.to_numeric(binance_df['Close'], errors='coerce')
            binance_df['Volume'] = pd.to_numeric(binance_df['Volume'], errors='coerce')
            print(number1)
            print(number2)
            unix_time1 = number1 // 1000
            unix_time2 = number2 // 1000
            print(unix_time1)
            print(unix_time2)
            print(coin_name)
            print(binance_df)
            coin_name = coin_name + "_SPBL"
            tick_interval2 = {"5m":"5min","30m":"30min", "1h":"1h","4h":"4h","6h":"6h","12h":"12h","1d":"1day", "1w":"1week","1M":"1M"}[tick_interval]
            # 5, 15, 30, 45, 60, 120, 180, 240, D, W, M
            print(tick_interval2)
            bitget_url =f"https://api.bitget.com/api/spot/v1/market/candles?symbol={coin_name}&period={tick_interval2}&after={number2}&endTime={number1}&limit=200"

            bitget_data = requests.get(bitget_url).json()
            print(bitget_data)
            bitget_df = pd.DataFrame(bitget_data)
            print(bitget_df)
            bitget_df = pd.DataFrame.from_dict(bitget_data['data'])
            bitget_df['ts'] = pd.to_numeric(bitget_df['ts'])
            bitget_df['time'] = pd.to_datetime(bitget_df['ts'], unit='ms')

            bitget_df['Open'] = pd.to_numeric(bitget_df['open'], errors='coerce')
            bitget_df['High'] = pd.to_numeric(bitget_df['high'], errors='coerce')
            bitget_df['Low'] = pd.to_numeric(bitget_df['low'], errors='coerce')
            bitget_df['Close'] = pd.to_numeric(bitget_df['close'], errors='coerce')
            bitget_df['Volume'] = pd.to_numeric(bitget_df['usdtVol'], errors='coerce')
            bitget_df = bitget_df[['Open', 'Close', 'High', 'Low', 'Volume', 'time']]
            print(bitget_df)
            bitget_last_rows = bitget_df['Open'].iloc[-200:]
            binance_last_rows = binance_df['Open'].iloc[-200:]
            binance_last_rows = binance_last_rows.reset_index(drop=True)
            bitget_last_rows = bitget_last_rows.reset_index(drop=True)
            print(binance_last_rows)
            print(9999999999999999999999999999999999999999999)
            print(bitget_last_rows)
            diff = bitget_last_rows - binance_last_rows
            #diff = bitget_df['Close'] - binance_df['Close']
            print(diff)
            result = (diff / bitget_df['Open']) * 100
            print(result)
            df1 = pd.DataFrame(result)
            print(df1)
            df2 = pd.concat([bitget_df['time'], df1['Open']], axis=1)
            print(df2)
            print(bitget_df.iloc[-1]['Open'])
            print(binance_df.iloc[-1]['Open'])
            spr = (df2.iloc[-1]['Open'])
            spr1 = round(spr,9)
            print(spr1)
            ax = df2.plot(x='time', y='Open')
            plt.title('спред')
            plt.grid(True)
            plt.show()
            # style = mpf.make_mpf_style(base_mpf_style='nightclouds', gridcolor='red')
            plt.plot(bitget_df['time'], bitget_df['Open'], color='blue', label='bitget')
            plt.plot(binance_df['time'], binance_df['Open'], color='red', label='binance')
            plt.title('графики цены')
            plt.xlabel('дата')
            plt.ylabel('цена')
            plt.legend()
            plt.grid(True)
            plt.show()
            resultat = spr1
            text.insert(tk.END, "spred % :" + str(resultat) + "\n")
            resultat1 = bitget_df.iloc[-1]['Open']
            text.insert(tk.END, "bitget:" + str(resultat1) + "\n")
            resultat2 = binance_df.iloc[-1]['Open']
            text.insert(tk.END, "binance:" + str(resultat2) + "\n")
        def search_coin(*args):
            print("Searching for", coin_var1.get())
        root = tk.Tk()
        root.geometry("300x700+50+260")
        label1 = tk.Label(root, text="select coin name:")
        label1.pack()

        coin_var1 = tk.StringVar(root)
        coin_var1.set("BTCUSDT")
        coin_options1 = ["NKNUSDT", "LOOMBTC", "GEMUSDT", "JUPETH", "LTC3LUSDT", "OASUSDT", "NEOBTC", "KNCUSDT", "LYMUSDT", "NIMETH", "SUTERBTC", "ID3SUSDT", "NULSBTC", "HAIUSDT", "MITXUSDT", "PDEXUSDT", "HTRBTC", "FLAMEUSDT", "EPXUSDT", "PUNDIXBTC", "AOGUSDT", "VETBTC", "ATOM3LUSDT", "TWTBTC", "AGLDUSDT", "KAIETH", "YLDUSDT", "CPCETH", "COTIBTC", "POWRUSDT", "CWSUSDT", "PEELBTC", "SENSOUSDT", "ALBTUSDT", "PIKAUSDT", "ALICEUSDT", "VOLTUSDT", "GOUSDT", "UNICUSDT", "SYSBTC", "IHCUSDT", "PNTBTC", "BULLUSDT", "INJUPUSDT", "STXDOWNUSDT", "BOSONETH", "ROOBEEBTC", "SWASHUSDT", "XECUSDT", "BCHUSDC", "ATOM3SUSDT", "CHSBBTC", "LINAUSDT", "ETCUSDT", "RUNEUSDT", "MPLXUSDT", "TRACBTC", "HYDRAUSDT", "ASTRUSDT", "WBTCETH", "CSIXETH", "BCHUSDT", "JARUSDT", "TONEUSDT", "POSIUSDT", "XDBBTC", "EOS3LUSDT", "HYVEBTC", "RUNEUSDC", "ETCUSDC", "KAVAUSDT", "GLQUSDT", "BDXBTC", "ETHDAI", "VSYSUSDT", "TKOBTC", "REQBTC", "PIVXBTC", "RNDRDOWNUSDT", "GASUSDT", "APTUSDT", "TRXUSDT", "CELOUSDT", "MOOVUSDT", "ENJBTC", "NEOKCS", "VETKCS", "SANDUSDT", "FIDAUSDT", "HIFRIENDSUSDT", "KLAYUSDT", "TUSDT", "SUNUSDT", "PUSHBTC", "PERPBTC", "DATAUSDT", "STOREETH", "ID3LUSDT", "ELFETH", "NGLBTC", "KLAYBTC", "POWRBTC", "CTCBTC", "LABSUSDT", "ETCETH", "XMRETH", "BONDUSDT", "LTC3SUSDT", "DPETUSDT", "TARAUSDT", "DEROUSDT", "SCRTBTC", "EFXUSDT", "LDOUSDT", "RLCBTC", "MATICBTC", "ALICEETH", "WOMUSDT", "NUMUSDT", "NMRUSDT", "LDOUSDC", "TONUSDT", "CFXETH", "WAXBTC", "DOGEUSDC", "CWARUSDT", "ICPUPUSDT", "AAVEUSDT", "EWTKCS", "HIODUSDT", "AAVE3SUSDT", "HIGAZERSUSDT", "CREDIUSDT", "BTC3LUSDT", "TRBUSDT", "ELAUSDT", "DOGEUSDT", "TLMBTC", "ITAMCUBEUSDT", "ZEEUSDT", "UOSBTC", "COMPUPUSDT", "USDTPAX", "SOULETH", "LINAUPUSDT", "BICOUSDT", "PREUSDT", "KCSETH", "XDCBTC", "SCLPBTC", "ENSUSDT", "TOWERBTC", "DATABTC", "DGBETH", "CTIUSDT", "LPTUSDT", "MMMUSDT", "TURBOSUSDT", "CHZBTC", "XEMBTC", "TELBTC", "EPSBTC", "PMONUSDT", "XNLUSDT", "SPELLUSDT", "ETHTUSD", "CTSIBTC", "EOS3SUSDT", "SYNRUSDT", "TLOSUSDT", "USDDUSDC", "INJDOWNUSDT", "ALGOETH", "NAVIUSDT", "KAGIUSDT", "ARBUSDT", "JAMETH", "WHALEUSDT", "VEMPUSDC", "USDDUSDT", "POLKBTC", "MONIUSDT", "ETH3SUSDT", "WESTBTC", "NEOUSDT", "SDUSDT", "MMUSDT", "EWTBTC", "BTC3SUSDT", "BNTUSDT", "MANAETH", "EOSUSDC", "ALGOUPUSDT", "DCRBTC", "LMRBTC", "INFRAUSDT", "CHZUSDT", "XCNUSDC", "SXPDOWNUSDT", "TOMOBTC", "OXTBTC", "USDCUSDT", "DOTUSDT", "PSLUSDT", "AZEROUSDT", "RFOXUSDT", "BNBKCS", "RFDUSDT", "APLUSDT", "UNI3LUSDT", "GAFIUSDT", "USDTGBP", "EOSUSDT", "DOTUSDC", "MNSTUSDT", "UOSUSDT", "GMXUSDT", "KINGUSDT", "XCNUSDT", "NOIABTC", "KSMBTC", "XRPTUSD", "GHXUSDT", "FTGUSDT", "ETNBTC", "POLSUSDT", "HISAND33USDT", "IOSTUSDT", "TVKUSDT", "AMBUSDT", "CCDUSDT", "ETH3LUSDT", "BTCUSDC", "OUSDUSDT", "GMEEUSDT", "DOT3SUSDT", "CFX2SUSDT", "ELABTC", "HTRUSDT", "CFGUSDT", "UBXUSDT", "ERTHAUSDT", "FEARUSDT", "NGLUSDT", "CSIXUSDT", "ICXETH", "BTCUSDT", "RNDRBTC", "AAVE3LUSDT", "BNTBTC", "PLUUSDT", "MKRDAI", "SUSHI3SUSDT", "OCEANUSDT", "CETUSUSDT", "GMBUSDT", "LAYERBTC", "ARB3SUSDT", "CGGUSDT", "AVAXBTC", "BCDETH", "P00LSUSDC", "JARBTC", "SRKUSDT", "AMBETH", "REDUSDT", "HIVALHALLAUSDT", "EFXBTC", "TRBBTC", "AIPADUSDT", "APEUSDT", "ERGUSDT", "ZBCUSDT", "SDLUSDT", "DAGBTC", "REVVUSDT", "RLTMUSDT", "GSTUSDT", "LOOKSUSDT", "AGIX2LUSDT", "APEUSDC", "ATOMBTC", "SNXBTC", "ADAUSDC", "PROMUSDT", "ANTBTC", "GAMMAUSDT", "ARKERUSDT", "IDUSDT", "EGOUSDT", "UDOOETH", "GHSTUSDT", "BNBBTC", "FTMETH", "HTUSDT", "COVETH", "HAPIUSDT", "PROMBTC", "P00LSUSDT", "ADAUSDT", "DIAUSDT", "CXOETH", "HIBAKCUSDT", "LOKIBTC", "HNTUSDT", "ALPHAUSDT", "ZCXBTC", "DPRUSDT", "HIODBSUSDT", "AERGOUSDT", "SUIAUSDT", "USDTUSDC", "CFXUSDT", "DOT3LUSDT", "SRMUSDT", "UTKBTC", "BOLTUSDT", "TFUELBTC", "ERNUSDT", "PEPEUSDT", "KAVAUPUSDT", "XSRUSDT", "KMDUSDT", "RBPUSDT", "AERGOBTC", "HORDUSDT", "ATOMKCS", "CAPPBTC", "EOSCUSDT", "SUSHI3LUSDT", "CSBTC", "DEXEETH", "OLTETH", "VLXBTC", "COMPDOWNUSDT", "BUYUSDT", "CQTUSDT", "ISPUSDT", "ALGODOWNUSDT", "UQCETH", "NRGETH", "MJTKCS", "KRLUSDT", "AGIXBTC", "TOMOUSDT", "RPCUSDT", "ARPAUPUSDT", "MAKIUSDT", "ARXUSDT", "CLVUSDT", "ZILUPUSDT", "MAPUSDT", "BTTUSDT", "PUSHUSDT", "ZECUSDT", "URUSUSDT", "IOTXETH", "SYLOUSDT", "XTAGUSDT", "SPAUSDT", "BAKEETH", "ICXUSDT", "FXSBTC", "TIMEBTC", "AGIXUSDT", "LSKETH", "SOLVEUSDT", "UBXETH", "VIDTUSDT", "CFX2LUSDT", "JASMYUSDT", "IOSTBTC", "WINUSDT", "BNSBTC", "SXPUSDT", "LBRUSDT", "VIDUSDT", "FORESTPLUSUSDT", "ERNBTC", "JASMYUSDC", "ARB3LUSDT", "SKUBTC", "TELUSDT", "ADAKCS", "ARRRUSDT", "KAVADOWNUSDT", "LYMETH", "AGIXETH", "JASMY3SUSDT", "HEARTUSDT", "HMNDUSDT", "NXRAUSDT", "AXS3SUSDT", "CLUBUSDT", "FCONUSDT", "NYMUSDT", "GMT3SUSDT", "ORAIUSDT", "GOALUSDT", "STCUSDT", "EPKUSDT", "HIFIDENZAUSDT", "LTOUSDT", "ONEBTC", "ICPBTC", "MJTUSDT", "USDTEUR", "TKYBTC", "APE3LUSDT", "ACOINUSDT", "RPLUSDT", "IDEAUSDT", "RENUSDT", "BLURUSDT", "ANCUSDT", "LUNCUSDT", "XRP3SUSDT", "CARDUSDT", "IOTABTC", "LOKIETH", "PLATOUSDT", "BCHBTC", "VEEDBTC", "SHILLUSDT", "SOULUSDT", "HBARBTC", "LUNCUSDC", "DAGUSDT", "FTMBTC", "SAND3SUSDT", "STGUSDT", "OPCTETH", "XMRUSDT", "TOKOUSDT", "EVERUSDT", "ADABTC", "POLCUSDT", "ZENUSDT", "ACTUSDT", "FTMUSDC", "VAIUSDT", "SFPBTC", "PEPE2USDT", "FTMUSDT", "WRXBTC", "PEPEUPUSDT", "ZCXUSDT", "AXS3LUSDT", "AKROUSDT", "XWGUSDT", "BTCDOWNUSDT", "CKBUSDT", "ONTBTC", "BAKEBTC", "TARAETH", "MAGICUSDT", "BURPUSDT", "SDAOETH", "BCHSVBTC", "AIONBTC", "ETCUPUSDT", "H2OUSDT", "OCEANETH", "COVUSDT", "CSPETH", "MTLUSDT", "NEAR3LUSDT", "GASBTC", "EGLDBTC", "MNETUSDT", "NXRAETH", "NRGBTC", "KNCBTC", "DYDXUSDT", "SKEYUSDT", "IGUUSDT", "XCVUSDT", "SYNUSDT", "1EARTHUSDT", "BTCEUR", "XPRBTC", "PHNXBTC", "SOL3SUSDT", "SUPERBTC", "AUSDUSDT", "GOETH", "CXOBTC", "DASHBTC", "IOTXBTC", "GRTKCS", "MKRBTC", "KLVBTC", "HIRENGAUSDT", "MAKIBTC", "EOSKCS", "XRP3LUSDT", "OVRUSDT", "REQUSDT", "BAXETH", "CFGBTC", "SUKUUSDT", "DAOUSDT", "WESTUSDT", "CIX100USDT", "CARRUSDT", "BNTETH", "BOSONUSDT", "SXPBTC", "ZILBTC", "AMPUSDT", "BEATUSDT", "GODSUSDT", "XPRUSDT", "APT2LUSDT", "ETHBTC", "TRIASBTC", "USDDTRX", "LOKIUSDT", "QIBTC", "NEAR3SUSDT", "OTKUSDT", "KATBTC", "DASHKCS", "AGIX2SUSDT", "EPSUSDT", "JAMUSDT", "ORBSUSDT", "LSKBTC", "FETBTC", "GMBETH", "BCHSVKCS", "FXSUSDT", "XRDUSDT", "RLCUSDT", "BADGERBTC", "UNFIUSDT", "CIRUSUSDT", "FTTUSDT", "FITFIUSDT", "DENTBTC", "HAKAUSDT", "HIFIUSDT", "YFDAIUSDT", "EOSBTC", "ZRXBTC", "ATOMUSDC", "MATIC3LUSDT", "APT2SUSDT", "FORESTPLUSBTC", "FXBTC", "LUNCDOWNUSDT", "ETHBRL", "WNXMBTC", "FKXUSDT", "SAND3LUSDT", "XCURBTC", "KARUSDT", "OMBTC", "ARRRBTC", "UQCBTC", "XEDUSDT", "BCHSVUSDT", "SOL3LUSDT", "BCHKCS", "SNXUSDT", "DOGEBTC", "PUMLXUSDT", "STXUPUSDT", "CANDYUSDT", "QRDOETH", "TVKBTC", "AIOZUSDT", "PBXUSDT", "CVBTC", "TLOSBTC", "INJUSDT", "BCHSVUSDC", "TIDALUSDT", "FITFIUSDC", "USDPUSDT", "LPOOLUSDT", "NHCTUSDT", "ATOMUSDT", "MANAUSDT", "DPXUSDT", "BRWLUSDT", "ACQUSDT", "BETAUSDT", "ALTUSDT", "MHCBTC", "CUDOSBTC", "FTM3LUSDT", "RNDRUPUSDT", "LTCETH", "KOLETH", "TRXBTC", "XLMBTC", "DGTXETH", "XLMKCS", "WNCGBTC", "AUDIOUSDT", "DOTBTC", "VEGAUSDT", "ORDIUSDT", "TRXKCS", "GRT2LUSDT", "DOGEKCS", "KSMUSDT", "MTLBTC", "LTOBTC", "SUSDETH", "ETHUSDT", "STORJUSDT", "OPCTUSDT", "HIDOODLESUSDT", "XMRBTC", "HIENS4USDT", "CHRBTC", "EFIUSDT", "GALAXUSDT", "ZPAYUSDT", "OBIUSDT", "SNTVTETH", "AVABTC", "BLOKUSDT", "MTVETH", "BURGERUSDT", "QKCBTC", "PEOPLEUSDT", "CWEBUSDT", "ICPDOWNUSDT", "BALUSDT", "SKUUSDT", "BUXUSDT", "FLOWUSDT", "GALAX3SUSDT", "MASKDOWNUSDT", "AMPLETH", "WMTUSDT", "SPAETH", "SUPERUSDT", "IMXUSDT", "OLEUSDT", "CREAMUSDT", "MYRIAUSDT", "ADA3LUSDT", "LINK3SUSDT", "MATIC3SUSDT", "PHNXUSDT", "COMBOUSDT", "DARBTC", "GARIUSDT", "ACQUSDC", "TCPUSDT", "TONEETH", "PNTUSDT", "WANETH", "RPCETH", "ROARUSDT", "DSLAUSDT", "SLCLUSDT", "VRAUSDT", "WAXUSDT", "KEYBTC", "STRKBTC", "DEXEUSDT", "SHRUSDT", "LINADOWNUSDT", "WINBTC", "LINK3LUSDT", "ALPHABTC", "GMT3LUSDT", "JASMY3LUSDT", "VRAUSDC", "CEEKUSDT", "LINABTC", "XCHUSDT", "SDAOUSDT", "SCLPUSDT", "HIMAYCUSDT", "AIUSDT", "FORTUSDT", "WBTCBTC", "CMPUSDT", "REQETH", "FRMUSDT", "LMRUSDT", "HISQUIGGLEUSDT", "ETHOUSDT", "NTVRKUSDT", "AURYUSDT", "GOVIBTC", "HIBEANZUSDT", "BTCDAI", "NFTTRX", "AURAUSDT", "HAWKUSDT", "AKTUSDT", "HALOUSDT", "TXAUSDT", "CPOOLUSDT", "PPTETH", "1INCHUSDT", "ALEPHUSDT", "PERPUSDT", "HFTUSDC", "NTVRKUSDC", "DOCKETH", "TXAUSDC", "CGPTUSDT", "ADA3SUSDT", "MNWUSDT", "ANTUSDT", "LUNAUPUSDT", "HICOOLCATSUSDT", "MTSUSDT", "ABBCUSDT", "ADXUSDT", "MFTUSDT", "SNTBTC", "ETHUSDC", "CASBTC", "CAKEUSDT", "KDABTC", "XETAUSDT", "NWCUSDT", "DARUSDT", "CVCBTC", "AURORAUSDT", "GALUSDT", "REPETH", "ONEUSDT", "SFUNDUSDT", "AVAXUSDC", "FTM3SUSDT", "GRT2SUSDT", "AOABTC", "DFIBTC", "SONUSDT", "STEPWATCHUSDT", "NRFBBTC", "PZPUSDT", "DATXETH", "XYOETH", "AVAXUSDT", "MASKUSDT", "LRCBTC", "PIXUSDT", "FORMUSDT", "MVUSDT", "GLMRUSDT", "NEOETH", "VRUSDT", "POKTUSDT", "DOTKCS", "DOGE3LUSDT", "STXUSDT", "XPRTUSDT", "SXPUPUSDT", "OOEUSDT", "SHAUSDT", "DYDXDOWNUSDT", "BCDBTC", "GLCHUSDT", "GEEQUSDT", "NIFUSDT", "LUNAUSDC", "OLTBTC", "MBLUSDT", "FILDOWNUSDT", "H3RO3SUSDT", "LINKBTC", "CBCBTC", "QRDOUSDT", "KASUSDT", "XAVAUSDT", "XYMUSDT", "LUNAUSDT", "CFXBTC", "XNOUSDT", "ENQBTC", "COOHAUSDT", "MLSUSDT", "DIABTC", "MHCUSDT", "MANA3SUSDT", "ATOMETH", "DOGE3SUSDT", "CVXUSDT", "PREBTC", "WLKNUSDT", "IOSTETH", "SOLVEBTC", "EQZUSDT", "CSPRETH", "IOTAUSDT", "STRKETH", "AMPLBTC", "XRPUSDC", "CROBTC", "MXWUSDT", "XDEFIUSDT", "TRVLBTC", "POWRETH", "DFIUSDT", "HFTUSDT", "CSPRUSDT", "LUNCUPUSDT", "PUNDIXUSDT", "ELONUSDT", "IXSUSDT", "DCRETH", "AXSUSDT", "XRPETH", "KARATEUSDT", "SUSDUSDT", "ELFBTC", "LQTYUSDT", "VELOUSDT", "ADSBTC", "MLKBTC", "FCLETH", "CBCUSDT", "KMAUSDT", "MANABTC", "DEROBTC", "SHABTC", "TITANUSDT", "SRBPUSDT", "OPULUSDT", "SENSOBTC", "CSETH", "POLSBTC", "VET3LUSDT", "FRONTUSDT", "CASUSDT", "CELRUSDT", "KONOUSDT", "LINKKCS", "SRKBTC", "IZIUSDT", "LITBTC", "NORDBTC", "MTVUSDT", "CROUSDT", "DAGETH", "HARDUSDT", "WOMBATUSDT", "MANUSDT", "USDTTUSD", "SOLUSDT", "API3USDT", "PHAETH", "SHIBDOGE", "ECOXUSDT", "YFIUSDT", "SWFTCUSDT", "MARSHUSDT", "VET3SUSDT", "PIVXETH", "RBTCBTC", "SYSUSDT", "FETUSDT", "MITXBTC", "XLMETH", "KOLUSDT", "PLYUSDT", "BTCUPUSDT", "TIMEETH", "DATXBTC", "COVBTC", "AKROBTC", "ALBTETH", "UMBUSDT", "MATICUSDT", "SWEATUSDT", "AAVEKCS", "LTXUSDT", "SOLUSDC", "ARPADOWNUSDT", "SWFTCUSDC", "MTRGUSDT", "BDXUSDT", "STORJETH", "PAXGUSDT", "SDNETH", "TRUBTC", "LACEETH", "SINUSDT", "MATICUSDC", "DPIUSDT", "XRPUSDT", "ETCDOWNUSDT", "GRAILUSDT", "HIMEEBITSUSDT", "BNBUSDT", "PRQUSDT", "NIMBTC", "TRADEBTC", "ALPINEUSDT", "CAREUSDT", "NIMUSDT", "DYPUSDT", "BOAUSDT", "MAHAUSDT", "BNBUSDC", "HIGHETH", "GALAX3LUSDT", "DOSEUSDC", "CRVUSDT", "GLMRBTC", "LAIUSDT", "DSLABTC", "LOCUSDT", "NOIAUSDT", "BEPROBTC", "AMBBTC", "EGLDUSDT", "LSSUSDT", "DFAUSDT", "HIENS3USDT", "DINOUSDT", "KINUSDT", "VLXUSDT", "PBRUSDT", "DEXEBTC", "STNDETH", "VETETH", "MANA3LUSDT", "ERSDLUSDT", "XYMBTC", "SOULBTC", "SWPUSDT", "GENSUSDT", "TLMETH", "MINAUSDT", "BALETH", "TOKOKCS", "ARBTC", "GRTUSDT", "PHAUSDT", "UNBUSDT", "SKLUSDT", "DFYNUSDT", "BURGERBTC", "IDEXUSDT", "RMRKUSDT", "VERSEUSDT", "BRISEUSDT", "LABSETH", "OGVUSDT", "TELETH", "FSNUSDT", "WNCGUSDT", "VSYSBTC", "LOKAUSDT", "ETHUPUSDT", "TRADEUSDT", "RACEFIUSDT", "KCSBTC", "BCHSVETH", "LTCUSDC", "SUI3SUSDT", "RDNTUSDT", "KATUSDT", "ENJETH", "AVAUSDT", "COTIUSDT", "KNCETH", "UNOBTC", "GGGUSDT", "WSIENNAUSDT", "WOOUSDT", "RACAUSDT", "LOOMETH", "CKBBTC", "HEGICBTC", "EULUSDT", "BUSDUSDT", "ALICEBTC", "REV3LUSDT", "GNSUSDT", "XCADUSDT", "ACHUSDT", "VETUSDT", "ILVUSDT", "LBPUSDT", "ODDZUSDT", "BNB3SUSDT", "CHMBUSDT", "BUSDUSDC", "HICLONEXUSDT", "TFUELUSDT", "METISUSDT", "TKOUSDT", "DUSKUSDT", "LMWRUSDT", "OLTUSDT", "TRUUSDT", "TKYETH", "BAXBTC", "CAPPETH", "BNCUSDT", "PIPUSDT", "KAIBTC", "WAVESBTC", "POLXUSDT", "MKRUPUSDT", "PIVXUSDT", "HNTBTC", "LADYSUSDT", "PAXGBTC", "SHIBUSDT", "HIMFERSUSDT", "NOMUSDT", "ILAUSDT", "FLOKIDOWNUSDT", "ZILDOWNUSDT", "LPOOLBTC", "DGBBTC", "VRABTC", "AVAX3SUSDT", "HIAZUKIUSDT", "ONSTONUSDT", "XDBUSDT", "SUI3LUSDT", "UNIUSDT", "ETHDOWNUSDT", "ALGOKCS", "FXETH", "FILUPUSDT", "FTUSDT", "DEGOETH", "FLOKIUPUSDT", "SNXETH", "ACAUSDT", "MBOXUSDT", "PYRBTC", "FLUXBTC", "SWINGBYUSDT", "REPUSDT", "ALGOBTC", "QUICKBTC", "SHIBUSDC", "WOOPUSDT", "STRONGUSDT", "ARPAUSDT", "CRPTETH", "CWARBTC", "OMGETH", "FALCONSUSDT", "SDNUSDT", "THETAUSDT", "LITHETH", "HBARUSDT", "ETNUSDT", "STARLYUSDT", "KDONUSDT", "IGUBTC", "XENUSDT", "TOMOETH", "NFTBUSDT", "LOCUSUSDT", "OGNBTC", "CPCBTC", "GTCUSDT", "XTMUSDT", "CELOBTC", "SUSHIUSDT", "TOKOBTC", "LINKUSDC", "SQUADUSDT", "LTCUSDT", "OXTETH", "NULSETH", "ANKRBTC", "CULTUSDT", "FRONTBTC", "SCRTUSDT", "TIMEUSDT", "TLMUSDT", "XCURUSDT", "CARRBTC", "BANDBTC", "USDTDAI", "VEEDUSDT", "LINKUSDT", "ABBCBTC", "AFKUSDT", "ETNETH", "KDAUSDC", "ASTRAUSDT", "PLDUSDT", "ETHGBP", "VEGAETH", "NMRBTC", "WEMIXUSDT", "AFKUSDC", "NDAUUSDT", "XCNBTC", "APE3SUSDT", "KDAUSDT", "IRONUSDT", "KICKSUSDT", "PONDBTC", "ROSEUSDT", "FLRUSDC", "ARNMUSDT", "AVAETH", "PEELUSDT", "HEARTBTC", "TKYUSDT", "PENDLEUSDT", "PPTBTC", "RIFBTC", "XTZUSDT", "MIRUSDT", "UFOUSDT", "EXRDUSDT", "ACEUSDT", "NKNBTC", "BTCBRL", "TRVLUSDT", "BLUR2LUSDT", "COMBUSDT", "NEERUSDT", "XYOBTC", "WANBTC", "BTCTUSD", "OP2SUSDT", "HBBUSDT", "DCUSDT", "WOODOWNUSDT", "RVNUSDT", "STCBTC", "BCH3LUSDT", "OPUSDT", "LTXBTC", "MOVRETH", "FTTBTC", "VXVUSDT", "SOLRUSDT", "IOIUSDT", "GTCBTC", "FORMETH", "ETHWUSDT", "SUIUSDT", "SHIB2SUSDT", "PONDUSDT", "ICPUSDT", "WAXLUSDT", "CVETH", "LACEUSDT", "OPUSDC", "TRACUSDT", "ETHEUR", "TENETUSDT", "CEURBTC", "BNSUSDT", "MAHABTC", "DGTXBTC", "FETETH", "UTKETH", "NORDUSDT", "DGUSDT", "BNB3LUSDT", "BAXUSDT", "LOCGUSDT", "QIUSDT", "XYOUSDT", "SOVUSDT", "OMNUSDT", "BADGERUSDT", "REVVBTC", "MFTBTC", "DORAUSDT", "GOBTC", "AVAX3LUSDT", "XVSUSDT", "SPIUSDT", "LTCBTC", "GHSTBTC", "DGBUSDT", "LRCUSDT", "VOXELETH", "QTUMBTC", "MSWAPBTC", "REEFUSDT", "ANKRUSDT", "PELUSDT", "USDTBRL", "CLHUSDT", "SUSDBTC", "DAPPXUSDT", "OUSDBTC", "DYPETH", "FLYUSDT", "PLAYBTC", "ROUTEUSDT", "BOBAUSDT", "OP2LUSDT", "BAKEUSDT", "MAPBTC", "ORNUSDT", "HIPUNKSUSDT", "FLOWBTC", "SLIMUSDT", "POLKUSDT", "HIUNDEADUSDT", "OPCTBTC", "WRXUSDT", "CTSIUSDT", "HAIBTC", "MSWAPUSDT", "RUNEBTC", "EGAMEUSDT", "BLZUSDT", "FILUSDT", "BCH3SUSDT", "C98USDT", "PRIMALUSDC", "NGCUSDT", "RSRUSDT", "UNI3SUSDT", "OOKIUSDT", "TRXETH", "GOVIUSDT", "MLNBTC", "OCEANBTC", "CSPBTC", "CEURUSDT", "RBSUSDT", "SWINGBYBTC", "PRIMALUSDT", "WILDUSDT", "CUDOSUSDT", "NAKAUSDT", "MXCUSDT", "NFTUSDT", "VCOREUSDT", "JUPUSDT", "ONTUSDT", "EGAMEBTC", "TONEBTC", "OOKIBTC", "DERCUSDT", "BOBUSDT", "INJBTC", "ELAETH", "UMAUSDT", "FORTHUSDT", "MOVRUSDT", "RUSDT", "KEYETH", "DVPNUSDT", "REVUUSDT", "ARUSDT", "XNOBTC", "USTCUSDT", "WELLUSDT", "AUDIOBTC", "SIDUSUSDT", "CTCUSDT", "ONTETH", "UNIKCS", "BALBTC", "BEPROUSDT", "HISEALSUSDT", "USTCUSDC", "OMGBTC", "DREAMSUSDT", "DYDXUPUSDT", "BANDUSDT", "VOXELUSDT", "GLQBTC", "ERGBTC", "ATAUSDT", "XLMUSDT", "NRFBUSDT", "XEDBTC", "YGGUSDT", "BONDLYUSDT", "GPTUSDT", "DOCKBTC", "CRPTBTC", "POLUSDT", "FLRUSDT", "KOKUSDT", "SNTVTBTC", "LAVAXUSDT", "EQXUSDT", "DEGOUSDT", "SHIB2LUSDT", "MLNUSDT", "USDJUSDT", "BATUSDT", "STNDUSDT", "TOMIUSDT", "SUKUBTC", "CTSIDOWNUSDT", "EDUUSDT", "SFPUSDT", "XTZKCS", "STMXUSDT", "CREAMBTC", "EOSETH", "SOSUSDT", "BMONUSDT", "KLVTRX", "SHRBTC", "MASKUPUSDT", "REPBTC", "DENTETH", "TRACETH", "NWCBTC", "UNOUSDT", "NEARBTC", "ENQUSDT", "SLPUSDT", "EQXBTC", "REEFBTC", "LRCETH", "MARS4USDT", "XEMUSDT", "ATABTC", "ZECBTC", "KAIUSDT", "BUYBTC", "IOTXUSDT", "YFDAIBTC", "OXTUSDT", "SSVUSDT", "PSTAKEUSDT", "USDNUSDT", "OMUSDT", "GMMUSDT", "GLMBTC", "SUIPUSDT", "RFUELUSDT", "ASDUSDT", "PEPEDOWNUSDT", "HIGHUSDT", "ACSUSDT", "WINTRX", "PDEXBTC", "KCSUSDT", "SKLBTC", "LITUSDT", "BSWUSDT", "GMTUSDT", "BTCGBP", "ETHPAX", "OSMOUSDT", "GFTUSDT", "XTZBTC", "TOWERUSDT", "SIMPUSDT", "DASHETH", "ZILUSDC", "EWTUSDT", "UBXTUSDT", "ZECKCS", "KCSUSDC", "ETHOBTC", "ADSUSDT", "BIFIUSDT", "ALGOUSDC", "SUTERUSDT", "OMGUSDT", "COCOSUSDT", "SRMBTC", "FRAUSDT", "HIFLUFUSDT", "ZILUSDT", "MATTERUSDT", "TTUSDT", "XDCUSDT", "COMPUSDT", "BBCUSDT", "HOTCROSSUSDT", "ETH2ETH", "PYRUSDT", "AMPLUSDT", "ALGOUSDT", "WAVESUSDT", "ZILETH", "WOOUPUSDT", "RSRBTC", "XDCETH", "GMTUSDC", "PLGRUSDT", "MELOSUSDT", "SNTETH", "ETCBTC", "XPLLUSDT", "MKRETH", "RANKERUSDT", "AAVEBTC", "DASHUSDT", "EPIKUSDT", "BABYDOGEUSDT", "CRPTUSDT", "HEGICUSDT", "LIKEUSDT", "VISIONUSDT", "HEROUSDT", "HIBAYCUSDT", "SRBSUSDT", "ENJUSDT", "BOLTBTC", "ZRXETH", "DODOUSDT", "GLMUSDT", "BLUR2SUSDT", "QKCETH", "KRLBTC", "SDLBTC", "TRIASUSDT", "DIVIUSDT", "MIRKCS", "TRIBLUSDT", "HIBIRDSUSDT", "STXBTC", "WALUSDT", "MANBTC", "CTIETH", "HYVEUSDT", "MTVBTC", "MKRDOWNUSDT", "BUXBTC", "STORJBTC", "TRXUSDC", "LTCKCS", "QUARTZUSDT", "QUICKUSDT", "JSTUSDT", "RLYUSDT", "LUNADOWNUSDT", "ORCUSDT", "CHSBETH", "KMDBTC", "FCLUSDT", "AOAUSDT", "NEARUSDC", "DORABTC", "TAUMUSDT", "ACABTC", "AIONETH", "MCUSDT", "OGNUSDT", "QNTUSDT", "GFTBTC", "NEARUSDT", "HIPENGUINSUSDT", "BONDLYETH", "BFCUSDT", "WNXMUSDT", "CTSIUPUSDT", "XRPKCS", "FLOKIUSDC", "MAVUSDT", "REAPUSDT", "LYMBTC", "CHRUSDT", "KLVUSDT", "TWTUSDT", "ASTRBTC", "MHCETH", "LAYERUSDT", "MKRUSDT", "ORBSBTC", "STOREUSDT", "LITHUSDT", "FLOKIUSDT", "ALPACAUSDT", "FLUXUSDT", "CEREUSDT", "UPOUSDT", "KP3RUSDT", "SURVUSDT", "2CRZUSDT", "VIDBTC", "WAXETH", "RNDRUSDT", "MBOXBTC", "XRPBTC", "FRRUSDT", "STRAXUSDT", "XVSBTC", "DMTRUSDT", "GMBBTC", "TSUGTUSDT", "TRIBEUSDT", "MLKUSDT"
]
        option_menu1 = tk.OptionMenu(root, coin_var1, *coin_options1)
        option_menu1.pack()
        coin_var1.trace("w", search_coin)
        label2 = tk.Label(root, text="select interval")
        label2.pack()
        coin_var2 = tk.StringVar(root)
        coin_var2.set("1d")
        coin_options2 = ["5m", "30m", "1h", "2h", "4h","12h","1d", "1w", "1M"]
        option_menu2 = tk.OptionMenu(root, coin_var2, *coin_options2)
        # entry1.pack()
        option_menu2.pack()
        button = tk.Button(root, text="START", command=on_button_click)
        button.pack()
        text = tk.Text(root)
        text.pack()
    elif exchange1 == "Binance" and exchange2 == "Kucoin" or exchange1 == "Kucoin" and exchange2 == "Binance" :
        def on_button_click():
            coin_name1 = coin_var1.get()
            time_interval1 = coin_var2.get()
            #time_interval2 = coin_var3.get()
            coin_name2 = coin_var4.get()
            binance_market = coin_name1
            tick_interval = time_interval1
            binance_url = 'https://api.binance.com/api/v3/klines?symbol=' + binance_market + '&interval=' + tick_interval
            binance_data = requests.get(binance_url).json()
            binance_df = pd.DataFrame(binance_data)
            binance_df.columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time',
                                  'Quote asset volume',
                                  'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume',
                                  'Ignore']
            binance_df['time'] = pd.to_datetime(binance_df['Open time'], unit='ms', origin='unix')
            number1 = binance_df['Open time'].iat[-1]
            number2 = binance_df['Open time'].iat[0]
            print(binance_df)
            number2 = binance_df['Open time'].iat[0]
            unix_time2 = number2 // 1000
            unix_time3 = number1 // 1000
            print(unix_time3)
            binance_df = binance_df[['Open', 'Close', 'High', 'Low', 'Volume', 'time']]
            binance_df['Open'] = pd.to_numeric(binance_df['Open'], errors='coerce')
            binance_df['High'] = pd.to_numeric(binance_df['High'], errors='coerce')
            binance_df['Low'] = pd.to_numeric(binance_df['Low'], errors='coerce')
            binance_df['Close'] = pd.to_numeric(binance_df['Close'], errors='coerce')
            binance_df['Volume'] = pd.to_numeric(binance_df['Volume'], errors='coerce')

            binance_df = binance_df.rename(columns={'Open': 'o', 'Close': 'close_usd', 'High': 'high_usd', 'Low': 'l', 'Volume': 'v'})
            print(binance_df)
            #print(binance_data)
            print(777)
            print(777777)
            print(unix_time2)
            # KUCOIN
            time_interval1 = {"1m":"1min", "3m":"3min", "5m":"5min","15m":"15min","30m":"30min", "1h":"1hour", "2h":"2hour", "4h":"4hour", "6h":"6hour", "8h":"8hour", "12h":"12hour", "1d":"1day", "1w":"1week"}[tick_interval]
            url = f'https://api.kucoin.com/api/v1/market/candles?type={time_interval1}&symbol={coin_name2}&startAt={unix_time2}'
            response = requests.get(url)
            data = response.json()
            df = pd.DataFrame(data)
            print(df)
            df = pd.DataFrame(data['data'], columns=['timestamp', 'open_usd',
                                                     'close_usd',
                                                     'high_usd',
                                                     'low_usd',
                                                     'volume_usd',
                                                     "turnover_usd"])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', origin='unix')
            df.set_index('timestamp')
            df = df.iloc[::-1].reset_index(drop=True)
            df['high_usd'] = pd.to_numeric(df['high_usd'], errors='coerce')
            print(df)
            diff = binance_df['high_usd'] - df['high_usd']
            print(diff)
            result = (diff / df['high_usd']) * 100
            print(result)
            df1 = pd.DataFrame(result)
            print(df1)
            df2 = pd.concat([df['timestamp'], df1['high_usd']], axis=1)
            print(df2)
            plt.plot(result)
            plt.title('спред binance-Kucoin в %')
            plt.grid(True)
            plt.show()
            plt.plot(df['timestamp'], df['high_usd'], color='blue', label='kucoin')
            plt.plot(binance_df['time'], binance_df['high_usd'], color='red', label='binance')
            plt.title('графики цены')
            plt.xlabel('дата')
            plt.ylabel('цена')
            plt.legend()
            plt.grid(True)
            plt.show()
            resultat = df.iloc[-1]['high_usd']
            text.insert(tk.END, "kucoin:" + str(resultat) + "\n")
            resultat1 = df2.iloc[-1]['high_usd']
            text.insert(tk.END, "spred % :" + str(resultat1) + "\n")
            resultat2 = binance_df.iloc[-1]['high_usd']
            text.insert(tk.END, "binance:" + str(resultat2) + "\n")
        url = f'https://api.kucoin.com/api/v1/symbols'
        response = requests.get(url)
        data = response.json()
        print(data)
        df = pd.DataFrame(data)
        print(df)
        symbols = []
        for item in data['data']:
            symbols.append(item['symbol'])
        print(symbols)
        symbols = ['BTCUSDT', 'ETHUSDT' ]
        root = tk.Tk()
        root.geometry("500x900+50+260")
        label1 = tk.Label(root, text="Select coin name:")
        label1.pack()
        coin_var1 = tk.StringVar(root)
        coin_var1.set("")
        coin_options1 = ["XRPUSDT","COCOSUSDT", "IOTAUSDT", "AMBUSDT", "CRVUSDT", "FLOWUSDT", "XEMUSDT", "UMAUSDT", "REEFUSDT", "ZECUSDT", "COMPUSDT", "ANKRUSDT", "CTSIUSDT", "ASTRUSDT", "FXSUSDT", "QNTUSDT", "ARPAUSDT", "SUIUSDT", "AGIXUSDT", "DARUSDT", "ONEUSDT", "INJUSDT", "RNDRUSDT", "ALGOUSDT", "ACHUSDT", "PERPUSDT", "SFPUSDT", "XTZUSDT", "LQTYUSDT", "ENJUSDT", "KSMUSDT", "FETUSDT", "GMTUSDT", "MAGICUSDT", "CHZUSDT", "ROSEUSDT", "ATOMUSDT", "BLURUSDT", "FTMUSDT", "AAVEUSDT", "OGNUSDT", "THETAUSDT", "SUSHIUSDT", "DYDXUSDT", "NKNUSDT", "MANAUSDT", "KAVAUSDT", "RVNUSDT", "MKRUSDT", "GALUSDT", "CHRUSDT", "SXPUSDT", "CELRUSDT", "BANDUSDT", "RLCUSDT", "C98USDT", "SSVUSDT", "IMXUSDT", "NMRUSDT", "ZENUSDT", "LPTUSDT", "OMGUSDT", "IOSTUSDT", "HFTUSDT", "LITUSDT", "TRBUSDT", "STGUSDT", "HIGHUSDT", "API3USDT", "TUSDT", "ALICEUSDT", "COMBOUSDT", "BLZUSDT", "UNFIUSDT", "GTCUSDT", "COTIUSDT", "STMXUSDT", "XVSUSDT", "IDEXUSDT", "TOMOUSDT"]
        sorted_list = sorted(coin_options1)
        coin_dropdown1 = ttk.Combobox(root, textvariable=coin_var1, values=sorted_list)
        coin_dropdown1.pack()
        def on_keyrelease(event):
            # get text from entry
            values = event.widget.get()
            values = values.strip().lower()
            print(values)
            # get data from test_list
            if values == 'BTCUSDT':
                data = coin_options1
            else:
                data = []
                for item in coin_options1:
                    if values in item.lower():
                        data.append(item)
            # update data in listbox
            update(data)
            print(7)
        def update(data):
            # clear previous data
            print(222)
            listbox.delete(0, 'end')
            # put new data
            for item in data:
                listbox.insert('end', item)
        # create a listbox
        listbox = tk.Listbox(root)
        listbox.pack()
        print(888)
        def on_select(event):
            # Получение индекса выбранного элемента
            print(333)
            index = event.widget.current()
            print(index)
            # Получение значения выбранного элемента
            values = event.widget.get()
            # Вывод индекса и значения выбранного элемента
            print(index, values)
        # add event on listbox selection
        listbox.bind('<<ListboxSelect>>', on_select)
        # add event on entry change
        coin_dropdown1.bind('<KeyRelease>', on_keyrelease)
        #listbox.bind('<<ListboxSelect>>', on_select)
        # entry1.pack()
        url = f'https://api.kucoin.com/api/v1/symbols'
        response = requests.get(url)
        data = response.json()
        print(data)
        df = pd.DataFrame(data)
        print(df)
        symbols = []
        for item in data['data']:
            symbols.append(item['symbol'])
        print(symbols)
        label4 = tk.Label(root, text="select coin name kucoin:")
        label4.pack()
        coin_var4 = tk.StringVar(root)
        coin_var4.set("")
        coin_options4 = ["XRP-USDT","BAKE-USDT", "SPELL-USDT", "COCOS-USDT", "IOTA-USDT", "AMB-USDT", "CRV-USDT", "FLOW-USDT", "XEM-USDT", "UMA-USDT", "REEF-USDT", "ZEC-USDT", "COMP-USDT", "ANKR-USDT", "CTSI-USDT", "ASTR-USDT", "FXS-USDT", "QNT-USDT", "ARPA-USDT", "SUI-USDT", "AGIX-USDT", "DAR-USDT", "ONE-USDT", "INJ-USDT", "RNDR-USDT", "ALGO-USDT", "ACH-USDT", "PERP-USDT", "SFP-USDT", "XTZ-USDT", "LQTY-USDT", "ENJ-USDT", "KSM-USDT", "FET-USDT", "GMT-USDT", "MAGIC-USDT", "CHZ-USDT", "ROSE-USDT", "ATOM-USDT", "BLUR-USDT", "FTM-USDT", "AAVE-USDT", "OGN-USDT", "THETA-USDT", "SUSHI-USDT", "DYDX-USDT", "NKN-USDT", "MANA-USDT", "KAVA-USDT", "RVN-USDT", "MKR-USDT", "GAL-USDT", "CHR-USDT", "SXP-USDT", "CELR-USDT", "BAND-USDT", "RLC-USDT", "C98-USDT", "SSV-USDT", "IMX-USDT", "NMR-USDT", "ZEN-USDT", "LPT-USDT", "OMG-USDT", "IOST-USDT", "HFT-USDT", "LIT-USDT", "TRB-USDT", "STG-USDT", "HIGH-USDT", "API3-USDT", "T-USDT", "ALICE-USDT", "COMBO-USDT", "BLZ-USDT", "UNFI-USDT", "GTC-USDT", "COTI-USDT", "STMX-USDT", "XVS-USDT", "IDEX-USDT", "TOMO-USDT"]
        sorted_list4 = sorted(symbols)
        coin_dropdown4 = ttk.Combobox(root, textvariable=coin_var4, values=sorted_list4)
        coin_dropdown4.pack()
        def on_keyrelease(event):
            # get text from entry
            value = event.widget.get()
            value = value.strip().lower()
            print(value)
            # get data from test_list
            if value == 'BTC-USDT':
                data = coin_options4
            else:
                data = []
                for item in coin_options4:
                    if value in item.lower():
                        data.append(item)
            # update data in listbox
            update(data)
        def update(data):
            # clear previous data
            listbox2.delete(0, 'end')
            # put new data
            for item in data:
                listbox2.insert('end', item)
        # create a listbox
        listbox2 = tk.Listbox(root)
        listbox2.pack()
        def on_select(event, value=None):
            # Получение индекса выбранного элемента
            index = event.widget.current()
            # Получение значения выбранного элемента
            value2 = event.widget.get()
            # Вывод индекса и значения выбранного элемента
            print(index, value)
        listbox.bind('<<ListboxSelect>>', on_select)
        coin_dropdown4.bind('<KeyRelease>', on_keyrelease)
        label2 = tk.Label(root, text="select interval")
        label2.pack()
        coin_var2 = tk.StringVar(root)
        coin_var2.set("1d")
        coin_options2 = ["1m", "3m", "5m","15m","30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "1w"]
        option_menu2 = tk.OptionMenu(root, coin_var2, *coin_options2)
        option_menu2.pack()
        button = tk.Button(root, text="START", command=on_button_click)
        button.pack()
        text = tk.Text(root)
        text.pack()
root = tk.Tk()
root.geometry("200x200+50+100")
label1 = tk.Label(root, text="Выберите первую биржу:")
label1.pack()
exchange1_var = tk.StringVar(root)
exchange1_var.set("Binance")
exchange_options1 = ["Binance", "Exmo", "Kucoin", "Bitget"]
exchange1_menu1 = tk.OptionMenu(root, exchange1_var, *exchange_options1)
exchange1_menu1.pack()
button = tk.Button(root, text="START", command=on_button_click)
button.pack()
label4 = tk.Label(root, text="Выберите вторую биржу::")
label4.pack()
exchange2_var = tk.StringVar(root)
exchange_options2 = ["Binance", "Exmo", "Kucoin", "Bitget"]
exchange2_var.set("Bitget")
exchange2_menu2 = tk.OptionMenu(root, exchange2_var, *exchange_options2)
exchange2_menu2.pack()
root.mainloop()
