#Ariel Chouminov

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.animation as animation
from matplotlib import style
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

#Plotting using candlestick graphs
from matplotlib.finance import candlestick_ohlc

import urllib
import json
import pandas as pd
import numpy as np

#Removes a warning
pd.options.mode.chained_assignment = None

#Import Tkinter
import tkinter as tk
from tkinter import ttk

#Fonts
LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 12)
SMALL_FONT = ("Verdana", 12)

#Styling the Graph
style.use("ggplot")
f = plt.figure()

#Default values
exchange = "BTC-e"
counter = 9000
programName = "btce"
resampleSize = "15Min"

dataPace = "tick"
candleWidth = 0.008

paneCount = 1
topIndicator = "none"
bottomIndicator = "none"
middleIndicators = "none"
EMAs = []
SMAs = []

darkColour = "#183A54"
lightColour = "#00A3E0"

chartLoad = True


def tutorial():
    def leave(what):
        what.destroy()

    def page2():
        #Destroys the first window then starts second window
        tut.destroy()
        tut2 = tk.Tk()

        def page3():
            #Destroys the second window
            tut2.destroy()
            #Creates the third window
            tut3 = tk.Tk()
            tut3.wm_title("part 3")
            label = ttk.Label(tut3, text = "Part 3", font = NORM_FONT)
            label.pack(side = "top", fill = "x", pady = 10)
            B1 = ttk.Button(tut3, text = "done", command = tut3.destroy)
            B1.pack()
            tut3.mainloop()

        tut2 = tk.Tk()
        tut2.wm_title("part 2")
        label = ttk.Label(tut2, text = "Part 2", font = NORM_FONT)
        label.pack(side = "top", fill = "x", pady = 10)
        B1 = ttk.Button(tut2, text = "Next", command = page3)
        B1.pack()
        tut2.mainloop()

    tut = tk.Tk()
    tut.wm_title("Tutorial")
    label = ttk.Label(tut, text = "what do you need help with? ", font = NORM_FONT)
    label.pack(side = "top", fill = "x", pady=10)

    B1 = ttk.Button(tut, text = "Overview of the application", command = page2)
    B1.pack()
    B2 = ttk.Button(tut, text = "How do I trade with this client", command = lambda: popupmsg("Not yet supported"))
    B2.pack()
    B3 = ttk.Button(tut, text = "Indicator Questions/help", command = lambda: popupmsg("Not yet supported"))
    B3.pack()
    tut.mainloop()

def loadChart(action):
    global chartLoad

    if action == "start":
        chartLoad = True

    if action == "stop":
        chartLoad = False

