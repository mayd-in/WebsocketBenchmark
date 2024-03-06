from enum import Enum

class Order(Enum):
    DONOTHING = 0
    BUY = 1
    SELL = 2

class Strategy:
    def feed_value(self, value):
        pass

    def result(self):
        pass

class TradingStrategy(Strategy):
    def __init__(self, window_size=5):
        self.__numbers = []
        self.__total = 0
        self.__window_size = window_size

    def feed_value(self, value):
        if len(self.__numbers) == self.__window_size:
            self.__total -= self.__numbers[0]
            self.__numbers.pop(0)
        
        self.__numbers.append(value)
        self.__total += value

    def moving_average(self):
        return self.__total / len(self.__numbers)
    
    def min_max_average(self):
        return (self.__numbers[0] + self.__numbers[-1])/2
    
    def result(self):
        moving_average = self.moving_average()
        min_max_average = self.min_max_average()
        ratio = min_max_average / moving_average
        if ratio > 1.02:
            return Order.BUY
        elif ratio < 0.98:
            return Order.SELL
        else:
            return Order.DONOTHING