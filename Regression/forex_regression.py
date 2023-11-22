import requests
import pandas as pd
import numpy as np 
import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        
        self.geometry('1200x400+200+200')
        self.title('Forex')
        self.update()

        # CREATING FRAME FOR THE GRAPH 
        self.frame = customtkinter.CTkFrame(
            master = self,
            height = self.winfo_height() * 0.95,
            width = self.winfo_width() * 0.66,
            fg_color = 'grey'
        )

        self.frame.place(relx = 0.33, rely = 0.025)

        # GET LIST OF CURRENCY CODES FROM FILE 
        self.currencies = list(
            pd.read_csv('codes-all.csv')['AlphabeticCode'].values
            )
        # self.lang = ['USD', 'JPY', 'ALL', 'DZD','USD', 'EUR', 'AOA', 'XCD']
        # self.lang_menu = customtkinter.CTkOptionMenu(
        #     master = self,
        #     values = self.lang,
        #     font = ('Arial', 12)
        # )
        # self.lang_menu.place(relx = 0.025, rely = 0.55)
        # self.lang_menu.set('Base Currency')

        # SELECT BASE CURRENCY 
        self.base_currency = customtkinter.CTkOptionMenu(
            master = self,
            values = self.currencies[:8],
            font = ('Arial', 12)
        )
        self.base_currency.place(relx = 0.025, rely = 0.75)
        self.base_currency.set('Base Currency')

        # SELECT QUOTE CURRENCY
        self.qoute_currency = customtkinter.CTkOptionMenu(
            master = self,
            values = self.currencies[:8],
            font = ('Arial', 12)
        )
        self.qoute_currency.place(relx = 0.025, rely = 0.95)
        self.qoute_currency.set('Qoute Currency')

        # # DISPLAY START AND END DATE, BASE AND QOUTE CURRENCY 
        # self.display_text = customtkinter.CTkTextbox(
        #     master = self,
        #     height = 200,
        #     width = 300,

        # )
        # self.display_text.place(relx = 0.025, rely = 0.05)

        # BUTTON TO THE DATA 
        self.button_data = customtkinter.CTkButton(
            master = self,
            text = 'Get Data',
            width = 300,
            height = 50,
            command = self.forex_data
        )
        self.button_data.place(relx = 0.025, rely = 0.15)
        
        # BUTTON TO DISPLAY THE GRAPH 
        self.button = customtkinter.CTkButton(
            master = self,
            text = 'Update Graph',
            width = 300,
            height = 50,
            command = self.update_window
        )
        self.button.place(relx = 0.025, rely = 0.25)
      

    # IMPORTING FOREX DATA
    def forex_data(self):
        self.api_key = '4mw1YIHn3X-r0jf08duW'
        self.start_date="2022-08-11-01:00"
        self.end_date="2023-08-11-13:00"
        self.url = 'https://marketdata.tradermade.com/api/v1/timeseries?currency='
        self.instrument = self.base_currency.get() + self.qoute_currency.get()
        self.format = 'split'
        self.interval =  'daily'
        self.df = pd.read_json(
            self.url + self.instrument + '&api_key=' + self.api_key 
            + '&start_date=' + self.start_date + '&end_date='
            + self.end_date +'&format='+ self.format + '&interval=' + self.interval
        )

        self.df = pd.DataFrame(
            self.df.quotes['data'],
            columns = self.df.quotes['columns']
        )

        self.df.to_csv(f'{self.base_currency.get()}_to_{self.qoute_currency.get()}.csv')


    # PLOTING THE GRAPH ON THE FRAME 
    def update_window(self):
        self.fig, self.ax = plt.subplots()
        self.fig.set_size_inches(11, 5.3)
        
        self.df_data = pd.read_csv(f'{self.base_currency.get()}_to_{self.qoute_currency.get()}.csv')
        self.df_data = self.df_data[['date', 'open']]
        self.df_data.date = pd.to_datetime(self.df_data.date)

        self.ax.plot(self.df_data.date, self.df_data.open, c = 'red')
        self.ax.axis('off')
        self.fig.subplots_adjust(
            left = 0,
            right = 1,
            bottom = 0,
            wspace = 0,
            hspace = 0
        )

        self.canvas = FigureCanvasTkAgg(self.fig, master = self)
        self.canvas.draw()

        self.canvas.get_tk_widget().place(relx = 0.33, rely = 0.025)
        self.update()


    def update_surface(self, other):
        self.fig, self.ax = plt.subplots()
        self.fig.set_size_inches(11, 5.3)

        self.ax.plot(self.df_data, c = 'red')
        self.ax.axis('off')
        self.fig.subplots_adjust(
            left = 0, right = 1,
            bottom = 0, top = 1,
            wspace = 0, hspace = 0
            )

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(relx=0.33, rely=0.025)
        self.update()



if __name__ == '__main__':
    app = App()
    app.mainloop()
