import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import random
from sklearn.preprocessing import MinMaxScaler

# Health check endpoint for ECS compatibility
def health_check():
    """Health check endpoint for ECS service"""
    return {
        "status": "healthy",
        "message": "Service is running properly"
    }

# Function to generate sample data
def generate_sample_data(days=30):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        current_date += timedelta(days=1)
    
    metrics = ['CPU Usage', 'Memory Usage', 'Network Traffic', 'Disk Usage']
    data = []
    
    for date in dates:
        for metric in metrics:
            # Generate a value with some random noise but following a trend
            base_value = 50
            if metric == 'CPU Usage':
                # CPU usage with weekly pattern and some random peaks
                day_of_week = date.weekday()
                base_value = 30 + (10 if day_of_week < 5 else 0)  # Higher during weekdays
            elif metric == 'Memory Usage':
                # Memory usage gradually increasing
                days_passed = (date - start_date).days
                base_value = 40 + (days_passed / len(dates)) * 20
            elif metric == 'Network Traffic':
                # Network traffic with daily pattern
                hour = date.hour if hasattr(date, 'hour') else 12
                base_value = 30 + (hour / 24) * 40
            
            # Add randomness
            value = base_value + random.uniform(-10, 20)
            value = max(0, min(100, value))  # Clamp between 0 and 100
            
            data.append({
                'Date': date,
                'Metric': metric,
                'Value': value
            })
    
    return pd.DataFrame(data)

# Main Streamlit app
def main():
    st.set_page_config(
        page_title="ECS Fargate Monitoring Dashboard",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("AWS ECS Fargate Monitoring Dashboard")
    st.write("This is a sample dashboard for monitoring AWS ECS Fargate services.")
    
    # Sidebar for controls
    st.sidebar.header("Dashboard Controls")
    date_range = st.sidebar.slider("Select Date Range (days)", 7, 60, 30)
    
    metrics_to_display = st.sidebar.multiselect(
        "Select Metrics to Display",
        ["CPU Usage", "Memory Usage", "Network Traffic", "Disk Usage"],
        default=["CPU Usage", "Memory Usage"]
    )
    
    # Generate sample data
    df = generate_sample_data(date_range)
    
    # Filter data based on selected metrics
    if metrics_to_display:
        df = df[df['Metric'].isin(metrics_to_display)]
    
    # Create dashboard layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Metrics Over Time")
        fig = px.line(
            df, 
            x='Date', 
            y='Value', 
            color='Metric', 
            title="Resource Utilization Over Time",
            labels={"Value": "Utilization (%)", "Date": "Date"}
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.header("Average Utilization by Metric")
        avg_df = df.groupby('Metric')['Value'].mean().reset_index()
        fig = px.bar(
            avg_df, 
            x='Metric', 
            y='Value', 
            title="Average Resource Utilization",
            labels={"Value": "Avg Utilization (%)", "Metric": "Resource Metric"}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Additional visualizations
    st.header("Detailed Metrics Analysis")
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Heatmap of daily values
        pivot_df = df.pivot_table(
            index=pd.Grouper(key='Date', freq='D'),
            columns='Metric',
            values='Value',
            aggfunc='mean'
        ).reset_index()
        
        # Convert to long format for heatmap
        heatmap_data = []
        for _, row in pivot_df.iterrows():
            date = row['Date']
            for metric in pivot_df.columns:
                if metric != 'Date':
                    heatmap_data.append({
                        'Date': date,
                        'Metric': metric,
                        'Value': row[metric]
                    })
        
        heatmap_df = pd.DataFrame(heatmap_data)
        if not heatmap_df.empty:
            fig = px.density_heatmap(
                heatmap_df,
                x='Date',
                y='Metric',
                z='Value',
                title="Daily Metric Heatmap",
                labels={"Value": "Utilization (%)"}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col4:
        # Box plot showing distribution
        fig = px.box(
            df,
            x='Metric',
            y='Value',
            title="Distribution of Metric Values",
            labels={"Value": "Utilization (%)", "Metric": "Resource Metric"}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # KPI cards
    st.header("Key Performance Indicators")
    kpi_cols = st.columns(len(metrics_to_display) if metrics_to_display else 4)
    
    for i, metric in enumerate(metrics_to_display if metrics_to_display else df['Metric'].unique()):
        metric_data = df[df['Metric'] == metric]
        avg_value = metric_data['Value'].mean()
        max_value = metric_data['Value'].max()
        
        with kpi_cols[i % len(kpi_cols)]:
            st.metric(
                label=metric,
                value=f"{avg_value:.1f}%",
                delta=f"{max_value - avg_value:.1f}% (Peak)"
            )

# Run the Streamlit app
if __name__ == "__main__":
    main()