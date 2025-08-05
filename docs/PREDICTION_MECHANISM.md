# 🔮 CƠ CHẾ DỰ ĐOÁN USAGE VÀ SAVINGS

## 💰 **POTENTIAL SAVINGS CALCULATION**

### **Công Thức Cơ Bản**
```python
potential_savings = (current_licenses - recommended_licenses) × cost_per_license
```

### **Ví Dụ Chi Tiết**
```python
# Adobe Creative Suite Case
current_licenses = 50
used_licenses = 8
cost_per_license = $52.99
usage_rate = 8/50 = 16%

# Rule: REDUCE_SIGNIFICANTLY (usage < 20%)
recommended_licenses = max(1, 8 × 1.2) = 10

# Savings Calculation
monthly_savings = (50 - 10) × $52.99 = $2,119.60
annual_savings = $2,119.60 × 12 = $25,435.20
savings_percentage = (40/50) × 100% = 80%
```

### **Multiple Scenarios**
```python
scenarios = {
    'conservative': used_licenses × 1.5,  # Safety-first
    'moderate': used_licenses × 1.3,      # Balanced
    'aggressive': used_licenses × 1.1     # Maximum savings
}
```

## 🔮 **USAGE PREDICTION MECHANISM**

### **1. Simple Prediction (Hiện tại)**
```python
def simple_predict(usage_rate):
    if usage_rate < 0.3:
        return {'trend': 'decreasing', 'change': -5}
    elif usage_rate > 0.8:
        return {'trend': 'increasing', 'change': +10}
    else:
        return {'trend': 'stable', 'change': +2}
```

### **2. Advanced Prediction (Weighted Factors)**
```python
def advanced_predict(license_data):
    factors = {
        'usage_trend': analyze_usage_trend(usage_rate),
        'cost_pressure': analyze_cost_pressure(cost, usage_rate),
        'expiry_impact': analyze_expiry_impact(days_to_expiry),
        'license_type': analyze_license_type(type),
        'seasonal': analyze_seasonal_pattern(month, industry)
    }
    
    weights = {
        'usage_trend': 0.4,
        'cost_pressure': 0.15,
        'expiry_impact': 0.15,
        'license_type': 0.1,
        'seasonal': 0.2
    }
    
    total_change = sum(factors[f] × weights[f] for f in factors)
    predicted_usage = current_usage + total_change
    
    return predicted_usage
```

## 📊 **FACTOR ANALYSIS DETAILS**

### **1. Usage Trend Factor (Weight: 40%)**
```python
def analyze_usage_trend(usage_rate):
    if usage_rate < 0.2:
        return -8    # Strong decrease tendency
    elif usage_rate < 0.4:
        return -3    # Moderate decrease
    elif usage_rate > 0.9:
        return +12   # Strong increase needed
    elif usage_rate > 0.8:
        return +5    # Moderate increase
    else:
        return +1    # Stable with slight growth
```

**Logic:**
- **Very Low Usage (<20%)**: Xu hướng giảm mạnh do tối ưu hóa
- **Low Usage (20-40%)**: Xu hướng giảm nhẹ
- **High Usage (80-90%)**: Xu hướng tăng để tránh thiếu
- **Very High Usage (>90%)**: Xu hướng tăng mạnh
- **Normal Usage (40-80%)**: Ổn định với tăng trưởng nhẹ

### **2. Cost Pressure Factor (Weight: 15%)**
```python
def analyze_cost_pressure(cost_per_license, usage_rate):
    if cost_per_license > 100 and usage_rate < 0.5:
        return -10   # High cost + low usage = strong reduction
    elif cost_per_license > 50 and usage_rate < 0.3:
        return -5    # Moderate pressure
    elif cost_per_license < 20:
        return +2    # Low cost = less optimization pressure
    else:
        return 0     # Neutral
```

**Logic:**
- **Expensive + Low Usage**: Áp lực giảm mạnh
- **Moderate Cost + Very Low Usage**: Áp lực giảm nhẹ
- **Cheap License**: Ít áp lực tối ưu hóa
- **Other Cases**: Trung tính

### **3. Expiry Impact Factor (Weight: 15%)**
```python
def analyze_expiry_impact(days_until_expiry):
    if days_until_expiry < 0:
        return -15   # Expired = strong reduction
    elif days_until_expiry <= 30:
        return +3    # Near expiry = slight increase for renewal
    elif days_until_expiry <= 90:
        return 0     # No immediate impact
    else:
        return 0     # Long term = no impact
```

