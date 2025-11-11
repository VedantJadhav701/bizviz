"""
Data Analysis and Visualization Service
Analyzes uploaded data and generates insights with visualizations.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any, Tuple
import numpy as np
import os
import json
from groq import Groq


class DataAnalyzer:
    """Service for analyzing data and generating insights."""
    
    def __init__(self, df: pd.DataFrame):
        """Initialize with a pandas DataFrame."""
        self.df = df
        self.insights = []
        self.charts = []
        self.groq_client = None
        
        # Initialize Groq client if API key is available
        try:
            api_key = os.getenv('GROQ_API_KEY')
            if api_key:
                self.groq_client = Groq(api_key=api_key)
        except Exception as e:
            print(f"⚠️ Groq API not available: {e}")
    
    def _parse_user_goal_with_ai(self, user_goal: str, available_columns: List[str]) -> Dict[str, Any]:
        """
        Use Groq AI to parse user's natural language goal and map it to actual columns.
        
        Args:
            user_goal: User's description like "effect of delivery date, zone on shipping fee"
            available_columns: List of available column names in the dataset
            
        Returns:
            Dictionary with parsed chart requirements:
            {
                'chart_type': 'bar' | 'line' | 'scatter' | 'box' | 'pie',
                'x_axis': 'column_name',
                'y_axis': 'column_name',
                'group_by': 'column_name' (optional),
                'explanation': 'Why this chart answers the question'
            }
        """
        if not self.groq_client:
            print("⚠️ Groq client not initialized")
            return None
            
        if not user_goal or len(user_goal.strip()) < 3:
            print("⚠️ User goal too short or empty")
            return None
        
        try:
            # Create a more detailed column description
            column_info = []
            for col in available_columns[:50]:  # Limit to first 50 columns
                sample_vals = self.df[col].dropna().head(3).tolist()
                col_type = str(self.df[col].dtype)
                column_info.append(f"{col} ({col_type})")
            
            prompt = f"""You are a data visualization expert. Analyze this user's request and map it to the available columns.

User Request: "{user_goal}"

Available Columns (with types):
{chr(10).join(column_info)}

Task: Parse the user's request and determine:
1. What chart type would best answer their question (bar, line, scatter, box, pie)
2. Which columns should be used for X-axis, Y-axis, and grouping
3. Brief explanation of why this chart answers their question

Important:
- For "relationship between A and B", use scatter plot with A as x_axis, B as y_axis
- For "effect of A on B", A is x_axis, B is y_axis
- Match user's terms to column names (e.g., "price" might match "Price" or "Unit Price")
- If user mentions multiple factors, use group_by for secondary factor

Respond ONLY with valid JSON in this exact format:
{{
    "chart_type": "scatter",
    "x_axis": "exact_column_name",
    "y_axis": "exact_column_name", 
    "group_by": null,
    "explanation": "Shows correlation between X and Y"
}}

