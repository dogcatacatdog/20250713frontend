from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from typing import Dict, Any
import time

app = Flask(__name__)
CORS(app)

# Ollama API Configuration
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3:latest"

def call_ollama_api(prompt: str) -> Dict[str, Any]:
    """Call Ollama API"""
    try:
        url = f"{OLLAMA_BASE_URL}/api/generate"
        data = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 200,
                "num_ctx": 1024
            }
        }
        
        print(f"🔄 Starting Ollama API call")
        print(f"📍 URL: {url}")
        print(f"🤖 Model: {OLLAMA_MODEL}")
        print(f"📝 Prompt: {prompt[:100]}...")
        print(f"📦 Request data: {data}")
        
        response = requests.post(url, json=data, timeout=80)  # Increased timeout to 80s
        
        print(f"📊 Response status code: {response.status_code}")
        print(f"📄 Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"📥 Response JSON: {result}")
            
            ollama_response = result.get("response", "")
            print(f"📏 Response length: {len(ollama_response)} characters")
            print(f"📖 Response content: '{ollama_response}'")
            
            if ollama_response.strip():
                return {
                    "success": True,
                    "response": ollama_response
                }
            else:
                print("❌ Empty response received")
                return {
                    "success": False,
                    "error": "Received empty response from Ollama"
                }
        else:
            error_text = response.text
            print(f"❌ HTTP error: {response.status_code}")
            print(f"📄 Error content: {error_text}")
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {error_text}"
            }
            
    except requests.exceptions.Timeout:
        print("⏰ Request timeout (80s)")
        return {
            "success": False,
            "error": "Ollama API call timeout (80s)"
        }
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - Cannot connect to Ollama server")
        return {
            "success": False,
            "error": "Failed to connect to Ollama server"
        }
    except Exception as e:
        print(f"💥 Exception occurred: {type(e).__name__}: {str(e)}")
        return {
            "success": False,
            "error": f"Exception occurred: {str(e)}"
        }

@app.route('/api/llama-advice', methods=['POST', 'OPTIONS'])
def get_advice():
    """Advice API"""
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        return response
    
    try:
        data = request.get_json()
        print(f"📨 Request data: {data}")
        
        if not data or 'goal' not in data:
            return jsonify({
                'success': False,
                'error': 'Please enter a goal.'
            }), 400
        
        goal = data['goal'].strip()
        if not goal:
            return jsonify({
                'success': False,
                'error': 'Goal is empty.'
            }), 400
        
        # Use English prompt
        prompt = f"""Goal: {goal}

Please provide practical advice to achieve this goal. Give 3-4 specific tips. Use emojis.

Advice:"""
        
        print(f"🎯 Goal to process: '{goal}'")
        print(f"📝 Generated prompt:\n{prompt}")
        
        # Call Ollama API
        print("🔄 Starting Ollama API call...")
        result = call_ollama_api(prompt)
        print(f"📥 Ollama API result: {result}")
        
        if result["success"]:
            advice = result["response"].strip()
            print(f"✅ Advice generation successful!")
            print(f"📋 Generated advice: '{advice}'")
            
            return jsonify({
                'success': True,
                'advice': advice
            })
        else:
            error_msg = result["error"]
            print(f"❌ Ollama API failed: {error_msg}")
            print("🔄 Using fallback advice")
            
            # Fallback advice
            fallback = f"🎯 Advice for achieving '{goal}' goal:\n\n📋 Create a specific plan\n⏰ Execute a little each day\n📊 Record your progress\n🎉 Celebrate small achievements\n\n⚠️ AI advice generation failed: {error_msg}"
            
            return jsonify({
                'success': True,
                'advice': fallback
            })
            
    except Exception as e:
        print(f"💥 Server error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/ollama-status', methods=['GET'])
def check_status():
    """Check Ollama status"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = [m["name"] for m in data.get("models", [])]
            return jsonify({
                'status': 'connected',
                'models': models,
                'current_model': OLLAMA_MODEL
            })
        else:
            return jsonify({
                'status': 'error',
                'message': f'Server error: {response.status_code}'
            }), 500
    except Exception as e:
        return jsonify({
            'status': 'disconnected',
            'message': f'Connection failed: {str(e)}'
        }), 503

@app.route('/api/health', methods=['GET'])
def health():
    """Server health check"""
    return jsonify({
        'status': 'healthy',
        'message': 'Flask server is running'
    })

@app.route('/api/simple-test', methods=['POST'])
def simple_test():
    """Simple test endpoint"""
    try:
        data = request.get_json()
        goal = data.get('goal', 'test')
        
        advice = f"🎯 Test advice for '{goal}':\n\n📋 Create a plan\n⏰ Execute consistently\n📊 Track progress\n🎉 Celebrate achievements"
        
        return jsonify({
            'success': True,
            'advice': advice
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Flask server")
    print("📍 http://localhost:5000")
    print("🔧 Ollama URL:", OLLAMA_BASE_URL)
    print("🤖 Model:", OLLAMA_MODEL)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
