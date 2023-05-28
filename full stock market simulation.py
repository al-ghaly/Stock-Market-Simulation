import pylab
import random


class Stock(object):
    def __init__(self, price, distribution, vol):
        self.price = price
        self.history = [price]
        self.distribution = distribution
        self.last_change_influence = 0
        self.vol = vol

    def set_price(self, price):
        self.price = price
        self.history.append(price)

    def get_price(self):
        return self.price

    def make_move(self, market_bias, momentum):
        old_price = self.price
        base_move = self.distribution(self.vol) + market_bias
        self.price *= 1 + base_move
        self.price += self.last_change_influence * random.choice([0, 1]) * momentum
        self.history.append(self.price)
        change = self.price - old_price
        self.last_change_influence = change
        if change >= 0:
            self.last_change_influence = min(change, old_price * 0.01)
        else:
            self.last_change_influence = max(change, -old_price * 0.01)

    def show_history(self, figure_number, test0):
        pylab.figure(figure_number)
        pylab.plot(self.history)
        pylab.title('Closing Price, Test ' + test0)
        pylab.xlabel('DAY')
        pylab.ylabel('PRICE')


class SimpleMarket:
    def __init__(self, num_stocks, vol_up):
        self.stocks = []
        self.bias = 0
        for n in range(num_stocks):
            volatility = random.uniform(0, vol_up)
            distribution = lambda vol: random.gauss(0, vol)
            stock = Stock(100, distribution, volatility)
            self.add_stock(stock)

    def add_stock(self, stk):
        self.stocks.append(stk)

    def set_bias(self, bias):
        self.bias = bias

    def get_bias(self):
        return self.bias

    def get_stocks(self):
        return self.stocks[:]

    def move(self, mo):
        prices = []
        for s in self.stocks:
            s.make_move(self.bias, mo)
            prices.append(s.get_price())
        return prices


class Market(SimpleMarket):
    def __init__(self, num_sts, vol_up, daily_bias_range):
        SimpleMarket.__init__(self, num_sts, vol_up)
        self.daily_bias_range = daily_bias_range

    def move(self, mo):
        prices = []
        daily_bias = random.gauss(self.daily_bias_range[0], self.daily_bias_range[1])
        for s in self.stocks:
            s.make_move(self.bias + daily_bias, mo)
            prices.append(s.get_price())
        return prices


def sim_market(mkt, num_days, mo):
    end_prices = []
    for i in range(num_days):
        values = mkt.move(mo)
        mean_of_day = sum(values) / len(values)
        end_prices.append(mean_of_day)
    return end_prices


def plot_average_prices_over_days(end_prices, title):
    pylab.plot(end_prices)
    pylab.title(title)
    pylab.xlabel('DAYS')
    pylab.ylabel('AVERAGE PRICE OF ALL STOCKS')


def plot_distribution_at_end(market, title, color):
    prices = []
    for i in market.get_stocks():
        prices.append(i.get_price())
    mean = sum(prices) / len(prices)
    prices.sort()
    pylab.plot(prices, color)
    pylab.axhline(mean, color=color)
    pylab.title(title)
    pylab.xlabel('Stock')
    pylab.ylabel('Last Sale')
    pylab.semilogy()


def run_trial(show_history, test1, p):
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    mkt = Market(p['numStocks'], p['volUB'], p['dailyBiasRange'])
    mkt.set_bias(p['bias'])
    end_prices = sim_market(mkt, p['numDays'], p['mo'])
    pylab.figure(1)
    plot_average_prices_over_days(end_prices, 'Average Closing Prices')
    pylab.figure(2)
    plot_distribution_at_end(mkt, 'Distribution of Prices', colors[test1 % len(colors)])
    if show_history:
        for s in mkt.get_stocks():
            s.show_history(test1+2, str(test1))


def run_test(num_trials):
    num_days_per_year = 200.0
    params = {}
    params['numDays'] = 200
    params['numStocks'] = 500
    params['bias'] = 0.1/num_days_per_year
    params['volUB'] = 12.0/num_days_per_year
    params['mo'] = 1.1/num_days_per_year
    params['dailyBiasRange'] = (0.0, 4.0/200.0)

    for t in range(1, num_trials+1):
        run_trial(True, t, params)


run_test(3)
pylab.show()
