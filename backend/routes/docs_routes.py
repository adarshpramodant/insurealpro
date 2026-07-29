from flask import Blueprint, jsonify, render_template_string

docs_bp = Blueprint('docs', __name__)

OPENAPI_SPEC = {
  "openapi": "3.0.0",
  "info": {
    "title": "InsureAI Pro REST API Documentation",
    "description": "Enterprise AI Insurance Intelligence Platform API Specification",
    "version": "2.0.0"
  },
  "paths": {
    "/api/predict": {
      "post": {
        "summary": "Execute Multi-Model Ensemble Insurance Premium Prediction",
        "requestBody": {
          "required": True,
          "content": {
            "application/json": {
              "example": {
                "age": 35,
                "sex": "female",
                "bmi": 28.5,
                "children": 2,
                "smoker": "no",
                "region": "southeast"
              }
            }
          }
        },
        "responses": {
          "200": { "description": "Successful prediction response with multi-model agreement & advisory package." }
        }
      }
    },
    "/api/chatbot": {
      "post": {
        "summary": "Query Context-Aware Insurance AI Chatbot",
        "requestBody": {
          "required": True,
          "content": {
            "application/json": {
              "example": {
                "message": "Why is my premium high?",
                "context": { "predicted_charge": 42000, "risk_level": "High" }
              }
            }
          }
        },
        "responses": { "200": { "description": "Chatbot reply with natural language explanation." } }
      }
    },
    "/api/simulate": {
      "post": {
        "summary": "Run What-If Lifestyle & Metric Scenario Simulation",
        "responses": { "200": { "description": "Simulation delta results and annual savings." } }
      }
    },
    "/api/history": {
      "get": { "summary": "Get Paginated Prediction History Database Records" },
      "delete": { "summary": "Clear History Database" }
    },
    "/api/export": {
      "post": { "summary": "Export Prediction in PDF, CSV, Excel, or JSON formats" }
    },
    "/api/health": {
      "get": { "summary": "Service Health Status Check" }
    }
  }
}

SWAGGER_UI_HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>InsureAI Pro API Documentation</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@4/swagger-ui.css" />
</head>
<body style="margin:0; background:#0f172a;">
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@4/swagger-ui-bundle.js"></script>
  <script>
    SwaggerUIBundle({
      url: '/api/docs/swagger.json',
      dom_id: '#swagger-ui',
    });
  </script>
</body>
</html>
"""

@docs_bp.route('/docs', methods=['GET'])
def render_swagger_ui():
    return render_template_string(SWAGGER_UI_HTML)

@docs_bp.route('/docs/swagger.json', methods=['GET'])
def get_swagger_json():
    return jsonify(OPENAPI_SPEC)