def addMiddleIndicator(what):
    global middleIndicators
    global counter
    if dataPace == "tick":
        popupmsg("Indicators in Tick Data not available, choose 1 minute tf if you want short term.")

    if what != "none":
        if middleIndicators == "none":

            if what == "sma":
                midIQ = tk.Tk()
                midIQ.wm_title("Periods?")
                label = ttk.Label(midIQ,
                                  text="Choose how many periods you want each SMA calculation to consider.\nThese periods are contingent on your current time settings on the chart.\n1 period = 1 OHLC candlestick.",
                                  font=NORM_FONT)
                label.pack(side="top", fill="x", pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0, 10)
                e.pack()
                e.focus_set()

                def callback():
                    middleIndicators = []
                    periods = (e.get())
                    group = []
                    group.append("sma")
                    group.append(int(periods))
                    middleIndicators.append(group)
                    counter = 9000
                    print("mid indicator", middleIndicators)
                    midIQ.destroy()

                b = ttk.Button(midIQ, text="Submit", width=10, command=callback)
                b.pack()
                tk.mainloop()

            if what == "ema":
                midIQ = tk.Tk()
                midIQ.wm_title("Periods?")
                label = ttk.Label(midIQ,
                                  text="Choose how many periods you want each EMA calculation to consider.\nThese periods are contingent on your current time settings on the chart.\n1 period = 1 OHLC candlestick.",
                                  font=NORM_FONT)
                label.pack(side="top", fill="x", pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0, 10)
                e.pack()
                e.focus_set()

                def callback():
                    middleIndicators = []
                    periods = (e.get())
                    group = []
                    group.append("ema")
                    group.append(int(periods))
                    middleIndicators.append(group)
                    counter = 9000
                    print("mid indicator", middleIndicators)
                    midIQ.destroy()

                b = ttk.Button(midIQ, text="Submit", width=10, command=callback)
                b.pack()
                tk.mainloop()


        else:
            if what == "sma":
                midIQ = tk.Tk()
                midIQ.wm_title("Periods?")
                label = ttk.Label(midIQ,
                                  text="Choose how many periods you want each SMA calculation to consider.\nThese periods are contingent on your current time settings on the chart.\n1 period = 1 OHLC candlestick.",
                                  font=NORM_FONT)
                label.pack(side="top", fill="x", pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0, 10)
                e.pack()
                e.focus_set()

                def callback():
                    periods = (e.get())
                    group = []
                    group.append("sma")
                    group.append(int(periods))
                    middleIndicators.append(group)
                    counter = 9000
                    print("mid indicator", middleIndicators)
                    midIQ.destroy()

                b = ttk.Button(midIQ, text="Submit", width=10, command=callback)
                b.pack()
                tk.mainloop()

            if what == "ema":
                midIQ = tk.Tk()
                midIQ.wm_title("Periods?")
                label = ttk.Label(midIQ,
                                  text="Choose how many periods you want each EMA calculation to consider.\nThese periods are contingent on your current time settings on the chart.\n1 period = 1 OHLC candlestick.",
                                  font=NORM_FONT)
                label.pack(side="top", fill="x", pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0, 10)
                e.pack()
                e.focus_set()

                def callback():
                    periods = (e.get())
                    group = []
                    group.append("ema")
                    group.append(int(periods))
                    middleIndicators.append(group)
                    counter = 9000
                    print("mid indicator", middleIndicators)
                    midIQ.destroy()

                b = ttk.Button(midIQ, text="Submit", width=10, command=callback)
                b.pack()
                tk.mainloop()
    else:
        middleIndicators = "none"

def addTopIndicator(what):
    global topIndicator
    global counter
    global dataPace

    if dataPace == "tick":
        popupmsg("Indicators in tick data not available")

    elif what == "none":
        topIndicator = what
        counter = 9000

    elif what == "rsi":
        rsiQuestion = tk.Tk()
        rsiQuestion.wm_title("Periods?")
        label = ttk.Label(rsiQuestion, text = "Choose how many periods you want each RSI calculation to consider.")
        label.pack(side = "top", fill = "x", pady = 10)

        e = ttk.Entry(rsiQuestion)
        e.insert(0, 14)
        e.pack()
        e.focus_set()

        def callBack():
            global topIndicator
            global counter

            periods = (e.get())
            group = []
            group.append("rsi")
            group.append(periods)

            topIndicator = group
            counter = 9000
            print("Set top Indicator to", group)
            rsiQuestion.destroy()

        b = ttk.Button(rsiQuestion, text = "Submit", width = 10, command = callBack)
        b.pack()
        tk.mainloop()

    elif what == "macd":
        topIndicator = "macd"
        counter = 9000

def addBottomIndicator(what):
    global bottomIndicator
    global counter
    global dataPace

    if dataPace == "tick":
        popupmsg("Indicators in tick data not available")

    elif what == "none":
        bottomIndicator = what
        counter = 9000

    elif what == "rsi":
        rsiQuestion = tk.Tk()
        rsiQuestion.wm_title("Periods?")
        label = ttk.Label(rsiQuestion, text = "Choose how many periods you want each RSI calculation to consider.")
        label.pack(side = "top", fill = "x", pady = 10)

        e = ttk.Entry(rsiQuestion)
        e.insert(0, 14)
        e.pack()
        e.focus_set()

        def callBack():
            global bottomIndicator
            global counter

            periods = (e.get())
            group = []
            group.append("rsi")
            group.append(periods)

            bottomIndicator = group
            counter = 9000
            print("Set bottom Indicator to", group)
            rsiQuestion.destroy()

        b = ttk.Button(rsiQuestion, text = "Submit", width = 10, command = callBack)
        b.pack()
        tk.mainloop()

    elif what == "macd":
        bottomIndicator = "macd"
        counter = 9000

