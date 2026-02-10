"""
Lottery Investment Calculator
Handles both US and Canadian lottery calculations
"""

def calculate_us_lottery(jackpot, invest_percentage=0.90, annual_return=0.045, cycles=8):
    """
    Calculate investment returns for US lottery winnings
    
    Args:
        jackpot: Original jackpot amount (USD)
        invest_percentage: Percentage to invest (default 90%)
        annual_return: Annual return rate (default 4.5%)
        cycles: Number of 90-day cycles to calculate (default 8)
    """
    # US Lottery calculations
    cash_sum = jackpot * 0.52  # Lump sum is 52%
    federal_tax = cash_sum * 0.37
    state_tax = cash_sum * 0.055
    net_amount = cash_sum - federal_tax - state_tax
    
    # Convert to Canadian dollars
    canadian_amount = net_amount * 1.35
    
    # Split into investment and fun money
    investment_principal = canadian_amount * invest_percentage
    fun_money = canadian_amount * (1 - invest_percentage)
    
    # Calculate cycles
    cycle_results = []
    principal = investment_principal
    total_personal_withdrawals = 0
    
    for cycle in range(1, cycles + 1):
        # Interest for 90 days
        interest_earned = principal * annual_return * (90/365)
        
        # Taxes on investment income (53.53%)
        taxes_owed = interest_earned * 0.5353
        
        # Personal withdrawal (10% of interest)
        personal_withdrawal = interest_earned * 0.10
        
        # Total withdrawal
        total_withdrawal = taxes_owed + personal_withdrawal
        
        # Reinvestment
        reinvestment = interest_earned - total_withdrawal
        
        # New principal
        new_principal = principal + reinvestment
        
        total_personal_withdrawals += personal_withdrawal
        
        cycle_results.append({
            'cycle': cycle,
            'principal_start': principal,
            'interest_earned': interest_earned,
            'taxes_owed': taxes_owed,
            'personal_withdrawal': personal_withdrawal,
            'total_withdrawal': total_withdrawal,
            'reinvestment': reinvestment,
            'principal_end': new_principal
        })
        
        principal = new_principal
    
    # Calculate daily income
    net_daily_income = (investment_principal * annual_return * 0.5353) / 365
    
    return {
        'country': 'US',
        'original_jackpot': jackpot,
        'cash_sum': cash_sum,
        'federal_tax': federal_tax,
        'state_tax': state_tax,
        'net_amount_usd': net_amount,
        'net_amount_cad': canadian_amount,
        'investment_principal': investment_principal,
        'fun_money': fun_money,
        'net_daily_income': net_daily_income,
        'annual_income': net_daily_income * 365,
        'total_personal_withdrawals': total_personal_withdrawals,
        'final_principal': principal,
        'cycles': cycle_results
    }


def calculate_canadian_lottery(jackpot, invest_percentage=0.90, annual_return=0.045, cycles=8):
    """
    Calculate investment returns for Canadian lottery winnings
    
    Args:
        jackpot: Original jackpot amount (CAD) - TAX FREE!
        invest_percentage: Percentage to invest (default 90%)
        annual_return: Annual return rate (default 4.5%)
        cycles: Number of 90-day cycles to calculate (default 8)
    """
    # Canadian lotteries - NO TAX on winnings!
    net_amount = jackpot
    
    # Split into investment and fun money
    investment_principal = net_amount * invest_percentage
    fun_money = net_amount * (1 - invest_percentage)
    
    # Calculate cycles
    cycle_results = []
    principal = investment_principal
    total_personal_withdrawals = 0
    
    for cycle in range(1, cycles + 1):
        # Interest for 90 days
        interest_earned = principal * annual_return * (90/365)
        
        # Taxes on investment income (53.53%)
        taxes_owed = interest_earned * 0.5353
        
        # Personal withdrawal (10% of interest)
        personal_withdrawal = interest_earned * 0.10
        
        # Total withdrawal
        total_withdrawal = taxes_owed + personal_withdrawal
        
        # Reinvestment
        reinvestment = interest_earned - total_withdrawal
        
        # New principal
        new_principal = principal + reinvestment
        
        total_personal_withdrawals += personal_withdrawal
        
        cycle_results.append({
            'cycle': cycle,
            'principal_start': principal,
            'interest_earned': interest_earned,
            'taxes_owed': taxes_owed,
            'personal_withdrawal': personal_withdrawal,
            'total_withdrawal': total_withdrawal,
            'reinvestment': reinvestment,
            'principal_end': new_principal
        })
        
        principal = new_principal
    
    # Calculate daily income
    net_daily_income = (investment_principal * annual_return * 0.5353) / 365
    
    return {
        'country': 'Canada',
        'original_jackpot': jackpot,
        'net_amount_cad': net_amount,
        'investment_principal': investment_principal,
        'fun_money': fun_money,
        'net_daily_income': net_daily_income,
        'annual_income': net_daily_income * 365,
        'total_personal_withdrawals': total_personal_withdrawals,
        'final_principal': principal,
        'cycles': cycle_results
    }


if __name__ == "__main__":
    # Test with current jackpots
    print("=" * 80)
    print("US LOTTERY - MEGA MILLIONS ($547M)")
    print("=" * 80)
    us_result = calculate_us_lottery(547_000_000)
    print(f"Original Jackpot: ${us_result['original_jackpot']:,.0f}")
    print(f"Cash Sum (52%): ${us_result['cash_sum']:,.0f}")
    print(f"After Taxes (USD): ${us_result['net_amount_usd']:,.0f}")
    print(f"After Taxes (CAD): ${us_result['net_amount_cad']:,.0f}")
    print(f"Investment (90%): ${us_result['investment_principal']:,.0f}")
    print(f"Fun Money (10%): ${us_result['fun_money']:,.0f}")
    print(f"Daily Income: ${us_result['net_daily_income']:,.2f}")
    print(f"Annual Income: ${us_result['annual_income']:,.2f}")
    print(f"Final Principal (after 8 cycles): ${us_result['final_principal']:,.0f}")
    
    print("\n" + "=" * 80)
    print("CANADIAN LOTTERY - LOTTO 6/49 ($32M CAD)")
    print("=" * 80)
    can_result = calculate_canadian_lottery(32_000_000)
    print(f"Original Jackpot (TAX FREE!): ${can_result['original_jackpot']:,.0f}")
    print(f"Investment (90%): ${can_result['investment_principal']:,.0f}")
    print(f"Fun Money (10%): ${can_result['fun_money']:,.0f}")
    print(f"Daily Income: ${can_result['net_daily_income']:,.2f}")
    print(f"Annual Income: ${can_result['annual_income']:,.2f}")
    print(f"Final Principal (after 8 cycles): ${can_result['final_principal']:,.0f}")
    
    print("\n" + "=" * 80)
    print("COMPARISON")
    print("=" * 80)
    print(f"US ($547M) - You keep: ${us_result['net_amount_cad']:,.0f} CAD after taxes")
    print(f"Canadian ($32M) - You keep: ${can_result['net_amount_cad']:,.0f} CAD (NO TAXES!)")
    print(f"\nUS Daily Income: ${us_result['net_daily_income']:,.2f}")
    print(f"Canadian Daily Income: ${can_result['net_daily_income']:,.2f}")