**Logic:**
- **Expired**: Giảm mạnh do không còn sử dụng được
- **Near Expiry (≤30 days)**: Tăng nhẹ để chuẩn bị renewal
- **Medium Term (30-90 days)**: Không ảnh hưởng
- **Long Term (>90 days)**: Không ảnh hưởng

### **4. License Type Factor (Weight: 10%)**
```python
def analyze_license_type(license_type):
    type_trends = {
        'SUBSCRIPTION': +2,    # Tend to grow with business
        'CONCURRENT': 0,       # Stable usage pattern
        'PERPETUAL': -1,       # Tend to optimize over time
        'NAMED_USER': +1       # Moderate growth
    }
    return type_trends.get(license_type, 0)
```

**Logic:**
- **SUBSCRIPTION**: Xu hướng tăng theo business growth
- **CONCURRENT**: Ổn định, ít biến động
- **PERPETUAL**: Xu hướng tối ưu hóa theo thời gian
- **NAMED_USER**: Tăng trưởng vừa phải

### **5. Seasonal Factor (Weight: 20%)**
```python
def analyze_seasonal_pattern(current_month, industry_type):
    # Ví dụ cho software design
    if industry_type == 'DESIGN':
        peak_months = [9, 10, 11, 12]  # Q4 busy season
        if current_month in peak_months:
            return +5    # Increase during peak
        else:
            return -2    # Decrease during off-peak
    
    # Default pattern
    return 0
```

## 🎯 **CONFIDENCE CALCULATION**

### **Confidence Score Formula**
```python
def calculate_confidence(license_data):
    base_confidence = 0.3
    
    # Usage stability (25% max)
    usage_rate = get_usage_rate(license_data)
    if 0.2 <= usage_rate <= 0.9:
        base_confidence += 0.25
    elif usage_rate < 0.1 or usage_rate > 0.95:
        base_confidence += 0.35  # Extreme values more predictable
    
    # License type predictability (20% max)
    license_type = license_data.get('license_type')
    type_confidence = {
        'SUBSCRIPTION': 0.2,   # Most predictable
        'CONCURRENT': 0.15,    # Moderate
        'PERPETUAL': 0.1       # Least predictable
    }
    base_confidence += type_confidence.get(license_type, 0.1)
    
    # Cost factor (15% max)
    cost = float(license_data.get('cost_per_license', 0))
    if cost > 100:
        base_confidence += 0.15
    elif cost > 50:
        base_confidence += 0.1
    else:
        base_confidence += 0.05
    
    # Expiry proximity (25% max)
    days_to_expiry = get_days_to_expiry(license_data)
    if 0 <= days_to_expiry <= 30:
        base_confidence += 0.2
    elif days_to_expiry < 0:
        base_confidence += 0.25
    else:
        base_confidence += 0.05
    
    return min(1.0, base_confidence)
```

## 📈 **PREDICTION ACCURACY FACTORS**

### **High Accuracy Scenarios (Confidence > 80%)**
1. **Extreme Usage Rates** (<10% or >95%)
2. **Near Expiry** (≤30 days)
3. **High Cost + Low Usage** (Predictable optimization)
4. **Subscription Licenses** (Regular patterns)

### **Medium Accuracy Scenarios (Confidence 50-80%)**
1. **Normal Usage Rates** (20-80%)
2. **Medium-term Expiry** (30-90 days)
3. **Moderate Cost Licenses**
4. **Concurrent Licenses**

### **Low Accuracy Scenarios (Confidence <50%)**
1. **New Licenses** (No historical data)
2. **Perpetual Licenses** (Unpredictable patterns)
3. **Invalid/Missing Data**
4. **Unusual Business Contexts**

## 🔄 **CONTINUOUS IMPROVEMENT**

### **Feedback Loop**
```python
def update_prediction_accuracy():
    # Compare predicted vs actual usage
    accuracy_rate = calculate_accuracy(predictions, actuals)
    
    # Adjust weights based on performance
    if accuracy_rate < 0.7:
        adjust_factor_weights()
        retrain_models()
    
    # Update confidence calculations
    update_confidence_factors(accuracy_rate)
```

### **Model Validation**
1. **Backtesting**: Test predictions against historical data
2. **Cross-validation**: Validate across different license types
3. **A/B Testing**: Compare different prediction methods
4. **User Feedback**: Incorporate business user insights