def changeTimeFrame(tf):
    global dataPace
    global counter

    if tf == "7d" and resampleSize == "1Min":
        popupmsg("Too Much Data Chose, choose a smaller time frame or higher OHLC interval.")
    else:
        dataPace = tf
        counter = 9000

def changeSampleSize(size, width):
    global resampleSize
    global counter
    global candleWidth

    if dataPace == "7d" and resampleSize == "1Min":
        popupmsg("Too Much Data Chose, choose a smaller time frame or higher OHLC interval.")

    elif dataPace == "tick":
        popupmsg("You're currently viewing tick data, not Open High low close")

    else:
        resampleSize = resampleSize
        counter = 9000
        candleWidth = width


def changeExchange(toWhat, pn):
    global exchange
    global counter
    global programName

    exchange = toWhat
    programName = pn
    counter = 9000

#Creates a pop up message with given text
def popupmsg(msg):
    popup = tk.Tk()

    popup.wm_title("!")
    label = ttk.Label(popup, text = msg, font = NORM_FONT)
    label.pack(side = 'top', fill = "x", pady = 10)

    #Closes the popup window
    B1 = ttk.Button(popup, text = "Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

#Creates live graph
def animate(i):
    global refreshRate
    global counter

    if chartLoad:
        if paneCount == 1:
            if dataPace == "tick":
                try:
                    if exchange == "BTC-e":
                        a = plt.subplot2grid((6,4), (0,0), rowspan = 5, colspan = 4)
                        a2 = plt.subplot2grid((6,4), (5,0), rowspan = 1, colspan = 4, sharex = a)

                        dataLink = 'https://wex.nz/api/3/trades/btc_usd?limit=2000'
                        data = urllib.request.urlopen(dataLink)
                        data = data.read().decode("utf-8")
                        data = json.loads(data)

                        #Takes all the data under 'btc_usd' in the api
                        data = data["btc_usd"]

                        #Makes data a panda dataset
                        data = pd.DataFrame(data)

                        data["datestamp"] = np.array(data["timestamp"]).astype("datetime64[s]")
                        allDates = data["datestamp"].tolist()

                        buys = data[(data['type'] == 'bid')]
                        #buys["datestamp"] = np.array(buys["timestamp"]).astype("datetime64[s]")
                        buyDates = (buys["datestamp"]).tolist()

                        sells = data[(data['type'] == 'ask')]
                        #sells["datestamp"] = np.array(sells["timestamp"]).astype("datetime64[s]")
                        sellDates = (sells["datestamp"]).tolist()

                        volume = data["amount"]

                        a.clear()

                        a.plot_date(buyDates, buys["price"], lightColour, label = "buys")
                        a.plot_date(sellDates, sells["price"], darkColour, label = "sells")

                        a2.fill_between(allDates, 0,volume, facecolor = darkColour)

                        #Makes it easier to see dates on the graph
                        a.xaxis.set_major_locator(mticker.MaxNLocator(5))
                        a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))

                        plt.setp(a.get_xticklabels(), visible = False)
                        #Creates legend
                        a.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol =2, borderaxespad = 0)
                        a.set_title("BTC Prices (USD) \nLast Price: "+str(data["price"][1999]))
                        priceData = data['price'].apply(float).tolist()

                    if exchange == "Bitstamp":
                        a = plt.subplot2grid((6, 4), (0, 0), rowspan=5, colspan=4)
                        a2 = plt.subplot2grid((6, 4), (5, 0), rowspan=1, colspan=4, sharex=a)

                        dataLink = 'https://www.bitstamp.net/api/transactions/'
                        data = urllib.request.urlopen(dataLink)
                        data = data.read().decode("utf-8")
                        data = json.loads(data)

                        # Makes data a panda dataset
                        data = pd.DataFrame(data)

                        data["datestamp"] = np.array(data["date"].apply(int)).astype("datetime64[s]")
                        dateStamps = data["datestamp"].tolist()
                        #allDates = data["datestamp"].tolist()

                        # buys = data[(data['type'] == 'bid')]
                        # # buys["datestamp"] = np.array(buys["timestamp"]).astype("datetime64[s]")
                        # buyDates = (buys["datestamp"]).tolist()
                        #
                        # sells = data[(data['type'] == 'ask')]
                        # # sells["datestamp"] = np.array(sells["timestamp"]).astype("datetime64[s]")
                        # sellDates = (sells["datestamp"]).tolist()

                        volume = data["amount"].apply(float).tolist()

                        a.clear()

                        a.plot_date(dateStamps, data["price"], lightColour, label="buys")

                        a2.fill_between(dateStamps, 0, volume, facecolor=darkColour)

                        # Makes it easier to see dates on the graph
                        a.xaxis.set_major_locator(mticker.MaxNLocator(5))
                        a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
                        plt.setp(a.get_xticklabels(), visible = False)
                        # Creates legend
                        a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3, ncol=2, borderaxespad=0)
                        a.set_title("Bitstamp BTC Prices (USD) \nLast Price: " + str(data["price"][0]))
                        priceData = data['price'].apply(float).tolist()

                    if exchange == "Bitfinex":
                        a = plt.subplot2grid((6,4), (0,0), rowspan = 5, colspan = 4)
                        a2 = plt.subplot2grid((6,4), (5,0), rowspan = 1, colspan = 4, sharex = a)

                        dataLink = 'https://api.bitfinex.com/v1/trades/btcusd?limit=2000'
                        data = urllib.request.urlopen(dataLink)
                        data = data.read().decode("utf-8")
                        data = json.loads(data)

                        #Makes data a panda dataset
                        data = pd.DataFrame(data)

                        data["datestamp"] = np.array(data["timestamp"]).astype("datetime64[s]")
                        allDates = data["datestamp"].tolist()

                        buys = data[(data['type'] == 'buy')]
                        #buys["datestamp"] = np.array(buys["timestamp"]).astype("datetime64[s]")
                        buyDates = (buys["datestamp"]).tolist()

                        sells = data[(data['type'] == 'sell')]
                        #sells["datestamp"] = np.array(sells["timestamp"]).astype("datetime64[s]")
                        sellDates = (sells["datestamp"]).tolist()

                        volume = data["amount"].apply(float).tolist()

                        a.clear()

                        a.plot_date(buyDates, buys["price"], lightColour, label = "buys")
                        a.plot_date(sellDates, sells["price"], darkColour, label = "sells")

                        a2.fill_between(allDates, 0,volume, facecolor = darkColour)

                        #Makes it easier to see dates on the graph
                        a.xaxis.set_major_locator(mticker.MaxNLocator(5))
                        a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
                        plt.setp(a.get_xticklabels(), visible=False)

                        #Creates legend
                        a.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol =2, borderaxespad = 0)
                        a.set_title("Bitfinex BTC Prices (USD) \nLast Price: "+str(data["price"][0]))
                        priceData = data['price'].apply(float).tolist()

                    if exchange == "Huobi":
                        a = plt.subplot2grid((6, 4), (0, 0), rowspan=6, colspan=4)

                        data = urllib.request.urlopen("http://seaofbtc.com/api/basic/price?key=1&tf=1d&exchange="+programName).read()
                        data = data.decode()

                        data = json.loads(data)

                        dateStamp = np.array(data[0]).astype("datetime64[s]")
                        dateStamp = dateStamp.tolist()

                        df = pd.DataFrame({'Datetime':dateStamp})

                        df['Price'] = data[1]
                        df['Volume'] = data[2]
                        df['Symbol'] = "BTCUSD"
                        df['MPLDate'] = df['Datetime'].apply(lambda date: mdates.date2num(date.to_pydatetime()))

                        df = df.set_index("Datetime")

                        lastPrice = df["Price"][-1]

                        a.plot_date(df["MPLDate"][-4500:], df['Price'][-4500:], lightColour, label = "price")

                        a.xaxis.set_major_locator(mticker.MaxNLocator(5))
                        a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))


                        a.set_title("Huobi BTCUSD PRICES BTC Prices (USD) \nLast Price: " + str(lastPrice))
                        priceData = df['price'].apply(float).tolist()


                except Exception as e:
                    print("Failed because of:", e)

            else:
                if counter > 12:
                    try:
                        if exchange == 'Huobi':
                            if topIndicator != "none":

                                a = plt.subplot2grid((6, 4), (1, 0), rowspan=5, colspan=4)
                                a0 = plt.subplot2grid((6, 4), (0, 0), sharex=a, rowspan=1, colspan=4)
                            else:
                                a = plt.subplot2grid((6, 4), (0, 0), rowspan=6, colspan=4)

                        else:
                            if topIndicator != "none" and bottomIndicator != "none":
                                # actual price chart.
                                a = plt.subplot2grid((6, 4), (1, 0), rowspan=3, colspan=4)
                                # volume!
                                a2 = plt.subplot2grid((6, 4), (4, 0), sharex=a, rowspan=1, colspan=4)
                                # top indicator
                                a0 = plt.subplot2grid((6, 4), (0, 0), sharex=a, rowspan=1, colspan=4)
                                # bottom indicator
                                a3 = plt.subplot2grid((6, 4), (5, 0), sharex=a, rowspan=1, colspan=4)

                            elif topIndicator != "none":
                                a = plt.subplot2grid((6, 4), (1, 0), rowspan=4, colspan=4)
                                a2 = plt.subplot2grid((6, 4), (5, 0), sharex=a, rowspan=1, colspan=4)
                                a0 = plt.subplot2grid((6, 4), (0, 0), sharex=a, rowspan=1, colspan=4)
                            elif bottomIndicator != "none":
                                a = plt.subplot2grid((6, 4), (0, 0), rowspan=4, colspan=4)
                                a2 = plt.subplot2grid((6, 4), (4, 0), sharex=a, rowspan=1, colspan=4)
                                # a0 = plt.subplot2grid((6,4), (0,0), sharex=a, rowspan=1, colspan=4)
                                a3 = plt.subplot2grid((6, 4), (5, 0), sharex=a, rowspan=1, colspan=4)

                            else:
                                a = plt.subplot2grid((6, 4), (0, 0), rowspan=5, colspan=4)
                                a2 = plt.subplot2grid((6, 4), (5, 0), sharex=a, rowspan=1, colspan=4)

                        print(
                            'http://seaofbtc.com/api/basic/price?key=1&tf=' + dataPace + '&exchange=' + programName)
                        data = urllib.request.urlopen(
                            'http://seaofbtc.com/api/basic/price?key=1&tf=' + dataPace + '&exchange=' + programName).read()

                        data = str(data).replace('b', '').replace("'", '')
                        data = json.loads(data)

                        dateStamp = np.array(data[0]).astype('datetime64[s]')
                        dateStamp = dateStamp.tolist()

                        df = pd.DataFrame({'Datetime': dateStamp})
                        df['Price'] = data[1]
                        df['Volume'] = data[2]
                        df['Symbol'] = "BTCUSD"
                        df['MPLDate'] = df['Datetime'].apply(lambda date: mdates.date2num(date.to_pydatetime()))
                        df = df.set_index('Datetime')

                        OHLC = df['Price'].resample(resampleSize).ohlc()
                        OHLC = OHLC.dropna()

                        volumeData = df['Volume'].resample(resampleSize).sum()

                        OHLC['dateCopy'] = OHLC.index
                        OHLC['MPLDates'] = OHLC['dateCopy'].apply(lambda date: mdates.date2num(date.to_pydatetime()))
                        del OHLC['dateCopy']

                        # volumeData['dateCopy'] = volumeData.index
                        # volumeData['MPLDates'] = volumeData['dateCopy'].apply(lambda date: mdates.date2num(date.to_pydatetime()))
                        # del volumeData['dateCopy']

                        priceData = OHLC['close'].apply(float).tolist()

                        a.clear()
                        if middleIndicators != "none":
                            for eachMA in middleIndicators:
                                ewma = pd.stats.moments.ewma
                                # print("type:",eachMA[0],"periods:",eachMA[1])
                                if eachMA[0] == "sma":
                                    sma = pd.rolling_mean(OHLC["close"], eachMA[1])
                                    label = str(eachMA[1]) + " SMA"
                                    a.plot(OHLC['MPLDates'], sma, label=label)
                                if eachMA[0] == "ema":
                                    ewma = pd.stats.moments.ewma
                                    label = str(eachMA[1]) + " EMA"
                                    a.plot(OHLC['MPLDates'], ewma(OHLC["close"], eachMA[1]), label=label)

                            # a.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                            #   ncol=2, borderaxespad=0.)

                            a.legend(loc=0)

                        if topIndicator[0] == "rsi":
                            rsiIndicator(priceData, "top")
                        elif topIndicator == "macd":
                            try:
                                computeMACD(priceData, location="top")
                            except:
                                print("failed macd")

                        if bottomIndicator[0] == "rsi":
                            rsiIndicator(priceData, "bottom")
                        elif bottomIndicator == "macd":
                            try:
                                computeMACD(priceData, location="bottom")
                            except:
                                print("failed macd")

                        csticks = candlestick_ohlc(a, OHLC[['MPLDates', 'open', 'high', 'low', 'close']].values,
                                                   width=candleWidth, colorup=lightColour, colordown=darkColour)
                        a.set_ylabel("price")
                        if exchange != 'Huobi':
                            a2.fill_between(volumeData['MPLDates'], 0, volumeData['volume'],
                                            facecolor='#183A54')  # , alpha=.4)
                            a2.set_ylabel("volume")

                        a.xaxis.set_major_locator(mticker.MaxNLocator(3))
                        a.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

                        plt.setp(a.get_xticklabels(), visible=False)

                        if topIndicator != "none":
                            plt.setp(a0.get_xticklabels(), visible=False)

                        if bottomIndicator != "none":
                            plt.setp(a2.get_xticklabels(), visible=False)

                        x = (len(OHLC['close'])) - 1

                        if dataPace == '1d':
                            title = exchange + ' 1 Day Data with ' + resampleSize + ' Bars\nLast Price: ' + str(
                                OHLC['close'][x])
                        if dataPace == '3d':
                            title = exchange + ' 3 Day Data with ' + resampleSize + ' Bars\nLast Price: ' + str(
                                OHLC['close'][x])
                        if dataPace == '7d':
                            title = exchange + ' 7 Day Data with ' + resampleSize + ' Bars\nLast Price: ' + str(
                                OHLC['close'][x])

                        if topIndicator != "none":
                            a0.set_title(title)
                        else:
                            a.set_title(title)
                        print('NewGraph!')

                        counter = 0


                    except Exception as e:
                        counter = 9000

                else:
                    counter += 1


