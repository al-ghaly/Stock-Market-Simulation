import pylab
import random


class Stock(object):
    def __init__(self, price, distribution):
        self.price = price
        self.history = [price]
        self.distribution = distribution
        self.last_change = 0

    def set_price(self, price):
        self.price = price
        self.history.append(price)

    def get_price(self):
        return self.price

    def make_move(self, market_bias, momentum=False):
        old_price = self.price
        base_move = self.distribution() + market_bias
        self.price *= 1 + base_move
        if momentum:
            self.price += self.last_change * random.gauss(.5, .5)
        if self.price < .01:
            self.price = 0
        self.history.append(self.price)
        self.last_change = old_price - self.price

    def show_history(self, figure_number):
        pylab.figure(figure_number)
        pylab.plot(self.history)
        pylab.title('Closing Price, Test ' + str(figure_number))
        pylab.xlabel('DAY')
        pylab.ylabel('PRICE')


def test():
    def run_simulation(stocks, fig):
        mean = 0
        for stock in stocks:
            for day in range(num_days):
                stock.make_move(market_bias, momentum)
            stock.show_history(fig)
            mean += stock.get_price()
        mean = mean / float(num_stocks)
        pylab.axhline(mean)
        pylab.show()

    num_days = 100
    market_bias = 0
    momentum = False
    num_stocks = 20
    stokes1 = []
    stokes2 = []
    for i in range(num_stocks):
        volatility = random.uniform(0, .20)
        d1 = lambda: random.uniform(-volatility, volatility)
        d2 = lambda: random.gauss(0, volatility / 2)
        stokes1.append(Stock(100, d1))
        stokes2.append(Stock(100, d2))
    run_simulation(stokes1, 1)
    run_simulation(stokes2, 2)


test()
