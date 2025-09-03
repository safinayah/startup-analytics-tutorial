#!/usr/bin/env python3
"""
Simple verification script for the dynamic calculation system
"""

import json
import sys
import os

# Add app directory to path
sys.path.append('app')

def main():
    print("🔍 VERIFYING DYNAMIC CALCULATION SYSTEM")
    print("=" * 50)
    
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
    
    # Test 2: Metrics calculator
    print("\n2. Testing metrics calculator...")
    try:
        from services.metrics_calculator import MetricsCalculator
        calculator = MetricsCalculator()
        
        # Test key calculations
        ltv = calculator.calculate_ltv("stripe")
        print(f"   ✅ LTV: ${ltv['value']}")
        
        ratio = calculator.calculate_ltv_cac_ratio()
        print(f"   ✅ LTV:CAC: {ratio['ratio']}:1")
        
        mrr = calculator.calculate_mrr()
        print(f"   ✅ MRR: ${mrr['value']:,}")
        
        arr = calculator.calculate_arr()
        print(f"   ✅ ARR: ${arr['value']:,}")
        
    except Exception as e:
        print(f"   ❌ Calculator error: {e}")
        return False
    
    # Test 3: Flask routes
    print("\n3. Testing Flask routes...")
    try:
        from app import create_app
        app = create_app()
        
        with app.test_client() as client:
            # Test main route
            response = client.get('/')
            if response.status_code == 200:
                print("   ✅ Main route works")
            else:
                print(f"   ❌ Main route failed: {response.status_code}")
                return False
            
            # Test API route
            response = client.get('/api/metrics')
            if response.status_code == 200:
                data = response.get_json()
                if data.get('success'):
                    print("   ✅ API route works")
                    print(f"   📊 API returns {len(data['data'])} metric categories")
                else:
                    print(f"   ❌ API returned error: {data.get('error')}")
                    return False
            else:
                print(f"   ❌ API route failed: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"   ❌ Flask error: {e}")
        return False
    
    # Test 4: Calculation accuracy
    print("\n4. Verifying calculation accuracy...")
    try:
        # Verify LTV calculation
        arpu = data['core_metrics']['monthly_arpu']
        churn = data['core_metrics']['monthly_churn_rate']
        expected_ltv = arpu / churn
        
        if abs(ltv['value'] - expected_ltv) < 0.01:
            print("   ✅ LTV calculation accurate")
        else:
            print(f"   ❌ LTV calculation error: {ltv['value']} vs {expected_ltv}")
            return False
        
        # Verify MRR calculation
        active_users = data['core_metrics']['monthly_active_users']
        expected_mrr = active_users * arpu
        
        if abs(mrr['value'] - expected_mrr) < 1:
            print("   ✅ MRR calculation accurate")
        else:
            print(f"   ❌ MRR calculation error: {mrr['value']} vs {expected_mrr}")
            return False
        
        # Verify ARR calculation
        expected_arr = mrr['value'] * 12
        
        if abs(arr['value'] - expected_arr) < 1:
            print("   ✅ ARR calculation accurate")
        else:
            print(f"   ❌ ARR calculation error: {arr['value']} vs {expected_arr}")
            return False
            
    except Exception as e:
        print(f"   ❌ Accuracy check error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 ALL TESTS PASSED!")
    print("✅ System is ready for GitHub push")
    print("=" * 50)
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
