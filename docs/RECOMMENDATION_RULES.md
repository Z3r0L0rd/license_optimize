# 📋 QUY TẮC RECOMMEND SỐ LICENSE/USER

## 🎯 **QUY TẮC CƠ BẢN**

### **1. REDUCE_SIGNIFICANTLY (Usage < 20%)**
```
Điều kiện: usage_rate < 0.2
Công thức: recommended = max(1, used_licenses * 1.2)
Buffer: 20%
Priority: HIGH
Lý do: Lãng phí nghiêm trọng
```

**Ví dụ:**
- Current: 100 licenses, 15 used (15%)
- Recommended: 18 licenses
- Savings: 82 licenses × $cost = tiết kiệm lớn

### **2. REDUCE_MODERATELY (Usage 20-50%)**
```
Điều kiện: 0.2 ≤ usage_rate < 0.5
Công thức: recommended = max(1, used_licenses * 1.5)
Buffer: 50%
Priority: MEDIUM
Lý do: Có thể tối ưu hóa
```

**Ví dụ:**
- Current: 100 licenses, 40 used (40%)
- Recommended: 60 licenses
- Savings: 40 licenses × $cost

### **3. INCREASE (Usage > 90%)**
```
Điều kiện: usage_rate > 0.9
Công thức: recommended = total_licenses * 1.2
Buffer: 20%
Priority: HIGH
Lý do: Rủi ro thiếu license
```

**Ví dụ:**
- Current: 100 licenses, 95 used (95%)
- Recommended: 120 licenses
- Cost: +20 licenses × $cost

### **4. MAINTAIN (Usage 50-90%)**
```
Điều kiện: 0.5 ≤ usage_rate ≤ 0.9
Công thức: recommended = total_licenses
Buffer: Existing
Priority: LOW
Lý do: Sử dụng hợp lý
```

## 🧮 **CÔNG THỨC BUFFER**

### **Tại sao cần Buffer?**
1. **Growth Buffer**: Dự phòng cho tăng trưởng
2. **Peak Usage**: Đối phó với usage cao điểm
3. **Safety Margin**: Tránh thiếu license đột xuất
4. **Renewal Gap**: Thời gian chờ gia hạn

### **Buffer Size Logic:**
```python
def calculate_buffer(usage_rate, license_type, cost_level):
    base_buffer = 0.2  # 20% cơ bản
    
    # Điều chỉnh theo usage rate
    if usage_rate < 0.3:
        buffer = 0.2  # Thấp = buffer nhỏ
    elif usage_rate > 0.8:
        buffer = 0.3  # Cao = buffer lớn
    else:
        buffer = 0.25  # Trung bình
    
    # Điều chỉnh theo license type
    if license_type == 'CONCURRENT':
        buffer += 0.1  # Concurrent cần buffer cao hơn
    elif license_type == 'PERPETUAL':
        buffer -= 0.05  # Perpetual ít biến động
    
    # Điều chỉnh theo cost
    if cost_level == 'HIGH':
        buffer -= 0.05  # Chi phí cao = buffer thận trọng
    elif cost_level == 'LOW':
        buffer += 0.05  # Chi phí thấp = buffer rộng rãi
    
    return min(0.5, max(0.1, buffer))  # Giới hạn 10-50%
```

## 📊 **FACTORS ẢNH HƯỞNG**

### **1. License Type Impact**
```python
type_multipliers = {
    'SUBSCRIPTION': 1.0,    # Standard
    'CONCURRENT': 1.2,      # Cần buffer cao hơn
    'PERPETUAL': 0.9,       # Ít biến động
}
```

### **2. Cost Pressure Impact**
```python
def cost_adjustment(cost_per_license, usage_rate):
    if cost_per_license > 100:  # Expensive
        if usage_rate < 0.3:
            return 0.8  # Aggressive reduction
        else:
            return 0.95  # Conservative
    elif cost_per_license < 20:  # Cheap
        return 1.1  # More generous
    else:
        return 1.0  # Standard
```

### **3. Expiry Proximity Impact**
```python
def expiry_adjustment(days_until_expiry):
    if days_until_expiry < 0:
        return 0.5  # Expired = major reduction
    elif days_until_expiry <= 30:
        return 0.9  # Near expiry = slight reduction
    elif days_until_expiry <= 90:
        return 1.0  # Standard
    else:
        return 1.05  # Long term = slight increase
```

## 🎯 **BUSINESS RULES**

### **Minimum License Rules**
```python
def apply_minimum_rules(recommended, current_usage):
    # Không bao giờ recommend ít hơn usage hiện tại
    recommended = max(recommended, current_usage)
    
    # Minimum 1 license
    recommended = max(1, recommended)
    
    # Không giảm quá 50% trong 1 lần
    max_reduction = current_total * 0.5
    recommended = max(recommended, max_reduction)
    
    return int(recommended)
```

### **Maximum Change Rules**
```python
def apply_maximum_rules(recommended, current_total):
    # Không tăng quá 100% trong 1 lần
    max_increase = current_total * 2
    recommended = min(recommended, max_increase)
    
    return int(recommended)
```

## 📈 **VALIDATION RULES**

### **Sanity Checks**
1. **recommended ≥ current_usage**: Không thiếu license
2. **recommended ≥ 1**: Tối thiểu 1 license
3. **recommended ≤ current_total × 2**: Không tăng quá 100%
4. **recommended ≥ current_total × 0.5**: Không giảm quá 50%

### **Business Logic Checks**
1. **High-cost licenses**: Thận trọng hơn với recommendations
2. **Critical software**: Buffer cao hơn
3. **Seasonal software**: Xem xét chu kỳ sử dụng
4. **New licenses**: Buffer cao cho giai đoạn đầu

## 🔄 **CONTINUOUS IMPROVEMENT**

### **Feedback Loop**
1. Track recommendation accuracy
2. Monitor actual vs predicted usage
3. Adjust algorithms based on results
4. Learn from user feedback

### **A/B Testing**
1. Test different buffer sizes
2. Compare recommendation strategies
3. Measure cost savings vs risk
4. Optimize for business outcomes