import yahoo_fin.stock_info as yf
import pandas as pd

class Pietrovski_Score:
    def __init__(self, ticker):

        self.get_data(ticker)
        print(ticker)
        print(self.info.loc['sector'][0])
        print(self.info.loc['industry'][0])
        print(self.info.loc['website'][0])
        self.profitability()
        self.leverage()
        self.operating_efficiency()
        self.F_Score = self.profitability_score + self.leverage_score + self.operating_efficiency_score
        print("Pietrvoski F-Score: " + str(self.F_Score) + "/9")


    #Instance Variables
    info = []
    analysts = []
    data = []
    balance_sheet = []
    income_statement = []
    cashflow_statement = []
    years = []
    F_Score = 0
    profitabiltiy_score = 0
    leverage_score = 0
    operating_efficiency_score = 0


    def get_data(self, ticker):

        self.info = yf.get_company_info(ticker)
        self.data = yf.get_data(ticker)
        self.analysts = yf.get_analysts_info(ticker)
        self.balance_sheet = yf.get_balance_sheet(ticker)
        self.income_statement = yf.get_income_statement(ticker)
        self.cashflow_statement = yf.get_cash_flow(ticker)
        self.years = self.balance_sheet.columns

    def profitability(self):

        # SCORE 1 & 2: net Income
        net_income = self.income_statement[self.years[0]].loc['netIncome']
        net_income_pre = self.income_statement[self.years[1]].loc['netIncome']
        ni_score = 1 if net_income > 0 else 0
        ni_score_2 = 1 if net_income > net_income_pre else 0

        # SCORE 3: Operating Cashflow
        op_cf = self.cashflow_statement[self.years[0]].loc['totalCashFromOperatingActivities']
        op_cf_score = 1 if op_cf > 0 else 0

        # SCORE 4: Change in RoA
        avg_assets = (self.balance_sheet[self.years[0]].loc['totalAssets'] + self.balance_sheet[self.years[1]].loc['totalAssets']) / 2
        avg_assets_pre = (self.balance_sheet[self.years[1]].loc['totalAssets'] + self.balance_sheet[self.years[2]].loc['totalAssets']) / 2
        RoA = net_income / avg_assets
        RoA_pre = net_income_pre / avg_assets_pre
        RoA_score = 1 if RoA > RoA_pre else 0

        # SCORE 5: Accruals
        total_assets = self.balance_sheet[self.years[0]].loc['totalAssets']
        accruals = op_cf / total_assets - RoA
        ac_score = 1 if accruals > 0 else 0

        self.profitability_score = ni_score + ni_score_2 + op_cf_score + RoA_score + ac_score
        print("Profitability Score:" + str(self.profitability_score))

    def leverage(self):

        # SCORE 6: long-term debt ratio
        try:
            lt_debt = self.balance_sheet[self.years[0]].loc['longTermDept']
            total_assets = self.balance_sheet[self.years[0]].loc['totalAssets']
            debt_ratio = lt_debt / total_assets
            debt_ratio_score = 1 if debt_ratio < 0.4 else 0
        except:
            debt_ratio_score = 1

        # SCORE 7: Current ratio
        current_assets = self.balance_sheet[self.years[0]].loc['totalCurrentAssets']
        current_liab = self.balance_sheet[self.years[0]].loc['totalCurrentLiabilities']
        current_ratio = current_assets / current_liab
        current_ratio_score = 1 if current_ratio > 1 else 0

        self.leverage_score = debt_ratio_score + current_ratio_score
        print("Leverage Score: " + str(self.leverage_score))

    def operating_efficiency(self):

        # SCORE 8: Gross margin
        gp = self.income_statement[self.years[0]].loc['grossProfit']
        gp_pre = self.income_statement[self.years[1]].loc['grossProfit']
        revenue = self.income_statement[self.years[0]].loc['totalRevenue']
        revenue_pre = self.income_statement[self.years[1]].loc['totalRevenue']
        gm = gp / revenue
        gm_pre = gp_pre / revenue_pre
        gm_score = 1 if gm > gm_pre else 0

        # SCORE 9: Asset turnover
        avg_assets = (self.balance_sheet[self.years[0]].loc['totalAssets'] + self.balance_sheet[self.years[1]].loc['totalAssets']) / 2
        avg_assets_pre = (self.balance_sheet[self.years[1]].loc['totalAssets'] + self.balance_sheet[self.years[2]].loc['totalAssets']) / 2
        asset_turnover = revenue / avg_assets
        asset_turnover_pre = revenue_pre / avg_assets_pre
        asset_turnover_score = 1 if asset_turnover > asset_turnover_pre else 0

        self.operating_efficiency_score = gm_score + asset_turnover_score
        print("Operating Efficiency Score: " + str(self.operating_efficiency_score))

