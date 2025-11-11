"""
Data Analysis and Visualization Service
Analyzes uploaded data and generates insights with visualizations.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any, Tuple
import numpy as np


class DataAnalyzer:
    """Service for analyzing data and generating insights."""
    
    def __init__(self, df: pd.DataFrame):
        """Initialize with a pandas DataFrame."""
        self.df = df
        self.insights = []
        self.charts = []
        
    def analyze_data(self) -> Dict[str, Any]:
        """
        Perform comprehensive data analysis.
        
        Returns:
            Dictionary containing analysis results
        """
        analysis = {
            'shape': self.df.shape,
            'columns': list(self.df.columns),
            'dtypes': self.df.dtypes.to_dict(),
            'missing_values': self.df.isnull().sum().to_dict(),
            'summary': self.df.describe().to_dict() if len(self.df.select_dtypes(include=[np.number]).columns) > 0 else {}
        }
        
        # Detect column types
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = self.df.select_dtypes(include=['object']).columns.tolist()
        date_cols = self.df.select_dtypes(include=['datetime64']).columns.tolist()
        
        # Try to detect date columns from object types
        for col in categorical_cols.copy():
            if 'date' in col.lower():
                try:
                    self.df[col] = pd.to_datetime(self.df[col], errors='ignore')
                    if pd.api.types.is_datetime64_any_dtype(self.df[col]):
                        date_cols.append(col)
                        categorical_cols.remove(col)
                except:
                    pass
        
        analysis['numeric_columns'] = numeric_cols
        analysis['categorical_columns'] = categorical_cols
        analysis['date_columns'] = date_cols
        
        return analysis
    
    def generate_sales_insights(self, analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Generate business insights from sales data.
        
        Args:
            analysis: Data analysis results
            
        Returns:
            List of insights with recommendations
        """
        insights = []
        df = self.df
        
        # Try to identify key columns
        revenue_cols = [col for col in df.columns if any(term in col.lower() for term in ['price', 'revenue', 'sale', 'amount'])]
        quantity_cols = [col for col in df.columns if any(term in col.lower() for term in ['quantity', 'qty', 'units'])]
        status_cols = [col for col in df.columns if any(term in col.lower() for term in ['status', 'state'])]
        category_cols = [col for col in df.columns if any(term in col.lower() for term in ['category', 'product', 'type'])]
        location_cols = [col for col in df.columns if any(term in col.lower() for term in ['location', 'zone', 'region', 'city'])]
        customer_cols = [col for col in df.columns if any(term in col.lower() for term in ['customer', 'client'])]
        
        # Insight 1: Revenue/Sales Analysis
        if revenue_cols:
            revenue_col = revenue_cols[0]
            if pd.api.types.is_numeric_dtype(df[revenue_col]):
                total_revenue = df[revenue_col].sum()
                avg_revenue = df[revenue_col].mean()
                
                insights.append({
                    'title': '💰 Revenue Performance',
                    'insight': f'Total revenue: ${total_revenue:,.2f} | Average per transaction: ${avg_revenue:,.2f}',
                    'recommendation': 'Focus on increasing average transaction value through upselling and cross-selling strategies.'
                })
        
        # Insight 2: Product Performance
        if category_cols and revenue_cols:
            category_col = category_cols[0]
            revenue_col = revenue_cols[0]
            
            if pd.api.types.is_numeric_dtype(df[revenue_col]):
                top_categories = df.groupby(category_col)[revenue_col].sum().nlargest(3)
                bottom_categories = df.groupby(category_col)[revenue_col].sum().nsmallest(3)
                
                top_cat_str = ', '.join([f"{cat} (${val:,.0f})" for cat, val in top_categories.items()])
                
                insights.append({
                    'title': '📊 Top Performing Categories',
                    'insight': f'Best sellers: {top_cat_str}',
                    'recommendation': 'Increase inventory and marketing budget for top-performing categories. Consider bundling low performers with bestsellers.'
                })
        
        # Insight 3: Return/Status Analysis
        if status_cols:
            status_col = status_cols[0]
            status_dist = df[status_col].value_counts()
            
            if 'Returned' in status_dist.index or 'Return' in status_dist.index:
                return_rate = (status_dist.get('Returned', 0) / len(df)) * 100
                
                insights.append({
                    'title': '🔄 Return Rate Analysis',
                    'insight': f'Return rate: {return_rate:.1f}% ({status_dist.get("Returned", 0)} returns)',
                    'recommendation': 'Investigate return reasons. Improve product descriptions, images, and quality control to reduce returns.'
                })
        
        # Insight 4: Geographic Performance
        if location_cols and revenue_cols:
            location_col = location_cols[0]
            revenue_col = revenue_cols[0]
            
            if pd.api.types.is_numeric_dtype(df[revenue_col]):
                location_revenue = df.groupby(location_col)[revenue_col].sum().nlargest(3)
                top_location = location_revenue.index[0]
                top_location_revenue = location_revenue.iloc[0]
                
                insights.append({
                    'title': '🗺️ Geographic Insights',
                    'insight': f'Top market: {top_location} (${top_location_revenue:,.0f})',
                    'recommendation': 'Replicate successful strategies from top-performing regions to underperforming areas. Consider targeted regional campaigns.'
                })
        
        # Insight 5: Customer Behavior
        if customer_cols:
            customer_col = [col for col in customer_cols if 'id' in col.lower()]
            if customer_col:
                unique_customers = df[customer_col[0]].nunique()
                total_orders = len(df)
                avg_orders_per_customer = total_orders / unique_customers if unique_customers > 0 else 0
                
                insights.append({
                    'title': '👥 Customer Engagement',
                    'insight': f'{unique_customers:,} unique customers | Avg {avg_orders_per_customer:.1f} orders per customer',
                    'recommendation': 'Implement loyalty programs and personalized email campaigns to increase repeat purchases and customer lifetime value.'
                })
        
        # Limit to top 5 insights
        return insights[:5]
    
    def create_visualizations(self, data_goal: str, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Create visualizations based on data goal and analysis.
        
        Args:
            data_goal: User's visualization goal
            analysis: Data analysis results
            
        Returns:
            List of plotly figure objects with metadata
        """
        charts = []
        df = self.df
        
        # Identify key columns
        revenue_cols = [col for col in df.columns if any(term in col.lower() for term in ['price', 'revenue', 'sale', 'amount'])]
        category_cols = [col for col in df.columns if any(term in col.lower() for term in ['category', 'product', 'subcategory'])]
        date_cols = analysis.get('date_columns', [])
        location_cols = [col for col in df.columns if any(term in col.lower() for term in ['location', 'zone', 'region'])]
        status_cols = [col for col in df.columns if any(term in col.lower() for term in ['status'])]
        
        # Chart 1: Revenue by Category (if available)
        if category_cols and revenue_cols:
            try:
                category_col = category_cols[0]
                revenue_col = revenue_cols[0]
                
                if pd.api.types.is_numeric_dtype(df[revenue_col]):
                    category_revenue = df.groupby(category_col)[revenue_col].sum().nlargest(10).sort_values(ascending=True)
                    
                    fig = go.Figure(data=[
                        go.Bar(
                            x=category_revenue.values,
                            y=category_revenue.index,
                            orientation='h',
                            marker=dict(
                                color=category_revenue.values,
                                colorscale='Blues',
                                showscale=False
                            ),
                            text=[f'${val:,.0f}' for val in category_revenue.values],
                            textposition='auto',
                        )
                    ])
                    
                    fig.update_layout(
                        title=f'Top 10 Categories by Revenue',
                        xaxis_title='Revenue ($)',
                        yaxis_title='Category',
                        height=500,
                        showlegend=False
                    )
                    
                    charts.append({
                        'figure': fig,
                        'title': 'Revenue by Category',
                        'description': 'Horizontal bar chart showing top performing categories'
                    })
            except Exception as e:
                pass
        
        # Chart 2: Sales Trend Over Time (if date column exists)
        if date_cols and revenue_cols:
            try:
                date_col = date_cols[0]
                revenue_col = revenue_cols[0]
                
                if pd.api.types.is_numeric_dtype(df[revenue_col]):
                    df_time = df.copy()
                    df_time[date_col] = pd.to_datetime(df_time[date_col], errors='coerce')
                    df_time = df_time.dropna(subset=[date_col])
                    
                    daily_revenue = df_time.groupby(df_time[date_col].dt.date)[revenue_col].sum().reset_index()
                    daily_revenue.columns = ['Date', 'Revenue']
                    
                    fig = px.line(
                        daily_revenue,
                        x='Date',
                        y='Revenue',
                        title='Revenue Trend Over Time',
                        labels={'Revenue': 'Revenue ($)', 'Date': 'Date'}
                    )
                    
                    fig.update_traces(line_color='#1f77b4', line_width=2)
                    fig.update_layout(height=500)
                    
                    charts.append({
                        'figure': fig,
                        'title': 'Revenue Trend',
                        'description': 'Line chart showing revenue changes over time'
                    })
            except Exception as e:
                pass
        
        # Chart 3: Order Status Distribution
        if status_cols:
            try:
                status_col = status_cols[0]
                status_dist = df[status_col].value_counts()
                
                fig = go.Figure(data=[
                    go.Pie(
                        labels=status_dist.index,
                        values=status_dist.values,
                        hole=0.4,
                        marker=dict(colors=['#2ecc71', '#e74c3c', '#3498db', '#f39c12'])
                    )
                ])
                
                fig.update_layout(
                    title='Order Status Distribution',
                    height=500
                )
                
                charts.append({
                    'figure': fig,
                    'title': 'Order Status',
                    'description': 'Donut chart showing distribution of order statuses'
                })
            except Exception as e:
                pass
        
        # Chart 4: Geographic Performance
        if location_cols and revenue_cols:
            try:
                location_col = location_cols[0]
                revenue_col = revenue_cols[0]
                
                if pd.api.types.is_numeric_dtype(df[revenue_col]):
                    location_revenue = df.groupby(location_col)[revenue_col].sum().nlargest(10).sort_values()
                    
                    fig = go.Figure(data=[
                        go.Bar(
                            x=location_revenue.values,
                            y=location_revenue.index,
                            orientation='h',
                            marker=dict(color='#3498db')
                        )
                    ])
                    
                    fig.update_layout(
                        title='Revenue by Location',
                        xaxis_title='Revenue ($)',
                        yaxis_title='Location',
                        height=500
                    )
                    
                    charts.append({
                        'figure': fig,
                        'title': 'Geographic Performance',
                        'description': 'Revenue distribution across different locations'
                    })
            except Exception as e:
                pass
        
        # Chart 5: Revenue vs Quantity Analysis
        if revenue_cols and len(revenue_cols) >= 2:
            try:
                # Try to find unit price and sale price
                unit_price_col = [col for col in revenue_cols if 'unit' in col.lower()]
                sale_price_col = [col for col in revenue_cols if 'sale' in col.lower() or 'total' in col.lower()]
                
                if unit_price_col and sale_price_col:
                    up_col = unit_price_col[0]
                    sp_col = sale_price_col[0]
                    
                    sample_df = df[[up_col, sp_col]].dropna().sample(min(1000, len(df)))
                    
                    fig = px.scatter(
                        sample_df,
                        x=up_col,
                        y=sp_col,
                        title='Unit Price vs Sale Price',
                        labels={up_col: 'Unit Price ($)', sp_col: 'Sale Price ($)'},
                        opacity=0.6
                    )
                    
                    fig.update_layout(height=500)
                    
                    charts.append({
                        'figure': fig,
                        'title': 'Price Analysis',
                        'description': 'Scatter plot showing relationship between unit price and sale price'
                    })
            except Exception as e:
                pass
        
        return charts
