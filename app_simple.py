from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from typing import Dict, Any
import time

app = Flask(__name__)
CORS(app)

# Ollama API 설정
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3:latest"

def call_ollama_api(prompt: str) -> Dict[str, Any]:
    """Ollama API 호출"""
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
        
        print(f"🔄 Ollama API 호출 시작")
        print(f"📍 URL: {url}")
        print(f"🤖 모델: {OLLAMA_MODEL}")
        print(f"📝 프롬프트: {prompt[:100]}...")
        print(f"📦 요청 데이터: {data}")
        
        response = requests.post(url, json=data, timeout=80)  # 타임아웃을 60초로 증가
        
        print(f"📊 응답 상태 코드: {response.status_code}")
        print(f"📄 응답 헤더: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"📥 응답 JSON: {result}")
            
            ollama_response = result.get("response", "")
            print(f"📏 응답 길이: {len(ollama_response)}자")
            print(f"📖 응답 내용: '{ollama_response}'")
            
            if ollama_response.strip():
                return {
                    "success": True,
                    "response": ollama_response
                }
            else:
                print("❌ 빈 응답 수신")
                return {
                    "success": False,
                    "error": "Ollama에서 빈 응답을 받았습니다"
                }
        else:
            error_text = response.text
            print(f"❌ HTTP 오류: {response.status_code}")
            print(f"📄 오류 내용: {error_text}")
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {error_text}"
            }
            
    except requests.exceptions.Timeout:
        print("⏰ 요청 타임아웃 (60초)")
        return {
            "success": False,
            "error": "Ollama API 호출 타임아웃 (60초)"
        }
    except requests.exceptions.ConnectionError:
        print("❌ 연결 오류 - Ollama 서버에 연결할 수 없음")
        return {
            "success": False,
            "error": "Ollama 서버 연결 실패"
        }
    except Exception as e:
        print(f"💥 예외 발생: {type(e).__name__}: {str(e)}")
        return {
            "success": False,
            "error": f"예외 발생: {str(e)}"
        }

@app.route('/api/llama-advice', methods=['POST', 'OPTIONS'])
def get_advice():
    """조언 API"""
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        return response
    
    try:
        data = request.get_json()
        print(f"📨 요청 데이터: {data}")
        
        if not data or 'goal' not in data:
            return jsonify({
                'success': False,
                'error': '목표를 입력해주세요.'
            }), 400
        
        goal = data['goal'].strip()
        if not goal:
            return jsonify({
                'success': False,
                'error': '목표가 비어있습니다.'
            }), 400
        
        # 영어 프롬프트 사용
        prompt = f"""Goal: {goal}

Please provide practical advice to achieve this goal. Give 3-4 specific tips. Use emojis.

Advice:"""
        
        print(f"🎯 처리할 목표: '{goal}'")
        print(f"📝 생성된 프롬프트:\n{prompt}")
        
        # Ollama API 호출
        print("🔄 Ollama API 호출 시작...")
        result = call_ollama_api(prompt)
        print(f"📥 Ollama API 결과: {result}")
        
        if result["success"]:
            advice = result["response"].strip()
            print(f"✅ 조언 생성 성공!")
            print(f"📋 생성된 조언: '{advice}'")
            
            return jsonify({
                'success': True,
                'advice': advice
            })
        else:
            error_msg = result["error"]
            print(f"❌ Ollama API 실패: {error_msg}")
            print("🔄 Fallback 조언 사용")
            
            # Fallback 조언
            fallback = f"🎯 '{goal}' 목표를 달성하기 위한 조언:\n\n📋 구체적인 계획을 세우세요\n⏰ 매일 조금씩 실행하세요\n📊 진행 상황을 기록하세요\n🎉 작은 성취도 축하하세요\n\n⚠️ AI 조언 생성 실패: {error_msg}"
            
            return jsonify({
                'success': True,
                'advice': fallback
            })
            
    except Exception as e:
        print(f"💥 서버 오류: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'서버 오류: {str(e)}'
        }), 500

@app.route('/api/ollama-status', methods=['GET'])
def check_status():
    """Ollama 상태 확인"""
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
                'message': f'서버 오류: {response.status_code}'
            }), 500
    except Exception as e:
        return jsonify({
            'status': 'disconnected',
            'message': f'연결 실패: {str(e)}'
        }), 503

@app.route('/api/health', methods=['GET'])
def health():
    """서버 상태"""
    return jsonify({
        'status': 'healthy',
        'message': 'Flask 서버 정상'
    })

@app.route('/api/simple-test', methods=['POST'])
def simple_test():
    """간단한 테스트"""
    try:
        data = request.get_json()
        goal = data.get('goal', '테스트')
        
        advice = f"🎯 '{goal}' 테스트 조언:\n\n📋 계획 세우기\n⏰ 꾸준히 실행\n📊 진행 확인\n🎉 성과 축하"
        
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
    print("🚀 Flask 서버 시작")
    print("📍 http://localhost:5000")
    print("🔧 Ollama URL:", OLLAMA_BASE_URL)
    print("🤖 모델:", OLLAMA_MODEL)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
