"""
Flask REST API for BizViz Data Visualization Assistant
Provides endpoints for React frontend integration
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from services.visualization_assistant import VisualizationAssistant
from services.data_analyzer import DataAnalyzer
import pandas as pd
import io
import base64
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Enable CORS for React frontend
CORS(app, origins=["http://localhost:3000", "http://localhost:3001"])

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB max file size
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

# Initialize services
viz_assistant = VisualizationAssistant()


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify API is running.
    
    Returns:
        JSON with status and version
    """
    return jsonify({
        "status": "healthy",
        "version": "1.0.0",
        "service": "BizViz Data Visualization API"
    }), 200


@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    """
    Get chart recommendations from text description.
    
    Request Body:
        {
            "data_goal": "Compare monthly sales across regions"
        }
    
    Response:
        {
            "intent": "comparison",
            "recommendations": [
                {
                    "name": "Bar Chart",
                    "rationale": "Perfect for comparing values across categories",
                    "constraints": {
                        "color": "Use distinct colors for each category",
                        "axis": "Categories on X-axis, values on Y-axis",
                        "label": "Label each bar with exact values"
                    }
                }
            ]
        }
    
    Status Codes:
        200: Success
        400: Bad request (missing data_goal)
        500: Internal server error
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data or 'data_goal' not in data:
            return jsonify({
                "error": "Missing 'data_goal' in request body"
            }), 400
        
        data_goal = data.get('data_goal', '').strip()
        
        if not data_goal:
            return jsonify({
                "error": "data_goal cannot be empty"
            }), 400
        
        # Get recommendations from service
        result = viz_assistant.analyze_data_goal(data_goal)
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({
            "error": "Failed to process request",
            "details": str(e)
        }), 500


@app.route('/api/detect-intent', methods=['POST'])
def detect_intent():
    """
    Detect visualization intent from text description only.
    
    Request Body:
        {
            "data_goal": "Show sales trend over time"
        }
    
    Response:
        {
            "intent": "trend"
        }
    
    Status Codes:
        200: Success
        400: Bad request
        500: Internal server error
    """
    try:
        data = request.get_json()
        
        if not data or 'data_goal' not in data:
            return jsonify({
                "error": "Missing 'data_goal' in request body"
            }), 400
        
        data_goal = data.get('data_goal', '').strip()
        
        if not data_goal:
            return jsonify({
                "error": "data_goal cannot be empty"
            }), 400
        
        # Detect intent only
        intent = viz_assistant.detect_intent(data_goal)
        
        return jsonify({
            "intent": intent,
            "data_goal": data_goal
        }), 200
    
    except Exception as e:
        return jsonify({
            "error": "Failed to detect intent",
            "details": str(e)
        }), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_data():
    """
    Analyze uploaded CSV/Excel file and generate insights + charts.
    
    Request:
        multipart/form-data with:
        - file: CSV or Excel file (required)
        - data_goal: Text description (optional)
    
    Response:
        {
            "analysis": {
                "shape": [rows, cols],
                "columns": ["col1", "col2", ...],
                "numeric_columns": [...],
                "categorical_columns": [...],
                "date_columns": [...]
            },
            "insights": [
                {
                    "title": "Revenue Performance",
                    "insight": "Total revenue is $1.2M...",
                    "recommendation": "Focus on top-performing categories"
                }
            ],
            "charts": [
                {
                    "title": "Revenue by Category",
                    "description": "Bar chart showing revenue distribution",
                    "chart_data": {...},  # Plotly JSON
                    "chart_type": "bar"
                }
            ]
        }
    
    Status Codes:
        200: Success
        400: Bad request (no file, invalid format)
        500: Internal server error
    """
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({
                "error": "No file uploaded",
                "details": "Request must include 'file' in multipart/form-data"
            }), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({
                "error": "No file selected"
            }), 400
        
        # Check file extension
        if not allowed_file(file.filename):
            return jsonify({
                "error": "Invalid file format",
                "details": f"Allowed formats: {', '.join(ALLOWED_EXTENSIONS)}"
            }), 400
        
        # Read file into DataFrame
        try:
            if file.filename.endswith('.csv'):
                df = pd.read_csv(io.StringIO(file.stream.read().decode("UTF-8")))
            elif file.filename.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file)
            else:
                return jsonify({
                    "error": "Unsupported file format"
                }), 400
        except Exception as e:
            return jsonify({
                "error": "Failed to read file",
                "details": f"File parsing error: {str(e)}"
            }), 400
        
        # Check if DataFrame is empty
        if df.empty:
            return jsonify({
                "error": "File is empty",
                "details": "Uploaded file contains no data"
            }), 400
        
        # Get optional data_goal parameter
        data_goal = request.form.get('data_goal', '')
        
        # Analyze data using DataAnalyzer service
        analyzer = DataAnalyzer(df)
        analysis = analyzer.analyze_data()
        insights = analyzer.generate_sales_insights(analysis)
        charts = analyzer.create_visualizations(data_goal, analysis)
        
        # Convert Plotly figures to JSON
        charts_json = []
        for chart in charts:
            charts_json.append({
                'title': chart['title'],
                'description': chart['description'],
                'chart_data': chart['figure'].to_json(),
                'chart_type': 'plotly'
            })
        
        # Build response
        response_data = {
            'filename': secure_filename(file.filename),
            'analysis': {
                'shape': list(analysis['shape']),
                'columns': analysis['columns'],
                'numeric_columns': analysis['numeric_columns'],
                'categorical_columns': analysis['categorical_columns'],
                'date_columns': analysis['date_columns']
            },
            'insights': insights,
            'charts': charts_json
        }
        
        return jsonify(response_data), 200
    
    except Exception as e:
        return jsonify({
            "error": "Failed to analyze data",
            "details": str(e)
        }), 500


@app.route('/api/export-chart', methods=['POST'])
def export_chart():
    """
    Export Plotly chart as PNG image (base64 encoded).
    
    Request Body:
        {
            "chart_json": {...}  # Plotly JSON from to_json()
        }
    
    Response:
        {
            "image": "base64_encoded_png_data",
            "format": "png",
            "width": 1200,
            "height": 800
        }
    
    Status Codes:
        200: Success
        400: Bad request
        500: Internal server error
    """
    try:
        import plotly.graph_objects as go
        
        data = request.get_json()
        
        if not data or 'chart_json' not in data:
            return jsonify({
                "error": "Missing 'chart_json' in request body"
            }), 400
        
        chart_json = data.get('chart_json', {})
        
        # Get optional dimensions
        width = data.get('width', 1200)
        height = data.get('height', 800)
        scale = data.get('scale', 2)
        
        # Recreate figure from JSON
        fig = go.Figure(chart_json)
        
        # Convert to PNG
        img_bytes = fig.to_image(
            format="png",
            width=width,
            height=height,
            scale=scale
        )
        
        # Encode as base64
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        
        return jsonify({
            'image': img_base64,
            'format': 'png',
            'width': width,
            'height': height
        }), 200
    
    except ImportError:
        return jsonify({
            "error": "Kaleido not installed",
            "details": "Install with: pip install kaleido"
        }), 500
    except Exception as e:
        return jsonify({
            "error": "Failed to export chart",
            "details": str(e)
        }), 500


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file size exceeded error."""
    return jsonify({
        "error": "File too large",
        "details": f"Maximum file size is {int(app.config['MAX_CONTENT_LENGTH'] / (1024 * 1024))}MB"
    }), 413


@app.errorhandler(404)
def not_found(error):
    """Handle not found errors."""
    return jsonify({
        "error": "Endpoint not found",
        "details": "Check API documentation for available endpoints"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle internal server errors."""
    return jsonify({
        "error": "Internal server error",
        "details": "An unexpected error occurred"
    }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 BizViz Data Visualization API")
    print("=" * 60)
    print("📡 Server running on: http://localhost:5000")
    print("📚 Available endpoints:")
    print("   GET  /api/health              - Health check")
    print("   POST /api/recommendations     - Get chart recommendations")
    print("   POST /api/detect-intent       - Detect visualization intent")
    print("   POST /api/analyze             - Analyze uploaded data")
    print("   POST /api/export-chart        - Export chart as PNG")
    print("=" * 60)
    print("✅ CORS enabled for: http://localhost:3000, http://localhost:3001")
    print("📁 Max file size: 16MB")
    print("📄 Allowed formats: CSV, XLSX, XLS")
    print("=" * 60)
    
    app.run(debug=True, port=5000, host='0.0.0.0')
