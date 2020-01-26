# StockMarketAnalysis
This repository gets the raw .txt data given by BMF&Bovespa and organizes it into a Pandas Dataframe, according to the features you want to keep track (such as average price, opening price, etc), for all assets of the market. Each cell of the DataFrame is a Pandas Series, indexed by the trading date.

## How to use:
* Download the BMF&Bovespa dataset at their website [here](http://www.bmfbovespa.com.br/en_us/services/market-data/historical-data/equities/historical-data/)

* Install bovespa `pip install bovespa`

* Run `dataprep.py` with the downloaded file name as an argument, such as in
`python3 dataprep.py COTAHIST_A2020.TXT`

* It will create a `pkl` file with the timestamp as a name, that you can use with pandas's `pd.read_pickle()` function
