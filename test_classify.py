def classify_order(amount):
    if amount > 100:
        return "High order value"
    elif 20 <= amount <= 100:
        return "Medium order value"
    else:
        return "Low order value"

def test_high_value():
    assert classify_order(150) == "High order value"

def test_medium_value():
    assert classify_order(50) == "Medium order value"

def test_low_value():
    assert classify_order(10) == "Low order value"

def test_boundary_at_100():
    assert classify_order(100) == "Medium order value"

def test_boundary_at_20():
    assert classify_order(20) == "Medium order value"