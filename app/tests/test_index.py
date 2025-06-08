import pytest
import pandas as pd
import index

def test_health_check_success():
    response = index.health_check()
    assert isinstance(response, dict)
    assert "status" in response
    assert response["status"] == "healthy"
    assert "message" in response

def test_generate_sample_data_default():
    df = index.generate_sample_data()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert set(['Date', 'Metric', 'Value']).issubset(df.columns)
    assert df['Value'].between(0, 100).all()

def test_generate_sample_data_custom_days():
    days = 10
    df = index.generate_sample_data(days=days)
    # There are 4 metrics per day
    expected_rows = (days + 1) * 4
    assert len(df) == expected_rows

def test_generate_sample_data_metrics():
    df = index.generate_sample_data(1)
    metrics = set(df['Metric'].unique())
    expected_metrics = set(['CPU Usage', 'Memory Usage', 'Network Traffic', 'Disk Usage'])
    assert metrics == expected_metrics

def test_generate_sample_data_value_range():
    df = index.generate_sample_data(5)
    assert df['Value'].min() >= 0
    assert df['Value'].max() <= 100