Chart type options: bar, line, scatter, box, pie"""

            print(f"🤖 Sending to Groq AI: '{user_goal}'")
            
            response = self.groq_client.chat.completions.create(
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                model="llama-3.1-70b-versatile",
                temperature=0.2,
                max_tokens=500
            )
            
            result_text = response.choices[0].message.content.strip()
            print(f"🤖 AI Response: {result_text[:200]}...")
            
            # Extract JSON from response (in case there's extra text)
            if '```json' in result_text:
                result_text = result_text.split('```json')[1].split('```')[0].strip()
            elif '```' in result_text:
                result_text = result_text.split('```')[1].split('```')[0].strip()
            
            result = json.loads(result_text)
            
            # Validate column names exist (case-insensitive matching)
            def find_column(col_name):
                if not col_name:
                    return None
                # Exact match first
                if col_name in available_columns:
                    return col_name
                # Case-insensitive match
                for col in available_columns:
                    if col.lower() == col_name.lower():
                        return col
                # Partial match
                for col in available_columns:
                    if col_name.lower() in col.lower() or col.lower() in col_name.lower():
                        return col
                return None
            
            # Try to find matching columns
            x_col = find_column(result.get('x_axis'))
            y_col = find_column(result.get('y_axis'))
            group_col = find_column(result.get('group_by'))
            
            if x_col:
                result['x_axis'] = x_col
            if y_col:
                result['y_axis'] = y_col
            if group_col:
                result['group_by'] = group_col
            
            print(f"✅ AI parsed user goal: {result}")
            return result
            
        except Exception as e:
            print(f"⚠️ AI parsing failed: {e}")
            import traceback
            traceback.print_exc()
            return None
        
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
    
    def _get_color_palette_and_constraints(self, chart_type: str, user_intent: str) -> Dict[str, Any]:
        """
        Generate color palette and 3 key visual design constraints for each chart.
        
        Args:
            chart_type: Type of chart (bar, line, scatter, pie, histogram, box)
            user_intent: User's goal (trend, comparison, distribution, proportion, relationship)
            
        Returns:
            Dictionary with color_palette, color_names, and 3 design constraints
        """
        # Define color palettes based on chart type and intent
        palettes = {
            'trend_line': {
                'colors': ['#3498db', '#2980b9', '#1abc9c', '#16a085'],
                'names': ['Azure Blue', 'Royal Blue', 'Turquoise', 'Sea Green'],
                'colorscale': 'Blues'
            },
            'comparison_bar': {
                'colors': ['#e74c3c', '#c0392b', '#e67e22', '#d35400'],
                'names': ['Crimson Red', 'Deep Red', 'Tangerine', 'Burnt Orange'],
                'colorscale': 'Viridis'
            },
            'distribution_hist': {
                'colors': ['#9b59b6', '#8e44ad', '#e74c3c', '#c0392b'],
                'names': ['Amethyst Purple', 'Deep Purple', 'Crimson', 'Dark Red'],
                'colorscale': 'Purples'
            },
            'proportion_pie': {
                'colors': ['#3498db', '#e74c3c', '#f39c12', '#2ecc71', '#9b59b6', '#1abc9c'],
                'names': ['Azure', 'Crimson', 'Golden', 'Emerald', 'Amethyst', 'Turquoise'],
                'colorscale': 'Set3'
            },
            'relationship_scatter': {
                'colors': ['#2ecc71', '#27ae60', '#f39c12', '#e67e22'],
                'names': ['Emerald Green', 'Forest Green', 'Golden Yellow', 'Orange'],
                'colorscale': 'Viridis'
            },
            'default': {
                'colors': ['#3498db', '#e74c3c', '#f39c12', '#2ecc71'],
                'names': ['Azure', 'Crimson', 'Golden', 'Emerald'],
                'colorscale': 'Plotly'
            }
        }
        
        # Map chart type and intent to palette
        palette_key = f"{user_intent}_{chart_type}" if f"{user_intent}_{chart_type}" in palettes else chart_type if chart_type in palettes else 'default'
        palette = palettes.get(palette_key, palettes['default'])
        
        # Define design constraints based on chart type
        constraints = {
            'bar': {
                'color_palette': f"{', '.join(palette['names'][:3])}",
                'axis_scale': 'Linear scale with auto-range for optimal data spread',
                'labeling_focus': 'Category labels on Y-axis, value labels on bars for readability'
            },
            'line': {
                'color_palette': f"{', '.join(palette['names'][:3])}",
                'axis_scale': 'Time-based X-axis with adaptive intervals, linear Y-axis',
                'labeling_focus': 'Clear date/time labels, gridlines for trend tracking'
            },
            'scatter': {
                'color_palette': f"{', '.join(palette['names'][:3])}",
                'axis_scale': 'Proportional scales to reveal correlations and outliers',
                'labeling_focus': 'Both axes labeled with units, hover tooltips for data points'
            },
            'pie': {
                'color_palette': f"{', '.join(palette['names'][:4])}",
                'axis_scale': 'Percentage-based proportions (0-100%)',
                'labeling_focus': 'Segment labels with percentages, legend for clarity'
            },
            'histogram': {
                'color_palette': f"{', '.join(palette['names'][:2])}",
                'axis_scale': 'Binned X-axis for data ranges, frequency count on Y-axis',
                'labeling_focus': 'Range labels on bins, count labels for peak values'
            },
            'box': {
                'color_palette': f"{', '.join(palette['names'][:3])}",
                'axis_scale': 'Categorical grouping with quartile-based distribution',
                'labeling_focus': 'Category names, median/quartile markers, outlier indication'
            }
        }
        
        constraint = constraints.get(chart_type, constraints['bar'])
        
        return {
            'color_palette': palette['colors'],
            'color_names': palette['names'],
            'colorscale': palette['colorscale'],
            'design_constraints': {
                '1_color_palette': constraint['color_palette'],
                '2_axis_scale': constraint['axis_scale'],
                '3_labeling_focus': constraint['labeling_focus']
            }
        }
    
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
        
        # =============================================================================
        # AI-POWERED GOAL PARSING - Generate specific chart from user's natural language
        # =============================================================================
        if data_goal and len(data_goal.strip()) > 5:
            print(f"🤖 Using AI to parse user goal: '{data_goal}'")
            all_columns = list(df.columns)
            ai_result = self._parse_user_goal_with_ai(data_goal, all_columns)
            
            if ai_result and ai_result.get('x_axis') and ai_result.get('y_axis'):
                try:
                    x_col = ai_result['x_axis']
                    y_col = ai_result['y_axis']
                    group_col = ai_result.get('group_by')
                    chart_type = ai_result.get('chart_type', 'bar')
                    
                    # Validate columns exist
                    if x_col in df.columns and y_col in df.columns:
                        print(f"✅ AI mapped: {x_col} (X) vs {y_col} (Y), grouped by {group_col}, chart type: {chart_type}")
                        
                        # Get design constraints
                        design = self._get_color_palette_and_constraints(chart_type, 'comparison')
                        
                        # Create the specific chart based on AI recommendation
                        if chart_type == 'bar':
                            # Bar chart with grouping
                            if group_col and group_col in df.columns:
                                # Grouped bar chart
                                agg_df = df.groupby([x_col, group_col])[y_col].mean().reset_index()
                                top_x = agg_df[x_col].value_counts().head(10).index
                                agg_df = agg_df[agg_df[x_col].isin(top_x)]
                                
                                fig = px.bar(
                                    agg_df,
                                    x=x_col,
                                    y=y_col,
                                    color=group_col,
                                    title=f'📊 {ai_result.get("explanation", "Analysis")}{sample_note}',
                                    labels={x_col: x_col, y_col: y_col},
                                    barmode='group',
                                    color_discrete_sequence=design['color_palette']
                                )
                            else:
                                # Simple bar chart
                                agg_df = df.groupby(x_col)[y_col].mean().nlargest(15).sort_values()
                                fig = go.Figure(data=[
                                    go.Bar(
                                        x=agg_df.values,
                                        y=agg_df.index,
                                        orientation='h',
                                        marker=dict(color=agg_df.values, colorscale=design['colorscale'], showscale=False),
                                        text=[f'{val:,.2f}' for val in agg_df.values],
                                        textposition='auto'
                                    )
                                ])
                                fig.update_layout(
                                    title=f'📊 {ai_result.get("explanation", "Analysis")}{sample_note}',
                                    xaxis_title=y_col,
                                    yaxis_title=x_col,
                                    height=500
                                )
                            
                        elif chart_type == 'line':
                            # Line chart (time series)
                            df_time = df[[x_col, y_col]].copy()
                            df_time[x_col] = pd.to_datetime(df_time[x_col], errors='coerce')
                            df_time = df_time.dropna()
                            daily_data = df_time.groupby(df_time[x_col].dt.date)[y_col].mean().reset_index()
                            daily_data.columns = ['Date', y_col]
                            
                            fig = px.line(
                                daily_data,
                                x='Date',
                                y=y_col,
                                title=f'📈 {ai_result.get("explanation", "Trend Analysis")}{sample_note}',
                                labels={'Date': x_col, y_col: y_col}
                            )
                            fig.update_traces(line_color=design['color_palette'][0], line_width=3)
                            
                        elif chart_type == 'scatter':
                            # Scatter plot
                            sample_df = df[[x_col, y_col]].dropna().sample(min(1000, len(df)), random_state=42)
                            fig = px.scatter(
                                sample_df,
                                x=x_col,
                                y=y_col,
                                title=f'🔍 {ai_result.get("explanation", "Relationship Analysis")}{sample_note}',
                                labels={x_col: x_col, y_col: y_col},
                                color_discrete_sequence=[design['color_palette'][0]],
                                trendline="ols"
                            )
                            
                        elif chart_type == 'box':
                            # Box plot
                            fig = px.box(
                                df_viz,
                                x=x_col,
                                y=y_col,
                                title=f'📦 {ai_result.get("explanation", "Distribution Analysis")}{sample_note}',
                                labels={x_col: x_col, y_col: y_col},
                                color_discrete_sequence=[design['color_palette'][0]]
                            )
                            
                        else:  # Default to bar
                            agg_df = df.groupby(x_col)[y_col].mean().nlargest(15).sort_values()
                            fig = go.Figure(data=[
                                go.Bar(
                                    x=agg_df.values,
                                    y=agg_df.index,
                                    orientation='h',
                                    marker=dict(color=design['color_palette'][0])
                                )
                            ])
                            fig.update_layout(title=f'📊 {ai_result.get("explanation", "Analysis")}{sample_note}')
                        
                        fig.update_layout(height=500)
                        
                        charts.append({
                            'figure': fig,
                            'title': f'🤖 AI Generated: {data_goal}',
                            'description': ai_result.get('explanation', 'Chart generated from your request'),
                            'chart_type': chart_type.capitalize() + ' Chart',
                            'color_palette': design['color_names'][:3],
                            'design_constraints': design['design_constraints']
                        })
                        print(f"✅ Created AI-generated chart based on user goal")
                        
                except Exception as e:
                    print(f"⚠️ Failed to create AI-generated chart: {e}")
        
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
                        
                        # Get design constraints
                        design = self._get_color_palette_and_constraints('line', user_intent)
                        
                        fig = px.line(
                            daily_data,
                            x='Date',
                            y=num_col,
                            title=f'📈 {num_col} Trend Over Time{sample_note}',
                            labels={num_col: num_col, 'Date': 'Date'}
                        )
                        
                        fig.update_traces(line_color=design['color_palette'][0], line_width=3, mode='lines+markers')
                        fig.update_layout(height=500)
                        
                        charts.append({
                            'figure': fig,
                            'title': f'🎯 {num_col} Over Time (Requested)',
                            'description': f'Time series showing {num_col} trend based on your request{sample_note}',
                            'chart_type': 'Line Chart',
                            'color_palette': design['color_names'][:3],
                            'design_constraints': design['design_constraints']
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
                        
                        # Get design constraints
                        design = self._get_color_palette_and_constraints('bar', user_intent)
                        
                        fig = go.Figure(data=[
                            go.Bar(
                                x=agg_data.values,
                                y=agg_data.index,
                                orientation='h',
                                marker=dict(
                                    color=agg_data.values,
                                    colorscale=design['colorscale'],
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
                            'description': f'Comparison chart based on your request{sample_note}',
                            'chart_type': 'Bar Chart',
                            'color_palette': design['color_names'][:3],
                            'design_constraints': design['design_constraints']
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
                    # Get design constraints
                    design = self._get_color_palette_and_constraints('histogram', user_intent)
                    
                    fig = px.histogram(
                        df_viz,
                        x=num_col,
                        title=f'📊 Distribution of {num_col}{sample_note}',
                        labels={num_col: num_col},
                        color_discrete_sequence=[design['color_palette'][0]],
                        nbins=50
                    )
                    fig.update_layout(height=500, showlegend=False)
                    
                    charts.append({
                        'figure': fig,
                        'title': f'🎯 {num_col} Distribution (Requested)',
                        'description': f'Distribution chart based on your request{sample_note}',
                        'chart_type': 'Histogram',
                        'color_palette': design['color_names'][:2],
                        'design_constraints': design['design_constraints']
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
                    
                    # Get design constraints
                    design = self._get_color_palette_and_constraints('scatter', user_intent)
                    
                    fig = px.scatter(
                        sample_df,
                        x=col1,
                        y=col2,
                        title=f'🔍 {col1} vs {col2} Relationship{sample_note}',
                        labels={col1: col1, col2: col2},
                        opacity=0.6,
                        color_discrete_sequence=[design['color_palette'][0]],
                        trendline="ols"  # Add trend line
                    )
                    fig.update_layout(height=500)
                    
                    charts.append({
                        'figure': fig,
                        'title': f'🎯 {col1} vs {col2} (Requested)',
                        'description': f'Relationship analysis based on your request{sample_note}',
                        'chart_type': 'Scatter Plot',
                        'color_palette': design['color_names'][:3],
                        'design_constraints': design['design_constraints']
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
                        
                        # Get design constraints
                        design = self._get_color_palette_and_constraints('bar', 'comparison')
                        
                        fig = go.Figure(data=[
                            go.Bar(
                                x=agg_data.values,
                                y=agg_data.index,
                                orientation='h',
                                marker=dict(
                                    color=agg_data.values,
                                    colorscale=design['colorscale'],
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
                            'description': f'Bar chart showing {num_col} across {cat_col}{sample_note}',
                            'chart_type': 'Bar Chart',
                            'color_palette': design['color_names'][:3],
                            'design_constraints': design['design_constraints']
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
                    
                    # Get design constraints
                    design = self._get_color_palette_and_constraints('pie', 'proportion')
                    
                    fig = go.Figure(data=[
                        go.Pie(
                            labels=value_counts.index,
                            values=value_counts.values,
                            hole=0.4,
                            marker=dict(colors=design['color_palette'])
                        )
                    ])
                    
                    fig.update_layout(
                        title=f'{cat_col} Distribution{sample_note}',
                        height=500
                    )
                    
                    charts.append({
                        'figure': fig,
                        'title': f'{cat_col} Breakdown',
                        'description': f'Pie chart showing {cat_col} distribution{sample_note}',
                        'chart_type': 'Pie Chart',
                        'color_palette': design['color_names'][:4],
                        'design_constraints': design['design_constraints']
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
