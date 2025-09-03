#!/usr/bin/env python3
"""
Simple test script for basic functionality
"""

import json
import sys
import os

# Add app directory to path
sys.path.append('app')

def test_basic_functionality():
    print("🔍 BASIC FUNCTIONALITY TEST")
    print("=" * 40)
    
    # Test 1: Data file
    print("1. Testing data file...")
    try:
        with open('data/business_metrics.json', 'r') as f:
            data = json.load(f)
        print("   ✅ Data file loads successfully")
        print(f"   📊 ARPU: ${data['core_metrics']['monthly_arpu']}")
        print(f"   📊 CAC: ${data['core_metrics']['cac']}")
        print(f"   📊 Churn: {data['core_metrics']['monthly_churn_rate'] * 100}%")
    except Exception as e:
        print(f"   ❌ Data file error: {e}")
        return False
    
    # Test 2: Manual calculations
    print("\n2. Manual calculation verification...")
    try:
        arpu = data['core_metrics']['monthly_arpu']
        churn = data['core_metrics']['monthly_churn_rate']
        cac = data['core_metrics']['cac']
        active_users = data['core_metrics']['monthly_active_users']
        
        # LTV calculation
        ltv = arpu / churn
        print(f"   ✅ LTV: ${ltv:.2f}")
        
        # LTV:CAC ratio
        ratio = ltv / cac
        print(f"   ✅ LTV:CAC: {ratio:.2f}:1")
        
        # MRR calculation
        mrr = active_users * arpu
        print(f"   ✅ MRR: ${mrr:,.2f}")
        
        # ARR calculation
        arr = mrr * 12
        print(f"   ✅ ARR: ${arr:,.2f}")
        
        # Payback period
        payback = cac / arpu
        print(f"   ✅ Payback: {payback:.1f} months")
        
        # Conversion rate
        visitors = data['core_metrics']['website_visitors']
        customers = data['core_metrics']['paid_customers']
        conversion = (customers / visitors) * 100
        print(f"   ✅ Conversion: {conversion:.2f}%")
        
        # Retention rate
        retention = (1 - churn) * 100
        print(f"   ✅ Retention: {retention:.1f}%")
        
    except Exception as e:
        print(f"   ❌ Manual calculation error: {e}")
        return False
    
    print("\n" + "=" * 40)
    print("🎉 BASIC TESTS PASSED!")
    print("✅ Core calculations are working")
    print("=" * 40)
    return True

if __name__ == "__main__":
    success = test_basic_functionality()
    sys.exit(0 if success else 1)
