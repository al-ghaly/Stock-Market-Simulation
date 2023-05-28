import pylab
import random
trading_days_per_year = 200


class Stock:
    def __init__(self, ticker, volatility):
        self.volatility = volatility
        self.ticker = ticker
        self.price = None
        self.history = []

    def set_price(self, price):
        self.price = price
        self.history.append(price)

    def get_price(self):
        return self.price

    def get_ticker(self):
        return self.ticker

    def make_move(self, bias):
        if self.price == 0:
            return
        base_move = bias + random.uniform(- self.volatility, self.volatility)
        self.price *= 1 + base_move
        if self.price < .01:
            self.price = 0
        self.history.append(self.price)


class Market:
    def __init__(self):
        self.sectors = []
        self.tickers = set()

    def add_sector(self, sector):
        if sector.get_name() in self.sectors:
            raise ValueError('Duplicated sectors')
        for ticker in sector.get_tickers():
            if ticker in self.tickers:
                raise ValueError('a ticker in sector is already in market')
            else:
                self.tickers.add(ticker)
        self.sectors.append(sector)

    def get_sectors(self):
        return self.sectors

    def get_stocks(self):
        stocks = []
        for sector in self.sectors:
            stocks += sector.get_stocks()
        return stocks

    def make_move_all_stocks(self):
        values = []
        for sector in self.sectors:
            values += sector.move_all_stocks()
        return values


class Sector:
    def __init__(self, name, bias):
        self.tickers = set()
        self.name = name
        self.stocks = []
        self.bias = bias
        self.origin_bias = bias

    def add_stock(self, stock):
        if stock.get_ticker() in self.tickers:
            raise ValueError('Duplicated ticker')

        self.tickers.add(stock.get_ticker())
        self.stocks.append(stock)

    def get_stocks(self):
        return self.stocks

    def get_tickers(self):
        return self.tickers

    def set_bias(self, bias):
        self.bias = bias

    def get_bias(self):
        return self.bias

    def get_original_bias(self):
        return self.origin_bias

    def same_sector(self, other):
        return self.name == other.name

    def get_name(self):
        return self.name

    def move_all_stocks(self):
        values = []
        for stock in self.stocks:
            stock.make_move(self.bias)
            values.append(stock.get_price())
        return values


def generate_sector(sector_size, sector_name, bias):
    sector = Sector(sector_name, bias)
    for i in range(sector_size):
        ticker = sector_name + ' Ticker' + str(i)
        volatility = random.uniform(- .04, .04)
        stock = Stock(ticker, volatility)
        stock.set_price(100)
        try:
            sector.add_stock(stock)
        except ValueError:
            print('Error in generate stocks should never reach here')
            raise AssertionError
    return sector


def generate_market(num_sectors, sector_size, bias):
    market = Market()
    for i in range(num_sectors):
        sector = generate_sector(sector_size, 'Sector ' + str(i), bias)
        market.add_sector(sector)
    return market


def simulate_market(market, num_days):
    end_prices = []
    for i in range(num_days):
        if i % (trading_days_per_year / 4) == 0:
            for sector in market.get_sectors():
                new_bias = sector.get_original_bias() + random.gauss(0, 2 * sector.get_original_bias())
                sector.set_bias(new_bias)
        values = market.make_move_all_stocks()
        values = pylab.array(values)
        mean = values.sum() / float(len(values))
        end_prices.append(mean)
    return end_prices


def plot_value_over_time(end_prices, title):
    pylab.plot(end_prices)
    pylab.title(title)
    pylab.xlabel('Days')
    pylab.ylabel('Average Price')


def plot_distribution_at_end(market, title):
    prices = []
    for stock in market.get_stocks():
        prices.append(stock.get_price())
    pylab.hist(prices, bins=20)
    pylab.title(title)
    pylab.xlabel('Last Sale')
    pylab.ylabel('Number of stocks')


def simulation(num_simulations):
    num_days = 500
    bias = .11 / 2000
    num_of_sectors = 5
    sector_size = 500
    mean = 0
    print('Testing model on', num_days, 'Days')
    for i in range(num_simulations):
        pylab.figure(1)
        market = generate_market(num_of_sectors, sector_size, bias)
        end_prices = simulate_market(market, num_days)
        mean += end_prices[-1]
        title = 'Clothing Price with ' + str(num_of_sectors) + ' Sectors' + ' 5 Trials'
        plot_value_over_time(end_prices, title)
        pylab.figure(2)
        plot_distribution_at_end(market, title)
    mean_closing = mean / num_simulations
    print('Mean closing with', num_of_sectors, 'Sectors is :', mean_closing)


simulation(3)
pylab.show()
