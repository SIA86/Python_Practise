class Statistics:
        def __init__(self, depo):
            self._depo = depo
            self.buys = 0
            self.sells = 0
            self.win_buys = 0
            self.win_sells = 0
            self.depo_buys = 0
            self.depo_sells = 0

        def __str__(self):
            return f"""
            Deposit: {self.deposit}
            Profit from buy orders: {self.depo_buys}
            Profit from sell orders: {self.depo_sells}
            Total number of deals: {self.total} (B:{self.buys}/S:{self.sells})
            Win rate of buy orders: {self.buy_rate:.2f}%
            Win rate of sell orders: {self.sell_rate:.2f}%
            Total rate: {self.total_rate:.2f}%
            """

        @property
        def total(self):
            return self.buys + self.sells

        @property    
        def buy_rate(self): 
            return self.win_buys/self.buys * 100 if self.buys != 0 else 0

        @property    
        def sell_rate(self): 
            return self.win_sells/self.sells * 100 if self.sells != 0 else 0

        @property    
        def total_rate(self): 
            return (self.win_buys + self.win_sells)/self.total * 100 if self.total != 0 else 0
        
        @property    
        def deposit(self): 
            return self._depo + self.depo_buys + self.depo_sells

        def upg_depo_buys(self, value):
            self.depo_buys += value
        
        def upg_depo_sells(self, value):
            self.depo_sells += value

        def add_buy(self):
            self.buys += 1
        
        def add_sell(self):
            self.sells += 1

        def add_win_buys(self):
            self.win_buys += 1

        def add_win_sells(self):
            self.win_sells += 1

