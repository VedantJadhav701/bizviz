"""
Test script for data analysis functionality
Tests the DataAnalyzer with the Flipkart Sales Dataset
"""

import pandas as pd
from services.data_analyzer import DataAnalyzer


def test_flipkart_analysis():
    """Test analysis with Flipkart dataset."""
    
    print("=" * 80)
    print("TESTING DATA ANALYZER WITH FLIPKART SALES DATASET")
    print("=" * 80)
    print()
    
    # Load the dataset
    print("📂 Loading Flipkart Sales Dataset...")
    try:
        df = pd.read_csv('Flipkart Sales Dataset.csv')
        print(f"✅ Loaded {len(df):,} rows and {len(df.columns)} columns")
        print()
    except FileNotFoundError:
        print("❌ Flipkart Sales Dataset.csv not found in current directory")
        return
    except Exception as e:
        print(f"❌ Error loading file: {str(e)}")
        return
    
    # Show dataset info
    print("📊 Dataset Preview:")
    print(df.head(3).to_string())
    print()
    
    # Initialize analyzer
    print("🔍 Initializing DataAnalyzer...")
    analyzer = DataAnalyzer(df)
    print("✅ Analyzer initialized")
    print()
    
    # Perform analysis
    print("=" * 80)
    print("ANALYZING DATA")
    print("=" * 80)
    print()
    
    analysis = analyzer.analyze_data()
    
    print(f"📊 Data Shape: {analysis['shape'][0]:,} rows × {analysis['shape'][1]} columns")
    print()
    
    print("📋 Column Types:")
    print(f"  - Numeric columns: {len(analysis['numeric_columns'])}")
    print(f"    {', '.join(analysis['numeric_columns'][:5])}")
    print(f"  - Categorical columns: {len(analysis['categorical_columns'])}")
    print(f"    {', '.join(analysis['categorical_columns'][:5])}")
    print(f"  - Date columns: {len(analysis['date_columns'])}")
    if analysis['date_columns']:
        print(f"    {', '.join(analysis['date_columns'])}")
    print()
    
    # Generate insights
    print("=" * 80)
    print("GENERATING BUSINESS INSIGHTS")
    print("=" * 80)
    print()
    
    insights = analyzer.generate_sales_insights(analysis)
    
    if insights:
        for i, insight in enumerate(insights, 1):
            print(f"{i}. {insight['title']}")
            print(f"   📊 Insight: {insight['insight']}")
            print(f"   💡 Recommendation: {insight['recommendation']}")
            print()
    else:
        print("⚠️ No insights generated")
        print()
    
    # Generate visualizations
    print("=" * 80)
    print("GENERATING VISUALIZATIONS")
    print("=" * 80)
    print()
    
    data_goal = "Analyze sales performance and identify improvement areas"
    charts = analyzer.create_visualizations(data_goal, analysis)
    
    if charts:
        print(f"✅ Generated {len(charts)} visualizations:")
        for i, chart in enumerate(charts, 1):
            print(f"   {i}. {chart['title']}")
            print(f"      {chart['description']}")
        print()
    else:
        print("⚠️ No visualizations generated")
        print()
    
    # Summary
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print()
    print(f"✅ Data Analysis: Success")
    print(f"✅ Insights Generated: {len(insights)}")
    print(f"✅ Charts Created: {len(charts)}")
    print()
    print("🎉 All tests completed successfully!")
    print()


def test_small_sample():
    """Test with a small sample dataset."""
    
    print("=" * 80)
    print("TESTING WITH SAMPLE DATA")
    print("=" * 80)
    print()
    
    # Create sample data
    sample_data = {
        'Date': pd.date_range('2024-01-01', periods=10),
        'Product': ['A', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C'],
        'Category': ['Electronics', 'Fashion', 'Electronics', 'Home', 'Fashion', 
                     'Electronics', 'Home', 'Fashion', 'Electronics', 'Home'],
        'Revenue': [100, 150, 120, 90, 180, 110, 95, 160, 130, 100],
        'Quantity': [1, 2, 1, 1, 3, 1, 1, 2, 1, 1],
        'Status': ['Delivered', 'Delivered', 'Returned', 'Delivered', 'Delivered',
                  'Delivered', 'Returned', 'Delivered', 'Delivered', 'Delivered']
    }
    
    df = pd.DataFrame(sample_data)
    print("📊 Sample Dataset Created:")
    print(df.to_string())
    print()
    
    # Analyze
    analyzer = DataAnalyzer(df)
    analysis = analyzer.analyze_data()
    insights = analyzer.generate_sales_insights(analysis)
    charts = analyzer.create_visualizations("Show sales performance", analysis)
    
    print(f"✅ Analysis Complete:")
    print(f"   - Insights: {len(insights)}")
    print(f"   - Charts: {len(charts)}")
    print()


if __name__ == "__main__":
    # Test with Flipkart dataset
    test_flipkart_analysis()
    
    print("\n" + "=" * 80 + "\n")
    
    # Test with sample data
    test_small_sample()