#Main class
class BitcoinTracker(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Bitcoin Price Tracker")
        window = tk.Frame(self)
        window.pack(side = "right", fill = "both", expand = True)
        window.grid_rowconfigure(0, weight = 1)
        window.grid_columnconfigure(0, weight = 1)

        #Menu bar items
        menubar = tk.Menu(window)
        filemenu = tk.Menu(menubar, tearoff = 0)
        filemenu.add_command(label = "Save Settings", command = lambda: popupmsg("Not Supported just yet!"))
        filemenu.add_separator()
        filemenu.add_command(label = "Exit", command = quit)

        menubar.add_cascade(label = "File", menu = filemenu)

        exchangeChoice = tk.Menu(menubar, tearoff = 1)

        exchangeChoice.add_command(label= "BTC-e", command = lambda: changeExchange("BTC-e", "btce"))
        exchangeChoice.add_command(label="Bitfinex", command=lambda: changeExchange("Bitfinex", "bitfinex"))
        exchangeChoice.add_command(label="Bitstamp", command=lambda: changeExchange("Bitstamp", "bitstamp"))
        exchangeChoice.add_command(label="Huobi", command=lambda: changeExchange("Huobi", "huobi"))

        menubar.add_cascade(label = "Exchange", menu = exchangeChoice)

        #Data time frame
        dataTF = tk.Menu(menubar, tearoff = 1)
        dataTF.add_command(label = "Tick", command = lambda: changeTimeFrame('tick'))
        dataTF.add_command(label= "1 Day", command=lambda: changeTimeFrame('1d'))
        dataTF.add_command(label= "3 Day", command=lambda: changeTimeFrame('3d'))
        dataTF.add_command(label= "1 Week", command=lambda: changeTimeFrame('7d'))
        menubar.add_cascade(label = "Data Time Frame", menu = dataTF)


        OHLCI = tk.Menu(menubar, tearoff = 1)
        OHLCI.add_command(label = "Tick", command = lambda: changeTimeFrame('tick'))
        OHLCI.add_command(label = "1 Minute", command=lambda: changeSampleSize('1min', 0.0005))
        OHLCI.add_command(label = "5 Minute", command=lambda: changeSampleSize('5min', 0.003))
        OHLCI.add_command(label = "15 Minute", command=lambda: changeSampleSize('15min', 0.008))
        OHLCI.add_command(label = "30 Minute", command=lambda: changeSampleSize('30min', 0.016))
        OHLCI.add_command(label = "1 Hour", command=lambda: changeSampleSize('1H', 0.032))
        OHLCI.add_command(label = "3 Hour", command=lambda: changeSampleSize('3H', 0.096))

        menubar.add_cascade(label = "OHLC interval", menu = OHLCI)

        topIndi = tk.Menu(menubar, tearoff = 1)
        topIndi.add_command(label = "None", command = lambda: addTopIndicator('none'))
        topIndi.add_command(label ="RSI", command=lambda: addTopIndicator('rsi'))
        topIndi.add_command(label ="MACD", command=lambda: addTopIndicator('macd'))

        menubar.add_cascade(label = "Top Indicator", menu = topIndi)


        mainI = tk.Menu(menubar, tearoff = 1)
        mainI.add_command(label = "None", command = lambda: addMiddleIndicator('none'))
        mainI.add_command(label ="SMA", command=lambda: addMiddleIndicator('sma'))
        mainI.add_command(label = "EMA", command=lambda: addMiddleIndicator('ema'))

        menubar.add_cascade(label = "Main/middle Indicator", menu = mainI)


        bottomI = tk.Menu(menubar, tearoff = 1)
        bottomI.add_command(label = "None", command = lambda: addBottomIndicator('none'))
        bottomI.add_command(label = "RSI", command=lambda: addBottomIndicator('rsi'))
        bottomI.add_command(label = "MACD", command=lambda: addBottomIndicator('macd'))

        menubar.add_cascade(label = "Bottom Indicator", menu = bottomI)

        tradeButton = tk.Menu(menubar, tearoff = 1)
        tradeButton.add_command(label = "Manual Trading", command = lambda: popupmsg('This is not live yet'))
        tradeButton.add_command(label="Automated Trading", command=lambda: popupmsg('This is not live yet'))

        tradeButton.add_separator()
        tradeButton.add_command(label = "Quick Buy", command = lambda: popupmsg('This is not live yet'))
        tradeButton.add_command(label="Quick Sell", command=lambda: popupmsg('This is not live yet'))
        tradeButton.add_separator()
        tradeButton.add_command(label="Set-up Quick Buy and Sell", command=lambda: popupmsg('This is not live yet'))

        menubar.add_cascade(label = "Trading", menu = tradeButton)

        startStop = tk.Menu(menubar, tearoff = 1)
        startStop.add_command(label = "resume", command = lambda: loadChart('start'))
        startStop.add_command(label = "pause", command = lambda: loadChart('stop'))

        menubar.add_cascade(label = "Resume/Pause client", menu = startStop)

        helpMenu = tk.Menu(menubar, tearoff = 0)
        helpMenu.add_command(label = "Tutorial", command = tutorial)

        menubar.add_cascade(label = "Help", menu = helpMenu)


        #sets candle wick size
        tk.Tk.config(self, menu = menubar)

        self.frames = {}

        for f in (StartPage, Graph_Page):

            frame = f(window, self)
            self.frames[f] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")

        self.show_frame(StartPage)
        # tk.Tk.iconbitmap(self, default = "icon.ico")


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise() #Raises the frame to the front

#Creates a start page asking if you agree or disagree
class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text = """Bitcoin Price Tracker is not responsible for any loss that is caused because the use of our application.
                   We kindly ask you to use our service as an educational tool only.""", font = "Verdana 20")
        label.pack(pady = 60, padx = 30)

        #Takes you to the graph page
        button1 = ttk.Button(self, text = "Agree", command = lambda: controller.show_frame(Graph_Page))
        button1.pack()

        #Exits the application
        button2 = ttk.Button(self, text = "Disagree", command = quit)
        button2.pack()

class Graph_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="BITCOIN PRICE TRACKER", font="Verdana 15 bold")
        label.pack(pady=10, padx=5)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        tk.Frame

app = BitcoinTracker()
#Set Screen size
app.geometry("1280x720")
ani = animation.FuncAnimation(f,animate, interval = 2000)
app.mainloop()