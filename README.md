# Cryptocurrencies trading

## Structure of the project
This project is structured as follows. 
* `notebooks` contains [Jupyter Notebooks](https://jupyter.org/). Those are useful to explore the data efficiently.
* `shell_scripts` contains scripts whose purpose is to automate the deployment and run the source code on a remote machine.
* `src` contains the source code.
    * `feature engineering` : all the preprocessing to extract attributes of the data from which the prediction will be made.
    * `strategies` : contains algorithms for automatic trading.
    * `utils` contains some common elementary algorithms useful for this project. Among others, the `market_rules` which simulates the fees applied to the trading actions, and `wallet` which tracks the amount of currencies (crypto of fiat) left in the user's wallet.
    * `download_big_data.py` is a script that downloads all the data from the trades made on Kraken.   

## TODO (General)

* Make features which reflect the market model closer to reality.
    * *WiP* Build an approximative cumulative histogram from the data.
    * *Done* : Base algorithms on the selling price to decide whether to buy or not.
    * Analyze what is the exact probabilistic criterion to buy
    * Re-Run data collection after interruption
    

## TODO (Data Science)

* What is the daily volume traded on the market ?
* What kind of actors are playing on this market ?
* Is there a correlation with the values of CAC40, S&P500 or other european indicators ?
* Visualize the data, with dimension reduction methods for instance.
* What is the average volatility ?
* Scrap Twitter data and other social media, like Reddit.
* Scrap data from specialized press.
* Measure daily tendencies.
* Modelize what would give multiple deals at once, e.g. EUR -> XBT -> ETH -> XBT -> EUR
* See how markets communicate. Maybe Kraken is not the only interesting market.
* See the strategy of big actors : the big actors have probably interesting information.
