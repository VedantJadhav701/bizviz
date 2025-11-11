"""
Enhanced Streamlit Application for Data Visualization Assistant
With file upload and automatic chart generation capabilities.
"""

import streamlit as st
import json
import pandas as pd
import io
import base64
from services.visualization_assistant import VisualizationAssistant
from services.data_analyzer import DataAnalyzer
from utils.formatting import (
    format_full_response,
    get_example_goals,
    validate_data_goal,
    get_intent_icon,
    get_intent_description,
    export_to_json
)


# Check if Kaleido is available for PNG export
def check_kaleido_available():
    """Check if Kaleido/Chrome is available for PNG export."""
    try:
        import plotly.graph_objects as go
        # Try to create a simple figure and export it
        test_fig = go.Figure(data=[go.Scatter(x=[1], y=[1])])
        test_fig.to_image(format="png", width=100, height=100)
        return True
    except Exception:
        return False


# Cache the result to avoid checking multiple times
@st.cache_data
def is_png_export_available():
    """Cached check for PNG export availability."""
    return check_kaleido_available()


def export_chart_to_png(fig, filename="chart.png"):
    """
    Export Plotly figure to PNG format.
    
    Args:
        fig: Plotly figure object
        filename: Name for the downloaded file
        
    Returns:
        PNG bytes data or None if export fails
    """
    try:
        # Export figure as PNG bytes
        img_bytes = fig.to_image(format="png", width=1200, height=800, scale=2)
        return img_bytes
    except Exception as e:
        # Silently fail - the UI will handle showing appropriate message
        return None


