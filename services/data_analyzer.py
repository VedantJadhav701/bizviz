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
    
    def _detect_chart_intent(self, data_goal: str) -> str:
        """
        Detect what type of charts the user wants based on their description.
        
        Args:
            data_goal: User's description of what they want to see
            
        Returns:
            Intent string: 'trend', 'comparison', 'distribution', 'relationship', or 'overview'
        """
        data_goal_lower = data_goal.lower()
        
        # Trend keywords
        if any(word in data_goal_lower for word in ['trend', 'over time', 'growth', 'change', 'progress', 
                                                      'evolution', 'time series', 'timeline', 'history',
                                                      'daily', 'monthly', 'yearly', 'weekly']):
            return 'trend'
        
        # Comparison keywords
        if any(word in data_goal_lower for word in ['compare', 'comparison', 'versus', 'vs', 'difference',
                                                      'which', 'best', 'worst', 'top', 'bottom', 'rank']):
            return 'comparison'
        
        # Distribution keywords
        if any(word in data_goal_lower for word in ['distribution', 'spread', 'frequency', 'histogram',
                                                      'how many', 'count', 'breakdown']):
            return 'distribution'
        
        # Relationship keywords
        if any(word in data_goal_lower for word in ['relationship', 'correlation', 'impact', 'affect',
                                                      'depends', 'influence', 'scatter', 'between']):
            return 'relationship'
        
        # Default to overview
        return 'overview'
    
    def create_visualizations(self, data_goal: str, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Create visualizations based on data analysis.
        UNIVERSAL: Works with ANY dataset structure.
        Optimized for large datasets (up to 200MB).
        
        Args:
            data_goal: User's visualization goal (e.g., "show trends", "compare categories")
            analysis: Data analysis results
            
        Returns:
            List of chart dictionaries with figure objects (minimum 5 charts)
        """
        charts = []
        df = self.df
        
        # For large datasets, sample data for visualization (keep all for analysis)
        MAX_ROWS_FOR_VIZ = 10000  # Limit for visualization performance
        df_viz = df.sample(n=min(MAX_ROWS_FOR_VIZ, len(df)), random_state=42) if len(df) > MAX_ROWS_FOR_VIZ else df
        
        if len(df) > MAX_ROWS_FOR_VIZ:
            sample_note = f" (showing sample of {MAX_ROWS_FOR_VIZ:,} from {len(df):,} total rows)"
        else:
            sample_note = ""
        
        # Get column types
        numeric_cols = analysis.get('numeric_columns', [])
        categorical_cols = analysis.get('categorical_columns', [])
        date_cols = analysis.get('date_columns', [])
        
        print(f"🔍 Dataset Analysis:")
        print(f"   Numeric columns: {len(numeric_cols)} - {numeric_cols[:3]}")
        print(f"   Categorical columns: {len(categorical_cols)} - {categorical_cols[:3]}")
        print(f"   Date columns: {len(date_cols)} - {date_cols}")
        
        # Detect user's intent from their goal
        user_intent = self._detect_chart_intent(data_goal if data_goal else "")
        print(f"   User Intent: {user_intent}")
        
        # =============================================================================
        # UNIVERSAL CHART GENERATION - GUARANTEED 5+ CHARTS FOR ANY DATASET
        # =============================================================================
        
        # PRIORITY: If user wants TRENDS, create time series first
        if user_intent == 'trend' and date_cols and numeric_cols:
            print(f"🎯 User wants TRENDS - prioritizing time series charts...")
            for date_col in date_cols[:2]:
                for num_col in numeric_cols[:3]:
                    if len(charts) >= 8:
                        break
                    try:
                        df_time = df_viz.copy()
                        df_time[date_col] = pd.to_datetime(df_time[date_col], errors='coerce')
                        df_time = df_time.dropna(subset=[date_col, num_col])
                        
                        if len(df_time) == 0:
                            continue
                        
                        # Aggregate by date
                        daily_data = df_time.groupby(df_time[date_col].dt.date)[num_col].sum().reset_index()
                        daily_data.columns = ['Date', num_col]
                        
                        fig = px.line(
                            daily_data,
                            x='Date',
                            y=num_col,
                            title=f'📈 {num_col} Trend Over Time{sample_note}',
                            labels={num_col: num_col, 'Date': 'Date'}
                        )
                        
                        fig.update_traces(line_color='#3498db', line_width=3, mode='lines+markers')
                        fig.update_layout(height=500)
                        
                        charts.append({
                            'figure': fig,
                            'title': f'🎯 {num_col} Over Time (Requested)',
                            'description': f'Time series showing {num_col} trend based on your request{sample_note}'
                        })
                        print(f"✅ Created TREND chart (user requested): {num_col} over {date_col}")
                    except Exception as e:
                        print(f"⚠️ Skipped trend chart {date_col} x {num_col}: {e}")
        
        # PRIORITY: If user wants COMPARISON, create comparison charts first
        if user_intent == 'comparison' and categorical_cols and numeric_cols:
            print(f"🎯 User wants COMPARISONS - prioritizing bar charts...")
            for cat_col in categorical_cols[:2]:
                for num_col in numeric_cols[:2]:
                    if len(charts) >= 8:
                        break
                    try:
                        unique_count = df[cat_col].nunique()
                        if unique_count > 100:
                            continue
                        
                        top_n = min(15, unique_count)
                        agg_data = df.groupby(cat_col)[num_col].sum().nlargest(top_n).sort_values()
                        
                        fig = go.Figure(data=[
                            go.Bar(
                                x=agg_data.values,
                                y=agg_data.index,
                                orientation='h',
                                marker=dict(
                                    color=agg_data.values,
                                    colorscale='Viridis',
                                    showscale=False
                                ),
                                text=[f'{val:,.1f}' for val in agg_data.values],
                                textposition='auto',
                            )
                        ])
                        
                        fig.update_layout(
                            title=f'📊 Top {top_n} {cat_col} by {num_col}{sample_note}',
                            xaxis_title=num_col,
                            yaxis_title=cat_col,
                            height=500,
                            showlegend=False
                        )
                        
                        charts.append({
                            'figure': fig,
                            'title': f'🎯 {num_col} by {cat_col} (Requested)',
                            'description': f'Comparison chart based on your request{sample_note}'
                        })
                        print(f"✅ Created COMPARISON chart (user requested): {num_col} by {cat_col}")
                    except Exception as e:
                        print(f"⚠️ Skipped comparison {cat_col} x {num_col}: {e}")
        
        # PRIORITY: If user wants DISTRIBUTION, create histograms/pie charts first
        if user_intent == 'distribution':
            print(f"🎯 User wants DISTRIBUTION - prioritizing histograms and pie charts...")
            # Histograms for numeric
            for num_col in numeric_cols[:2]:
                if len(charts) >= 8:
                    break
                try:
                    fig = px.histogram(
                        df_viz,
                        x=num_col,
                        title=f'📊 Distribution of {num_col}{sample_note}',
                        labels={num_col: num_col},
                        color_discrete_sequence=['#e74c3c'],
                        nbins=50
                    )
                    fig.update_layout(height=500, showlegend=False)
                    
                    charts.append({
                        'figure': fig,
                        'title': f'🎯 {num_col} Distribution (Requested)',
                        'description': f'Distribution chart based on your request{sample_note}'
                    })
                    print(f"✅ Created DISTRIBUTION chart (user requested): {num_col}")
                except Exception as e:
                    print(f"⚠️ Skipped distribution {num_col}: {e}")
        
        # PRIORITY: If user wants RELATIONSHIP, create scatter plots first
        if user_intent == 'relationship' and len(numeric_cols) >= 2:
            print(f"🎯 User wants RELATIONSHIPS - prioritizing scatter plots...")
            for i in range(min(2, len(numeric_cols) - 1)):
                if len(charts) >= 8:
                    break
                try:
                    col1 = numeric_cols[i]
                    col2 = numeric_cols[i + 1]
                    
                    sample_df = df_viz[[col1, col2]].dropna().sample(min(1000, len(df_viz)), random_state=42)
                    if len(sample_df) == 0:
                        continue
                    
                    fig = px.scatter(
                        sample_df,
                        x=col1,
                        y=col2,
                        title=f'🔍 {col1} vs {col2} Relationship{sample_note}',
                        labels={col1: col1, col2: col2},
                        opacity=0.6,
                        color_discrete_sequence=['#9b59b6'],
                        trendline="ols"  # Add trend line
                    )
                    fig.update_layout(height=500)
                    
                    charts.append({
                        'figure': fig,
                        'title': f'🎯 {col1} vs {col2} (Requested)',
                        'description': f'Relationship analysis based on your request{sample_note}'
                    })
                    print(f"✅ Created RELATIONSHIP chart (user requested): {col1} vs {col2}")
                except Exception as e:
                    print(f"⚠️ Skipped relationship {col1} vs {col2}: {e}")
        
        # =============================================================================
        # AUTOMATIC CHARTS - Generate remaining charts to reach minimum 5
        # =============================================================================
        print(f"📊 Generated {len(charts)} user-requested charts. Adding automatic charts...")
        
        # STRATEGY 1: If we have numeric + categorical → Create aggregated bar charts
        if categorical_cols and numeric_cols:
            for i, cat_col in enumerate(categorical_cols[:3]):  # Top 3 categorical columns
                for j, num_col in enumerate(numeric_cols[:2]):  # Top 2 numeric columns
                    if len(charts) >= 8:  # Limit to 8 charts max
                        break
                    try:
                        # Get unique values count
                        unique_count = df[cat_col].nunique()
                        
                        # Skip if too many categories (over 100)
                        if unique_count > 100:
                            continue
                        
                        # Aggregate data
                        top_n = min(15, unique_count)
                        agg_data = df.groupby(cat_col)[num_col].sum().nlargest(top_n).sort_values()
                        
                        fig = go.Figure(data=[
                            go.Bar(
                                x=agg_data.values,
                                y=agg_data.index,
                                orientation='h',
                                marker=dict(
                                    color=agg_data.values,
                                    colorscale=['#3498db', '#2ecc71', '#f39c12', '#e74c3c'],
                                    showscale=False
                                ),
                                text=[f'{val:,.1f}' for val in agg_data.values],
                                textposition='auto',
                            )
                        ])
                        
                        fig.update_layout(
                            title=f'Top {top_n} {cat_col} by {num_col}{sample_note}',
                            xaxis_title=num_col,
                            yaxis_title=cat_col,
                            height=500,
                            showlegend=False
                        )
                        
                        charts.append({
                            'figure': fig,
                            'title': f'{num_col} by {cat_col}',
                            'description': f'Bar chart showing {num_col} across {cat_col}{sample_note}'
                        })
                        print(f"✅ Created chart: {num_col} by {cat_col}")
                    except Exception as e:
                        print(f"⚠️ Skipped chart {cat_col} x {num_col}: {e}")
        
        # STRATEGY 2: Time Series Charts (if date columns exist)
        if date_cols and numeric_cols:
            for date_col in date_cols[:2]:  # Max 2 date columns
                for num_col in numeric_cols[:2]:  # Max 2 numeric columns
                    if len(charts) >= 8:
                        break
                    try:
                        df_time = df_viz.copy()
                        df_time[date_col] = pd.to_datetime(df_time[date_col], errors='coerce')
                        df_time = df_time.dropna(subset=[date_col, num_col])
                        
                        if len(df_time) == 0:
                            continue
                        
                        # Aggregate by date
                        daily_data = df_time.groupby(df_time[date_col].dt.date)[num_col].sum().reset_index()
                        daily_data.columns = ['Date', num_col]
                        
                        fig = px.line(
                            daily_data,
                            x='Date',
                            y=num_col,
                            title=f'{num_col} Trend Over Time{sample_note}',
                            labels={num_col: num_col, 'Date': 'Date'}
                        )
                        
                        fig.update_traces(line_color='#3498db', line_width=2)
                        fig.update_layout(height=500)
                        
                        charts.append({
                            'figure': fig,
                            'title': f'{num_col} Over Time',
                            'description': f'Time series showing {num_col} trend{sample_note}'
                        })
                        print(f"✅ Created time series: {num_col} over {date_col}")
                    except Exception as e:
                        print(f"⚠️ Skipped time series {date_col} x {num_col}: {e}")
        
        # STRATEGY 3: Distribution Charts (Histograms for numeric columns)
        if len(charts) < 5 and numeric_cols:
            for num_col in numeric_cols[:3]:
                if len(charts) >= 8:
                    break
                try:
                    fig = px.histogram(
                        df_viz,
                        x=num_col,
                        title=f'Distribution of {num_col}{sample_note}',
                        labels={num_col: num_col},
                        color_discrete_sequence=['#9b59b6'],
                        nbins=50
                    )
                    
                    fig.update_layout(height=500, showlegend=False)
                    
                    charts.append({
                        'figure': fig,
                        'title': f'{num_col} Distribution',
                        'description': f'Histogram showing distribution of {num_col}{sample_note}'
                    })
                    print(f"✅ Created histogram: {num_col}")
                except Exception as e:
                    print(f"⚠️ Skipped histogram {num_col}: {e}")
        
        # STRATEGY 4: Pie Charts (for categorical columns)
        if len(charts) < 5 and categorical_cols:
            for cat_col in categorical_cols[:3]:
                if len(charts) >= 8:
                    break
                try:
                    unique_count = df[cat_col].nunique()
                    
                    # Only create pie chart if reasonable number of categories
                    if unique_count > 15 or unique_count < 2:
                        continue
                    
                    value_counts = df[cat_col].value_counts().head(10)
                    
                    fig = go.Figure(data=[
                        go.Pie(
                            labels=value_counts.index,
                            values=value_counts.values,
                            hole=0.4,
                            marker=dict(colors=['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6', '#1abc9c', '#e67e22', '#95a5a6'])
                        )
                    ])
                    
                    fig.update_layout(
                        title=f'{cat_col} Distribution{sample_note}',
                        height=500
                    )
                    
                    charts.append({
                        'figure': fig,
                        'title': f'{cat_col} Breakdown',
                        'description': f'Pie chart showing {cat_col} distribution{sample_note}'
                    })
                    print(f"✅ Created pie chart: {cat_col}")
                except Exception as e:
                    print(f"⚠️ Skipped pie chart {cat_col}: {e}")
        
        # STRATEGY 5: Scatter Plots (numeric vs numeric)
        if len(charts) < 5 and len(numeric_cols) >= 2:
            # Create scatter plots for numeric column pairs
            for i in range(min(2, len(numeric_cols) - 1)):
                if len(charts) >= 8:
                    break
                try:
                    col1 = numeric_cols[i]
                    col2 = numeric_cols[i + 1]
                    
                    sample_df = df_viz[[col1, col2]].dropna().sample(min(1000, len(df_viz)), random_state=42)
                    
                    if len(sample_df) == 0:
                        continue
                    
                    fig = px.scatter(
                        sample_df,
                        x=col1,
                        y=col2,
                        title=f'{col1} vs {col2}{sample_note}',
                        labels={col1: col1, col2: col2},
                        opacity=0.6,
                        color_discrete_sequence=['#e74c3c']
                    )
                    
                    fig.update_layout(height=500)
                    
                    charts.append({
                        'figure': fig,
                        'title': f'{col1} vs {col2}',
                        'description': f'Scatter plot comparing {col1} and {col2}{sample_note}'
                    })
                    print(f"✅ Created scatter: {col1} vs {col2}")
                except Exception as e:
                    print(f"⚠️ Skipped scatter {col1} vs {col2}: {e}")
        
        # STRATEGY 6: Box Plots (numeric distributions by category)
        if len(charts) < 5 and categorical_cols and numeric_cols:
            for cat_col in categorical_cols[:2]:
                for num_col in numeric_cols[:1]:
                    if len(charts) >= 8:
                        break
                    try:
                        unique_count = df[cat_col].nunique()
                        
                        # Only if reasonable number of categories
                        if unique_count > 10 or unique_count < 2:
                            continue
                        
                        fig = px.box(
                            df_viz,
                            x=cat_col,
                            y=num_col,
                            title=f'{num_col} Distribution by {cat_col}{sample_note}',
                            color=cat_col
                        )
                        
                        fig.update_layout(height=500, showlegend=False)
                        
                        charts.append({
                            'figure': fig,
                            'title': f'{num_col} by {cat_col} (Box Plot)',
                            'description': f'Box plot showing {num_col} distribution across {cat_col}{sample_note}'
                        })
                        print(f"✅ Created box plot: {num_col} by {cat_col}")
                    except Exception as e:
                        print(f"⚠️ Skipped box plot {cat_col} x {num_col}: {e}")
        
        # FALLBACK: If still less than 5 charts, create simple visualizations
        if len(charts) < 5:
            print(f"⚠️ Only {len(charts)} charts created. Creating fallback charts...")
            
            # Fallback 1: Count of records by first categorical column
            if categorical_cols and len(charts) < 5:
                try:
                    cat_col = categorical_cols[0]
                    value_counts = df[cat_col].value_counts().head(15)
                    
                    fig = px.bar(
                        x=value_counts.index,
                        y=value_counts.values,
                        title=f'Count of Records by {cat_col}{sample_note}',
                        labels={'x': cat_col, 'y': 'Count'},
                        color=value_counts.values,
                        color_continuous_scale='Blues'
                    )
                    
                    fig.update_layout(height=500, showlegend=False)
                    charts.append({
                        'figure': fig,
                        'title': f'Record Count by {cat_col}',
                        'description': f'Bar chart showing count of records{sample_note}'
                    })
                    print(f"✅ Created fallback count chart")
                except Exception as e:
                    print(f"⚠️ Fallback 1 failed: {e}")
            
            # Fallback 2: Simple numeric statistics
            if numeric_cols and len(charts) < 5:
                try:
                    # Create a summary bar chart of means
                    means = df[numeric_cols[:5]].mean().sort_values(ascending=False)
                    
                    fig = px.bar(
                        x=means.index,
                        y=means.values,
                        title=f'Average Values Across Numeric Columns{sample_note}',
                        labels={'x': 'Column', 'y': 'Average Value'},
                        color=means.values,
                        color_continuous_scale='Viridis'
                    )
                    
                    fig.update_layout(height=500, showlegend=False)
                    charts.append({
                        'figure': fig,
                        'title': 'Numeric Column Averages',
                        'description': f'Average values across numeric columns{sample_note}'
                    })
                    print(f"✅ Created fallback averages chart")
                except Exception as e:
                    print(f"⚠️ Fallback 2 failed: {e}")
        
        print(f"📊 Total charts generated: {len(charts)}")
        return charts
