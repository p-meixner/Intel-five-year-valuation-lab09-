"""ABG classroom pro forma. USD millions except per-share values.

Inputs supplied by the lab; share count is 17.951349 million (June 2026).
Run with: python proforma.py
"""

GROWTH = 0.018
GROSS_MARGIN = 0.1705
SGA_RATIOS = [0.665, 0.655, 0.645, 0.645, 0.645]
DEPRECIATION_RATE = 82.4 / 3070.4
INVENTORY_DAYS = 2135.8 / (17999.0 - 3071.7) * 365
FLOOR_PLAN_RATIO = 2027.0 / 2135.8
IMPAIRMENT = 120.0
CAPEX = 250.0
TAX_RATE = 0.255
OTHER_WC_RATE = 0.008
MIN_CASH = 25.0
REVOLVER_LIMIT = 850.0
REVOLVER_RATE = 0.06
REPAYMENT = 150.0
BUYBACK = 150.0
FLOOR_PLAN_RATE = 0.0467
DEBT_RATE = 0.0544
COST_OF_EQUITY = 0.10
TERMINAL_GROWTH = 0.025
SHARES = 17.951349

OPENING = dict(revenue=17999.0, inventory=2135.8, ppe=3070.4,
               other_assets=6371.6, cash=40.4, floor_plan=2027.0,
               debt=3572.0, other_liabilities=2127.5, equity=3891.7,
               revolver=0.0)


def balance_gap(row):
    return (row['cash'] + row['inventory'] + row['ppe'] + row['other_assets']
            - row['floor_plan'] - row['debt'] - row['revolver']
            - row['other_liabilities'] - row['equity'])


def assert_balanced(year, row):
    """Check independently computed balances; never plug cash to equity."""
    gap = balance_gap(row)
    if abs(gap) > 1e-7:
        raise ValueError(f'{year}: balance-sheet gap {gap:.1f}')
    if row['cash'] < MIN_CASH - 1e-7:
        raise ValueError(f"{year}: cash below minimum; gap {row['cash'] - MIN_CASH:.1f}")
    if not -1e-7 <= row['revolver'] <= REVOLVER_LIMIT + 1e-7:
        raise ValueError(f'{year}: revolver outside 0 to {REVOLVER_LIMIT:.1f}')


def project():
    rows = []
    opening = OPENING.copy()
    assert_balanced('FY2025', opening)
    for year, sga_ratio in zip(range(2026, 2031), SGA_RATIOS):
        row = {'year': year}
        row['revenue'] = opening['revenue'] * (1 + GROWTH)
        row['gross_profit'] = row['revenue'] * GROSS_MARGIN
        row['cost_of_sales'] = row['revenue'] - row['gross_profit']
        row['sga'] = row['gross_profit'] * sga_ratio
        row['depreciation'] = opening['ppe'] * DEPRECIATION_RATE
        row['impairment'] = IMPAIRMENT
        row['operating_income'] = (row['gross_profit'] - row['sga']
                                   - row['depreciation'] - IMPAIRMENT)
        row['interest'] = (opening['floor_plan'] * FLOOR_PLAN_RATE
                           + opening['debt'] * DEBT_RATE
                           + opening['revolver'] * REVOLVER_RATE)
        row['pretax'] = row['operating_income'] - row['interest']
        row['tax'] = max(0, row['pretax']) * TAX_RATE
        row['net_income'] = row['pretax'] - row['tax']
        row['inventory'] = row['cost_of_sales'] * INVENTORY_DAYS / 365
        row['floor_plan'] = row['inventory'] * FLOOR_PLAN_RATIO
        row['ppe'] = opening['ppe'] + CAPEX - row['depreciation']
        row['change_other_wc'] = OTHER_WC_RATE * (row['revenue'] - opening['revenue'])
        row['other_assets'] = opening['other_assets'] + row['change_other_wc'] - IMPAIRMENT
        row['repayment'] = REPAYMENT
        row['debt'] = opening['debt'] - row['repayment']
        row['other_liabilities'] = opening['other_liabilities']
        row['equity'] = opening['equity'] + row['net_income'] - BUYBACK
        row['change_inventory'] = row['inventory'] - opening['inventory']
        row['change_floor_plan'] = row['floor_plan'] - opening['floor_plan']
        row['operating_cash_flow'] = (row['net_income'] + row['depreciation'] + IMPAIRMENT
                                      - row['change_inventory'] - row['change_other_wc']
                                      + row['change_floor_plan'])
        row['capex_outflow'] = -CAPEX
        row['fcfe'] = row['operating_cash_flow'] - CAPEX - row['repayment']
        cash_before_revolver = opening['cash'] + row['fcfe'] - BUYBACK
        if cash_before_revolver < MIN_CASH:
            change_revolver = min(MIN_CASH - cash_before_revolver,
                                  REVOLVER_LIMIT - opening['revolver'])
        else:
            change_revolver = -min(cash_before_revolver - MIN_CASH, opening['revolver'])
        row['change_revolver'] = change_revolver
        row['revolver'] = opening['revolver'] + change_revolver
        row['cash'] = cash_before_revolver + change_revolver
        row['repayment_outflow'] = -row['repayment']
        row['buyback_outflow'] = -BUYBACK
        row['financing_cash_flow'] = -row['repayment'] - BUYBACK + change_revolver
        row['opening_cash'] = opening['cash']
        row['change_cash'] = row['cash'] - opening['cash']
        row['assets'] = row['cash'] + row['inventory'] + row['ppe'] + row['other_assets']
        row['liabilities_equity'] = (row['floor_plan'] + row['debt'] + row['revolver']
                                      + row['other_liabilities'] + row['equity'])
        assert_balanced(f'FY{year}E', row)
        rows.append(row)
        opening = row
    return rows


