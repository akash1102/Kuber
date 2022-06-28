def Calculate_macd(DF,len1, len2, len3):
    #Function to calculate MACD
    #Typical Values a (fast Moving Avg) = 12;
    #               b (slow Moving Avg) = 26;
    #               c (signal line Ma Window):
    df = DF.copy()
    df["MA_Fast"]=df["close"].ewm(span=len1,min_periods=len1).mean() 
    df["MA_Slow"]=df["close"].ewm(span=len2,min_periods=len2).mean() 
    df["MACD"]=df["MA_Fast"]-df["MA_Slow"]
    df["Signal"]=df["MACD"].ewm(span=len3,min_periods=len3).mean()
    df.dropna(inplace=True)