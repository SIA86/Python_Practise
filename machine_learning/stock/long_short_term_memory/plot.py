import pandas as pd
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt


class Statistics:
    def __init__(self, depo: int = 50000):
        self.depo = depo
        self._wins = 0
        
    
    @property
    def wins(self):
        return self._wins
        
    def add_wins(self):
        self._wins += 1
   
    