def print_table(title, fields, rows):
    print(f'\n{title} (USD millions)')
    print(f"{'':32}" + ''.join(f"{'FY' + str(r['year']) + 'E':>13}" for r in rows))
    for label, key in fields:
        print(f'{label:32}' + ''.join(f'{r[key]:13.1f}' for r in rows))


def main():
    rows = project()
    print_table('Income statement', [
        ('Revenue', 'revenue'), ('Cost of sales', 'cost_of_sales'),
        ('Gross profit', 'gross_profit'), ('SG&A', 'sga'),
        ('Depreciation', 'depreciation'), ('Impairment', 'impairment'),
        ('Operating income', 'operating_income'), ('Interest', 'interest'),
        ('Pretax income', 'pretax'), ('Tax', 'tax'), ('Net income', 'net_income')], rows)
    print_table('Balance sheet', [
        ('Cash', 'cash'), ('Inventory', 'inventory'), ('PP&E', 'ppe'),
        ('Other assets', 'other_assets'), ('Total assets', 'assets'),
        ('Floor plan', 'floor_plan'), ('Term debt', 'debt'), ('Revolver', 'revolver'),
        ('Other liabilities', 'other_liabilities'), ('Equity', 'equity'),
        ('Liabilities + equity', 'liabilities_equity')], rows)
    print_table('Cash flow statement', [
        ('Net income', 'net_income'), ('Add depreciation', 'depreciation'),
        ('Add impairment', 'impairment'), ('Increase inventory (subtract)', 'change_inventory'),
        ('Increase other WC (subtract)', 'change_other_wc'),
        ('Increase floor plan (add)', 'change_floor_plan'),
        ('Operating cash flow', 'operating_cash_flow'), ('Capital spending', 'capex_outflow'),
        ('Debt repayment', 'repayment_outflow'), ('Share buyback', 'buyback_outflow'),
        ('Revolver draw / (repayment)', 'change_revolver'),
        ('Financing cash flow', 'financing_cash_flow'), ('Change in cash', 'change_cash'),
        ('Opening cash', 'opening_cash'), ('Closing cash', 'cash'), ('FCFE', 'fcfe')], rows)
    print('\nChecks')
    for row in rows:
        assert_balanced(f"FY{row['year']}E", row)
        print(f"FY{row['year']}E: assets - liabilities - equity = {abs(balance_gap(row)):.1f}; "
              f"cash >= {MIN_CASH:.1f}: PASS; revolver within limit: PASS")
    if COST_OF_EQUITY <= TERMINAL_GROWTH:
        raise ValueError('Cost of equity must exceed terminal growth')
    pv_fcfe = sum(r['fcfe'] / (1 + COST_OF_EQUITY) ** t
                  for t, r in enumerate(rows, 1))
    terminal = ((rows[-1]['fcfe'] + rows[-1]['repayment']) * (1 + TERMINAL_GROWTH)
                / (COST_OF_EQUITY - TERMINAL_GROWTH))
    pv_terminal = terminal / (1 + COST_OF_EQUITY) ** 5
    equity_value = pv_fcfe + pv_terminal
    print(f'\nEquity value (USD millions): {equity_value:.2f}')
    print(f'Share of value after 2030: {pv_terminal / equity_value:.2%}')
    print(f'Value per share (USD): {equity_value / SHARES:.2f}')


if __name__ == '__main__':
    main()
