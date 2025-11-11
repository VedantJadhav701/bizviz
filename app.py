"""
Main Streamlit Application for Data Visualization Assistant
"""

import streamlit as st
import json
from services.visualization_assistant import VisualizationAssistant
from utils.formatting import (
    format_full_response,
    get_example_goals,
    validate_data_goal,
    get_intent_icon,
    get_intent_description,
    export_to_json
)


def main():
    """Main application function."""
    
    # Page configuration
    st.set_page_config(
        page_title="Data Visualization Assistant",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
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
        .stButton>button {
            width: 100%;
            background-color: #1f77b4;
            color: white;
            font-weight: bold;
        }
        .intent-box {
            background-color: #f0f8ff;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 5px solid #1f77b4;
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">📊 Data Visualization Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Transform your data goals into perfect visualizations</p>', unsafe_allow_html=True)
    
    # Initialize the assistant
    if 'assistant' not in st.session_state:
        st.session_state.assistant = VisualizationAssistant()
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.write("""
        This tool helps you choose the right chart for your data by analyzing your visualization goal.
        
        **How it works:**
        1. Describe what you want to show with your data
        2. Get visualization intent detection
        3. Receive top 3 chart recommendations
        4. Follow design constraints for best results
        """)
        
        st.divider()
        
        st.header("📚 Examples")
        st.write("Click any example to try it:")
        
        examples = get_example_goals()
        for example in examples:
            if st.button(f"💡 {example}", key=f"example_{example}"):
                st.session_state.data_goal = example
        
        st.divider()
        
        st.header("🎯 Intent Types")
        st.write("""
        - **Comparison**: Compare values across categories
        - **Trend**: Show changes over time
        - **Distribution**: Display data spread/frequency
        - **Proportion**: Show parts of a whole
        - **Relationship**: Examine correlations
        """)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🎯 Your Data Goal")
        
        # Text input
        data_goal = st.text_area(
            "Describe what you want to communicate with your data:",
            value=st.session_state.get('data_goal', ''),
            height=100,
            placeholder="Example: Compare monthly sales across regions...",
            help="Be specific about what you want to show. Include details like time periods, categories, or metrics."
        )
        
        # Buttons
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
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
        export_json = st.checkbox("Export to JSON File", value=False)
        
        st.info("💡 **Tip:** The more specific your goal, the better the recommendations!")
    
    # Process analysis
    if analyze_button:
        is_valid, message = validate_data_goal(data_goal)
        
        if not is_valid:
            st.error(message)
        else:
            with st.spinner("🔍 Analyzing your data goal..."):
                # Get recommendations
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
        <div class="intent-box">
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
        
        # Export option
        if export_json:
            try:
                export_status = export_to_json(result)
                st.success(export_status)
            except Exception as e:
                st.error(f"Error exporting: {str(e)}")
    
    else:
        # Welcome message when no analysis has been done
        st.info("👆 Enter your data visualization goal above and click 'Analyze Goal' to get started!")
        
        st.divider()
        
        # Show some tips
        st.header("💡 Tips for Better Recommendations")
        
        tip_cols = st.columns(3)
        
        with tip_cols[0]:
            st.markdown("""
            **Be Specific**
            - Mention the type of data
            - Include time periods if relevant
            - Specify what you're comparing
            """)
        
        with tip_cols[1]:
            st.markdown("""
            **Use Clear Language**
            - "Compare sales across regions"
            - "Show revenue growth over time"
            - "Display age distribution"
            """)
        
        with tip_cols[2]:
            st.markdown("""
            **Include Context**
            - What's your audience?
            - What decision needs to be made?
            - What's the key insight?
            """)
    
    # Footer
    st.divider()
    st.markdown("""
        <div style="text-align: center; color: #888; padding: 1rem;">
            <p>Built for small business users • Keep it simple, keep it clear 📊</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
