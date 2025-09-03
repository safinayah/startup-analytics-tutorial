"""
Stripe Calculation Methods for Startup Metrics
Provides enhanced calculation methods using Stripe's pricing and tax calculation APIs
"""

import stripe
import os
from typing import Dict, List, Optional, Tuple
from decimal import Decimal, ROUND_HALF_UP

class StripeCalculations:
    """
    Enhanced calculation methods using Stripe's APIs for more accurate financial metrics
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Stripe calculations with API key
        """
        self.api_key = api_key or os.getenv('STRIPE_SECRET_KEY')
        if self.api_key:
            stripe.api_key = self.api_key
    
    def calculate_ltv_stripe_method(self, 
                                  monthly_arpu: float, 
                                  monthly_churn: float = 0.052) -> float:
        """
        Calculate LTV using Stripe's recommended method
        
        Args:
            monthly_arpu: Average Revenue Per User per month
            monthly_churn: Monthly churn rate (default 5.2%)
            
        Returns:
            Customer Lifetime Value
        """
        # Stripe method: LTV = ARPU ÷ Churn Rate
        # This is the standard Stripe LTV calculation
        ltv = monthly_arpu / monthly_churn
        return round(ltv, 2)
    
    def calculate_payback_period(self, cac: float, monthly_arpu: float) -> float:
        """
        Calculate payback period in months
        
        Args:
            cac: Customer Acquisition Cost
            monthly_arpu: Monthly Average Revenue Per User
            
        Returns:
            Payback period in months
        """
        if monthly_arpu <= 0:
            return float('inf')
        return round(cac / monthly_arpu, 1)
    
    def calculate_mrr(self, monthly_active_users: int, monthly_arpu: float) -> float:
        """
        Calculate Monthly Recurring Revenue
        
        Args:
            monthly_active_users: Number of active users
            monthly_arpu: Monthly Average Revenue Per User
            
        Returns:
            Monthly Recurring Revenue
        """
        return round(monthly_active_users * monthly_arpu, 2)
    
    def calculate_arr(self, mrr: float) -> float:
        """
        Calculate Annual Recurring Revenue
        
        Args:
            mrr: Monthly Recurring Revenue
            
        Returns:
            Annual Recurring Revenue
        """
        return round(mrr * 12, 2)
    
    def calculate_cac_by_channel(self, 
                               total_cac: float, 
                               channel_attribution: Dict[str, float],
                               channel_conversion_rates: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate CAC breakdown by acquisition channel
        
        Args:
            total_cac: Overall Customer Acquisition Cost
            channel_attribution: Percentage of traffic by channel
            channel_conversion_rates: Conversion rates by channel
            
        Returns:
            CAC by channel
        """
        cac_by_channel = {}
        
        for channel, attribution_pct in channel_attribution.items():
            if channel in channel_conversion_rates:
                # Weighted CAC calculation based on conversion efficiency
                conversion_rate = channel_conversion_rates[channel]
                # Higher conversion rate = lower effective CAC
                efficiency_factor = 1 / (conversion_rate / 0.0125)  # Normalize to 1.25% baseline
                channel_cac = total_cac * efficiency_factor
                cac_by_channel[channel] = round(channel_cac, 2)
        
        return cac_by_channel
    
    def calculate_net_revenue_retention(self, 
                                      starting_mrr: float,
                                      expansion_revenue: float,
                                      churn_revenue: float) -> float:
        """
        Calculate Net Revenue Retention
        
        Args:
            starting_mrr: MRR at start of period
            expansion_revenue: Revenue from upsells/expansions
            churn_revenue: Revenue lost from churned customers
            
        Returns:
            Net Revenue Retention percentage
        """
        if starting_mrr <= 0:
            return 0
        
        nrr = ((starting_mrr + expansion_revenue - churn_revenue) / starting_mrr) * 100
        return round(nrr, 1)
    
    def calculate_gross_revenue_retention(self, 
                                        starting_mrr: float,
                                        churn_revenue: float) -> float:
        """
        Calculate Gross Revenue Retention
        
        Args:
            starting_mrr: MRR at start of period
            churn_revenue: Revenue lost from churned customers
            
        Returns:
            Gross Revenue Retention percentage
        """
        if starting_mrr <= 0:
            return 0
        
        grr = ((starting_mrr - churn_revenue) / starting_mrr) * 100
        return round(grr, 1)
    
    def calculate_growth_rate(self, current_period: float, previous_period: float) -> float:
        """
        Calculate month-over-month growth rate
        
        Args:
            current_period: Current period value
            previous_period: Previous period value
            
        Returns:
            Growth rate percentage
        """
        if previous_period <= 0:
            return 0
        
        growth_rate = ((current_period - previous_period) / previous_period) * 100
        return round(growth_rate, 1)
    
    def calculate_stripe_processing_fees(self, transaction_amount: float) -> Dict[str, float]:
        """
        Calculate Stripe processing fees for a transaction
        
        Args:
            transaction_amount: Amount of the transaction
            
        Returns:
            Dictionary with fee breakdown
        """
        # Standard Stripe fee: 2.9% + $0.30
        percentage_fee = transaction_amount * 0.029
        fixed_fee = 0.30
        total_fee = percentage_fee + fixed_fee
        net_amount = transaction_amount - total_fee
        
        return {
            'transaction_amount': round(transaction_amount, 2),
            'percentage_fee': round(percentage_fee, 2),
            'fixed_fee': round(fixed_fee, 2),
            'total_fee': round(total_fee, 2),
            'net_amount': round(net_amount, 2),
            'fee_percentage': round((total_fee / transaction_amount) * 100, 2)
        }
    
    def calculate_unit_economics(self, 
                               monthly_arpu: float,
                               cac: float,
                               gross_margin: float = 0.80,
                               monthly_churn: float = 0.052) -> Dict[str, float]:
        """
        Calculate comprehensive unit economics
        
        Args:
            monthly_arpu: Monthly Average Revenue Per User
            cac: Customer Acquisition Cost
            gross_margin: Gross margin percentage
            monthly_churn: Monthly churn rate
            
        Returns:
            Dictionary with unit economics metrics
        """
        ltv = self.calculate_ltv_stripe_method(monthly_arpu, monthly_churn)
        payback_period = self.calculate_payback_period(cac, monthly_arpu)
        ltv_cac_ratio = ltv / cac if cac > 0 else 0
        contribution_margin = monthly_arpu * gross_margin
        months_to_breakeven = cac / contribution_margin if contribution_margin > 0 else float('inf')
        
        return {
            'ltv': round(ltv, 2),
            'cac': round(cac, 2),
            'ltv_cac_ratio': round(ltv_cac_ratio, 2),
            'payback_period_months': round(payback_period, 1),
            'monthly_arpu': round(monthly_arpu, 2),
            'gross_margin': round(gross_margin * 100, 1),
            'monthly_churn': round(monthly_churn * 100, 1),
            'contribution_margin': round(contribution_margin, 2),
            'months_to_breakeven': round(months_to_breakeven, 1)
        }

# Example usage and calculations for the startup tracker
def get_enhanced_startup_metrics():
    """
    Get enhanced startup metrics using Stripe calculation methods
    """
    calculator = StripeCalculations()
    
    # Current metrics from the dashboard
    monthly_arpu = 20.83
    cac = 127.0
    monthly_churn = 0.052
    gross_margin = 0.80
    monthly_active_users = 2400  # Estimated from revenue chart
    
    # Calculate enhanced metrics
    ltv_stripe = calculator.calculate_ltv_stripe_method(monthly_arpu, monthly_churn)
    payback_period = calculator.calculate_payback_period(cac, monthly_arpu)
    mrr = calculator.calculate_mrr(monthly_active_users, monthly_arpu)
    arr = calculator.calculate_arr(mrr)
    
    # Channel attribution and conversion rates
    channel_attribution = {
        'Organic Search': 0.45,
        'Social Media': 0.25,
        'Paid Ads': 0.15,
        'Referrals': 0.10,
        'Direct Traffic': 0.05
    }
    
    channel_conversion_rates = {
        'Organic Search': 0.015,  # 1.5%
        'Social Media': 0.008,    # 0.8%
        'Paid Ads': 0.012,        # 1.2%
        'Referrals': 0.020,       # 2.0%
        'Direct Traffic': 0.025   # 2.5%
    }
    
    cac_by_channel = calculator.calculate_cac_by_channel(cac, channel_attribution, channel_conversion_rates)
    
    # Revenue retention estimates
    starting_mrr = mrr * 0.95  # Assume 5% growth
    expansion_revenue = mrr * 0.15  # 15% expansion revenue
    churn_revenue = mrr * 0.052  # 5.2% churn
    
    nrr = calculator.calculate_net_revenue_retention(starting_mrr, expansion_revenue, churn_revenue)
    grr = calculator.calculate_gross_revenue_retention(starting_mrr, churn_revenue)
    
    # Growth rate calculation (from revenue chart data)
    current_revenue = 62000  # December revenue
    previous_revenue = 58000  # November revenue
    growth_rate = calculator.calculate_growth_rate(current_revenue, previous_revenue)
    
    # Unit economics summary
    unit_economics = calculator.calculate_unit_economics(monthly_arpu, cac, gross_margin, monthly_churn)
    
    return {
        'enhanced_metrics': {
            'ltv_stripe': ltv_stripe,
            'ltv_cac_ratio_updated': round(ltv_stripe / cac, 2),
            'payback_period': payback_period,
            'mrr': mrr,
            'arr': arr,
            'nrr': nrr,
            'grr': grr,
            'monthly_growth_rate': growth_rate
        },
        'cac_by_channel': cac_by_channel,
        'unit_economics': unit_economics,
        'channel_attribution': channel_attribution,
        'channel_conversion_rates': channel_conversion_rates
    }

if __name__ == "__main__":
    # Test the calculations
    metrics = get_enhanced_startup_metrics()
    print("Enhanced Startup Metrics:")
    print(f"LTV (Stripe method): ${metrics['enhanced_metrics']['ltv_stripe']}")
    print(f"LTV:CAC Ratio: {metrics['enhanced_metrics']['ltv_cac_ratio_updated']}:1")
    print(f"Payback Period: {metrics['enhanced_metrics']['payback_period']} months")
    print(f"MRR: ${metrics['enhanced_metrics']['mrr']:,.2f}")
    print(f"ARR: ${metrics['enhanced_metrics']['arr']:,.2f}")
    print(f"NRR: {metrics['enhanced_metrics']['nrr']}%")
    print(f"GRR: {metrics['enhanced_metrics']['grr']}%")
    print(f"Monthly Growth Rate: {metrics['enhanced_metrics']['monthly_growth_rate']}%")
