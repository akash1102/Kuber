from Utilities import kuberconstants
from fyers_api import fyersModel
import pandas as pd

class HistoricalDataGenerator:
    def __init__(self, access_token, logPath, symbol, startDate, endDate,interval):
        self.access_token = access_token
        self.logPath = logPath
        self.symbol = symbol
        self.startDate = startDate
        self.endDate = endDate
        self.interval = interval

    def historical_bydate(self):
        fyers = fyersModel.FyersModel(client_id=kuberconstants.CLIENT_ID, token=self.access_token, log_path="/")
        data = {"symbol":self.symbol, "resolution": str(self.interval),"date_format":"1","range_from":str(self.startDate),"range_to":str(self.endDate),"cont_flag":"1"}
        nx = fyers.history(data)
        cols = ['datetime','open','high','low','close','volume']
        dataframe = pd.DataFrame.from_dict(nx['candles'])
        dataframe.columns = cols
        dataframe['datetime'] = pd.to_datetime(dataframe['datetime'],unit = "s")
        dataframe['datetime'] = dataframe['datetime'].dt.tz_localize('utc').dt.tz_convert('Asia/Kolkata')
        dataframe['datetime'] = dataframe['datetime'].dt.tz_localize(None)
        dataframe = dataframe.set_index('datetime')
        return dataframe