def main():
    """Main application function."""
    
    # Page configuration
    st.set_page_config(
        page_title="Data Visualization Assistant",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .main-header {
            font-size: 3rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 1rem;
        }
        .sub-header {
            font-size: 1.2rem;
            color: #555;
            text-align: center;
            margin-bottom: 2rem;
        }
        .insight-card {
            background-color: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 5px solid #1f77b4;
            margin: 1rem 0;
        }
        .recommendation-card {
            background-color: #e8f5e9;
            padding: 1rem;
            border-radius: 8px;
            margin-top: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">📊 Data Visualization Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Upload data or describe your goal - Get instant insights & visualizations</p>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'assistant' not in st.session_state:
        st.session_state.assistant = VisualizationAssistant()
    if 'mode' not in st.session_state:
        st.session_state.mode = 'recommendation'
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 Choose Your Mode")
        
        mode = st.radio(
            "Select mode:",
            options=['recommendation', 'data_analysis'],
            format_func=lambda x: '💡 Get Recommendations' if x == 'recommendation' else '📈 Analyze My Data',
            key='mode_selector'
        )
        st.session_state.mode = mode
        
        st.divider()
        
        if mode == 'recommendation':
            st.header("📚 Examples")
            st.write("Click any example to try it:")
            
            examples = get_example_goals()
            for i, example in enumerate(examples[:5]):
                if st.button(f"💡 {example}", key=f"example_{i}"):
                    st.session_state.data_goal = example
        else:
            st.header("ℹ️ Data Analysis Mode")
            st.write("""
            Upload your CSV/Excel file to:
            - Get automatic visualizations
            - Receive business insights
            - See actionable recommendations
            """)
        
        st.divider()
        
        st.header("🎯 Intent Types")
        st.write("""
        - **Comparison**: Compare values
        - **Trend**: Show changes over time
        - **Distribution**: Display data spread
        - **Proportion**: Show parts of whole
        - **Relationship**: Examine correlations
        """)
    
    # Main content area
    if st.session_state.mode == 'recommendation':
        show_recommendation_mode()
    else:
        show_data_analysis_mode()
    
    # Footer
    st.divider()
    st.markdown("""
        <div style="text-align: center; color: #888; padding: 1rem;">
            <p>Built for small business users • Keep it simple, keep it clear 📊</p>
        </div>
    """, unsafe_allow_html=True)


def show_recommendation_mode():
    """Show the recommendation mode interface."""
    st.header("💡 Get Chart Recommendations")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Text input
        data_goal = st.text_area(
            "Describe what you want to communicate with your data:",
            value=st.session_state.get('data_goal', ''),
            height=100,
            placeholder="Example: Compare monthly sales across regions...",
            help="Be specific about what you want to show."
        )
        
        # Buttons
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            analyze_button = st.button("🔍 Analyze Goal", type="primary", use_container_width=True)
        with col_btn2:
            clear_button = st.button("🗑️ Clear", use_container_width=True)
        
        if clear_button:
            st.session_state.data_goal = ''
            st.session_state.pop('result', None)
            st.rerun()
    
    with col2:
        st.header("⚙️ Options")
        show_json = st.checkbox("Show JSON Output", value=False)
        
        st.info("💡 **Tip:** The more specific your goal, the better the recommendations!")
    
    # Process analysis
    if analyze_button:
        is_valid, message = validate_data_goal(data_goal)
        
        if not is_valid:
            st.error(message)
        else:
            with st.spinner("🔍 Analyzing your data goal..."):
                result = st.session_state.assistant.analyze_data_goal(data_goal)
                st.session_state.result = result
                st.session_state.data_goal = data_goal
    
    # Display results
    if 'result' in st.session_state:
        result = st.session_state.result
        
        st.divider()
        
        # Intent display
        intent = result['intent']
        intent_icon = get_intent_icon(intent)
        intent_desc = get_intent_description(intent)
        
        st.markdown(f"""
        <div class="insight-card">
            <h2>{intent_icon} Detected Intent: <strong>{intent.upper()}</strong></h2>
            <p style="font-size: 1.1rem; margin-top: 0.5rem;">{intent_desc}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Recommendations
        st.header("📈 Top 3 Chart Recommendations")
        
        tabs = st.tabs([f"#{i+1} {rec['name']}" for i, rec in enumerate(result['recommendations'])])
        
        for i, (tab, rec) in enumerate(zip(tabs, result['recommendations'])):
            with tab:
                st.subheader(f"{rec['name']}")
                st.write(f"**📝 Rationale:** {rec['rationale']}")
                
                st.markdown("---")
                st.markdown("### 🎨 Design Constraints")
                
                col_c1, col_c2, col_c3 = st.columns(3)
                
                with col_c1:
                    st.markdown("**🎨 Color Palette**")
                    st.info(rec['constraints']['color'])
                
                with col_c2:
                    st.markdown("**📊 Axis Scale**")
                    st.info(rec['constraints']['axis'])
                
                with col_c3:
                    st.markdown("**🏷️ Labeling Focus**")
                    st.info(rec['constraints']['label'])
        
        # JSON output
        if show_json:
            st.divider()
            st.header("📄 JSON Output")
            json_output = json.dumps(result, indent=2)
            st.code(json_output, language="json")
            
            st.download_button(
                label="⬇️ Download JSON",
                data=json_output,
                file_name="visualization_recommendations.json",
                mime="application/json"
            )
    else:
        st.info("👆 Enter your data visualization goal above and click 'Analyze Goal' to get started!")


def show_data_analysis_mode():
    """Show the data analysis mode interface with file upload."""
    st.header("📈 Analyze Your Data")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload your data file (CSV or Excel)",
        type=['csv', 'xlsx', 'xls'],
        help="Upload CSV or Excel files up to 200MB. Large files may take a moment to process."
    )
    
    st.markdown("### 🎯 What would you like to see? (Optional)")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Optional data goal input
        data_goal = st.text_area(
            "Describe what you want:",
            value=st.session_state.get('data_analysis_goal', ''),
            height=80,
            placeholder="Example: Show me trends over time, Compare categories, Show distribution..."
        )
        
        # Quick examples
        st.caption("**💡 Quick examples:**")
        col_ex1, col_ex2, col_ex3 = st.columns(3)
        with col_ex1:
            if st.button("� Trends", key="ex_trends"):
                data_goal = "Show me trends over time"
        with col_ex2:
            if st.button("📊 Compare", key="ex_compare"):
                data_goal = "Compare by category"
        with col_ex3:
            if st.button("🔍 Relationships", key="ex_relation"):
                data_goal = "Show relationships"
    
    with col2:
        st.info("💡 **Smart Charts:**\n- **'trends'** → Time series charts\n- **'compare'** → Bar charts\n- **'distribution'** → Histograms\n- Blank → Auto-select best charts")
    
    if uploaded_file is not None:
        try:
            # Load data
            file_size_mb = uploaded_file.size / (1024 * 1024)
            
            with st.spinner(f"📂 Loading your data ({file_size_mb:.1f}MB)..."):
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.session_state.uploaded_df = df
                st.session_state.data_analysis_goal = data_goal
            
            # Show data preview
            st.success(f"✅ Loaded {len(df):,} rows and {len(df.columns)} columns ({file_size_mb:.1f}MB)")
            
            with st.expander("📋 Data Preview", expanded=True):
                st.dataframe(df.head(10), use_container_width=True)
            
            # Analyze data
            with st.spinner("🔍 Analyzing your data..."):
                analyzer = DataAnalyzer(df)
                analysis = analyzer.analyze_data()
                insights = analyzer.generate_sales_insights(analysis)
                charts = analyzer.create_visualizations(data_goal, analysis)
            
            st.divider()
            
            # Display insights
            if insights:
                st.header("💡 Business Insights & Recommendations")
                st.write("Here are the top insights from your data:")
                
                for i, insight in enumerate(insights, 1):
                    st.markdown(f"""
                    <div class="insight-card">
                        <h3>{insight['title']}</h3>
                        <p style="font-size: 1.1rem; margin: 0.5rem 0;"><strong>Insight:</strong> {insight['insight']}</p>
                        <div class="recommendation-card">
                            <strong>💡 Recommendation:</strong> {insight['recommendation']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.divider()
            
            # Display charts
            if charts:
                st.header("📊 Visualizations")
                st.write("Automatically generated charts based on your data:")
                
                # Check PNG export availability once
                png_available = is_png_export_available()
                
                # Show info message if PNG export is not available
                if not png_available:
                    st.info("💡 **Tip:** PNG export requires Chrome/Chromium. You can still interact with and use the charts below. To enable PNG downloads, run: `pip install kaleido` and install Chrome.")
                
                for i, chart_data in enumerate(charts, 1):
                    with st.container():
                        col_title, col_download = st.columns([3, 1])
                        
                        with col_title:
                            st.subheader(f"{i}. {chart_data['title']}")
                        
                        with col_download:
                            # PNG download button - only show if available
                            if png_available:
                                try:
                                    img_bytes = export_chart_to_png(
                                        chart_data['figure'], 
                                        f"{chart_data['title'].lower().replace(' ', '_')}.png"
                                    )
                                    if img_bytes:
                                        st.download_button(
                                            label="📥 PNG",
                                            data=img_bytes,
                                            file_name=f"{chart_data['title'].lower().replace(' ', '_')}.png",
                                            mime="image/png",
                                            key=f"download_png_{i}"
                                        )
                                except Exception:
                                    pass  # Silently skip if export fails
                        
                        st.write(chart_data['description'])
                        
                        # Display chart type and color palette
                        if 'chart_type' in chart_data:
                            col_type, col_palette = st.columns([1, 2])
                            with col_type:
                                st.markdown(f"**📊 Type:** `{chart_data['chart_type']}`")
                            with col_palette:
                                if 'color_palette' in chart_data:
                                    colors_text = ", ".join(chart_data['color_palette'])
                                    st.markdown(f"**🎨 Colors:** {colors_text}")
                        
                        # Display 3 key visual design constraints
                        if 'design_constraints' in chart_data:
                            with st.expander("🎯 Visual Design Constraints", expanded=False):
                                constraints = chart_data['design_constraints']
                                st.markdown(f"""
                                1. **Color Palette:** {constraints['1_color_palette']}
                                2. **Axis Scale:** {constraints['2_axis_scale']}
                                3. **Labeling Focus:** {constraints['3_labeling_focus']}
                                """)
                        
                        st.plotly_chart(chart_data['figure'], use_container_width=True)
                        st.divider()
            
            # Data summary
            with st.expander("📊 Data Summary Statistics"):
                col_sum1, col_sum2, col_sum3 = st.columns(3)
                
                with col_sum1:
                    st.metric("Total Rows", f"{len(df):,}")
                    st.metric("Total Columns", len(df.columns))
                
                with col_sum2:
                    numeric_cols = len(analysis['numeric_columns'])
                    categorical_cols = len(analysis['categorical_columns'])
                    st.metric("Numeric Columns", numeric_cols)
                    st.metric("Categorical Columns", categorical_cols)
                
                with col_sum3:
                    missing_total = sum(analysis['missing_values'].values())
                    missing_pct = (missing_total / (len(df) * len(df.columns))) * 100
                    st.metric("Missing Values", f"{missing_total:,}")
                    st.metric("Missing %", f"{missing_pct:.1f}%")
            
            # Export options
            st.divider()
            col_exp1, col_exp2 = st.columns(2)
            
            with col_exp1:
                if insights:
                    insights_text = "\n\n".join([
                        f"{ins['title']}\n{ins['insight']}\nRecommendation: {ins['recommendation']}"
                        for ins in insights
                    ])
                    st.download_button(
                        label="📥 Download Insights Report",
                        data=insights_text,
                        file_name="business_insights.txt",
                        mime="text/plain"
                    )
            
            with col_exp2:
                if charts:
                    st.download_button(
                        label="📥 Download Data Summary",
                        data=df.describe().to_csv(),
                        file_name="data_summary.csv",
                        mime="text/csv"
                    )
        
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
            st.write("Please make sure your file is properly formatted.")
    
    else:
        # Show example/instructions
        st.info("👆 Upload a CSV or Excel file to get started!")
        
        st.divider()
        
        col_inst1, col_inst2 = st.columns(2)
        
        with col_inst1:
            st.markdown("### 📁 Supported File Types")
            st.write("""
            - **CSV** (.csv) - Comma-separated values
            - **Excel** (.xlsx, .xls) - Microsoft Excel files
            """)
            
            st.markdown("### 💡 What You'll Get")
            st.write("""
            1. **Automatic Visualizations** - Charts based on your data
            2. **Business Insights** - Key findings from your data
            3. **Recommendations** - Actionable suggestions to improve
            4. **Data Summary** - Statistical overview
            """)
        
        with col_inst2:
            st.markdown("### 🎯 Best Practices")
            st.write("""
            - Use clean, structured data
            - Include column headers
            - Ensure dates are properly formatted
            - Remove special characters from headers
            """)
            
            st.markdown("### 📊 Example Columns")
            st.code("""
OrderDate, Product, Category, 
Revenue, Quantity, Location,
Status, CustomerID
            """)


if __name__ == "__main__":
    main()
