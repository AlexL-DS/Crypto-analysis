import requests
import pandas as pd
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def on_button_click():
    exchange1 = exchange1_var.get()
    exchange2 = exchange2_var.get()

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
        binance_df = binance_df[['Open', 'Close', 'High', 'Low', 'Volume', 'time']]
        binance_df['Open'] = pd.to_numeric(binance_df['Open'], errors='coerce')
        binance_df['High'] = pd.to_numeric(binance_df['High'], errors='coerce')
        binance_df['Low'] = pd.to_numeric(binance_df['Low'], errors='coerce')
        binance_df['Close'] = pd.to_numeric(binance_df['Close'], errors='coerce')
        binance_df['Volume'] = pd.to_numeric(binance_df['Volume'], errors='coerce')
        unix_time1 = number1 // 1000
        unix_time2 = number2 // 1000
        coin_name = coin_name.replace("USDT", "_USDT")
        coin_name = "_".join(coin_name.split(" "))
        tick_interval2 = {"5m":"5","30m": "30", "1h": "60","2h": "120","4h": "240","1d": "D", "1w": "W","1M": "M"}[tick_interval]
        exmo_url = f'https://api.exmo.com/v1.1/candles_history?symbol={coin_name}&resolution={tick_interval2}&from={unix_time2}&to={unix_time1}'
        exmo_data = requests.get(exmo_url).json()
        df = pd.DataFrame.from_dict(exmo_data['candles'])
        df['time'] = pd.to_datetime(df['t'], unit='ms')
        df['Open'] = pd.to_numeric(df['o'], errors='coerce')
        df['High'] = pd.to_numeric(df['h'], errors='coerce')
        df['Low'] = pd.to_numeric(df['l'], errors='coerce')
        df['Close'] = pd.to_numeric(df['c'], errors='coerce')
        df['Volume'] = pd.to_numeric(df['v'], errors='coerce')
        df = df[['Open', 'Close', 'High', 'Low', 'Volume', 'time']]
        df_fin = df.merge(binance_df, on='time', how='inner')
        diff = df_fin['Close_x'] - df_fin['Close_y']
        result = (diff / df_fin['Close_y']) * 100
        df_fin['spred'] = result
        ## Создаем график спреда в отдельном окне
        root = tk.Tk()
        root.title(f"Спред {coin_name}")
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(df_fin['time'], df_fin['spred'])
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()
        root.mainloop()
        ## Создаем график цены в терминале
        plt.plot(df['time'], df['Close'], color='blue', label='exmo')
        plt.plot(binance_df['time'], binance_df['Close'], color='red', label='binance')
        plt.title(f'графики цены {coin_name}')
        plt.xlabel('дата')
        plt.ylabel('цена')
        plt.legend()
        plt.grid(True)
        plt.show()
       
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
                         "FLOKIUSDT", "LINKUSDT"
                         ]
    option_menu1 = tk.OptionMenu(root, coin_var1, *coin_options1)
    option_menu1.pack()
    coin_var1.trace("w", search_coin)
    label2 = tk.Label(root, text="select interval")
    label2.pack()
    coin_var2 = tk.StringVar(root)
    coin_var2.set("1d")
    coin_options2 = ["5m", "30m", "1h", "2h", "4h","1d", "1w", "1M"]
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
exchange_options1 = ["Binance", "Exmo"]
exchange1_menu1 = tk.OptionMenu(root, exchange1_var, *exchange_options1)
exchange1_menu1.pack()
button = tk.Button(root, text="START", command=on_button_click)
button.pack()
label4 = tk.Label(root, text="Выберите вторую биржу::")
label4.pack()
exchange2_var = tk.StringVar(root)
exchange_options2 = ["Binance", "Exmo"]
exchange2_var.set("Exmo")
exchange2_menu2 = tk.OptionMenu(root, exchange2_var, *exchange_options2)
exchange2_menu2.pack()
root.mainloop()
