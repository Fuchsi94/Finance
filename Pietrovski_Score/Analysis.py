from Pietrovski_Score import Pietrovski_Score
import argparse

"""
Usage: -t tickersymbol / --ticker tickersymbol
python Analysis.py -t aapl
calculates the pietrovski score of the apple stock

"""



parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', required=True, help='input the ticker symbol')
args = parser.parse_args()

if __name__ == '__main__':
    PS = Pietrovski_Score(args.ticker)

