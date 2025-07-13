#!/usr/bin/env python3
"""
Ollama Integration Debug Script
Space Fantasy Todo App Backend
"""

import requests
import json
import time
import sys

# Configuration
FLASK_URL = "http://localhost:5000"
OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3:latest"

def print_header(title: str):
    """Print header"""
    print("\n" + "=" * 60)
    print(f"🔍 {title}")
    print("=" * 60)

def test_ollama_direct():
    """Test direct Ollama API connection"""
    print_header("Direct Ollama Connection Test")
    
    try:
        # 1. Check Ollama server status
        print("📡 Checking Ollama server connection...")
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=10)
        
        if response.status_code == 200:
            print("✅ Ollama server connection successful!")
            tags = response.json()
            models = [model["name"] for model in tags.get("models", [])]
            print(f"📋 Available models: {models}")
            
            if OLLAMA_MODEL in models:
                print(f"✅ {OLLAMA_MODEL} model available")
            else:
                print(f"❌ {OLLAMA_MODEL} model not found")
                print(f"💡 Download model with: 'ollama pull {OLLAMA_MODEL}'")
                return False
            
            # 2. Test with simple prompt
            test_prompt = "Goal: daily exercise\n\nPlease provide practical advice to achieve this goal. Give 3-4 specific tips. Use emojis.\n\nAdvice:"
            
            data = {
                "model": OLLAMA_MODEL,
                "prompt": test_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 200,
                    "num_ctx": 1024
                }
            }
            
            print(f"🔄 Testing {OLLAMA_MODEL} model...")
            print(f"📝 Prompt: {test_prompt[:50]}...")
            
            start_time = time.time()
            response = requests.post(f"{OLLAMA_URL}/api/generate", json=data, timeout=60)
            end_time = time.time()
            
            response_time = end_time - start_time
            print(f"⏱️ Response time: {response_time:.2f}s")
            
            if response.status_code == 200:
                result = response.json()
                ollama_response = result.get("response", "")
                print("✅ Ollama response successful!")
                print(f"📏 Response length: {len(ollama_response)} characters")
                print(f"📝 Response content:\n{ollama_response}")
                return True
            else:
                print(f"❌ Ollama response failed: {response.status_code}")
                print(f"📄 Error content: {response.text}")
                return False
                
        else:
            print(f"❌ Ollama server connection failed: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama server.")
        print("💡 Solutions:")
        print("   1. Start Ollama server with 'ollama serve'")
        print("   2. Check if port 11434 is available")
        return False
    except requests.exceptions.Timeout:
        print("⏰ Ollama server response timeout")
        return False
    except Exception as e:
        print(f"� Unexpected error: {e}")
        return False

def test_flask_server():
    """Test Flask server"""
    print_header("Flask Server Integration Test")
    
    try:
        # 1. Check Flask server status
        print("🚀 Checking Flask server connection...")
        response = requests.get(f"{FLASK_URL}/api/health", timeout=10)
        
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Flask server connection successful!")
            print(f"📊 Status: {health_data.get('status')}")
            print(f"💬 Message: {health_data.get('message')}")
            
            # 2. Check Ollama status through Flask
            print("\n🦙 Checking Ollama status through Flask...")
            response = requests.get(f"{FLASK_URL}/api/ollama-status", timeout=10)
            
            if response.status_code == 200:
                ollama_status = response.json()
                print(f"🔗 Ollama status: {ollama_status.get('status')}")
                print(f"📋 Available models: {ollama_status.get('models', [])}")
                print(f"🤖 Current model: {ollama_status.get('current_model')}")
                
                # 3. Test advice API
                print("\n🧠 Testing advice API...")
                test_goal = "daily exercise routine"
                advice_data = {"goal": test_goal}
                
                print(f"🎯 Test goal: '{test_goal}'")
                print("⏱️ Generating advice (waiting up to 90s)...")
                
                start_time = time.time()
                response = requests.post(f"{FLASK_URL}/api/llama-advice", json=advice_data, timeout=100)
                end_time = time.time()
                
                response_time = end_time - start_time
                print(f"⏱️ Total response time: {response_time:.2f}s")
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        advice = result.get("advice", "")
                        print("✅ Advice API successful!")
                        print(f"📏 Advice length: {len(advice)} characters")
                        print(f"📝 Generated advice:\n{advice}")
                        return True
                    else:
                        print(f"❌ Advice API failed: {result.get('error')}")
                        return False
                else:
                    print(f"❌ Advice API HTTP error: {response.status_code}")
                    print(f"📄 Error content: {response.text}")
                    return False
            else:
                print(f"❌ Ollama status check failed: {response.status_code}")
                return False
        else:
            print(f"❌ Flask server connection failed: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Flask server.")
        print("💡 Solutions:")
        print("   1. Start Flask server with 'python app_simple.py'")
        print("   2. Check if port 5000 is available")
        return False
    except requests.exceptions.Timeout:
        print("⏰ Flask server response timeout")
        return False
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        return False

def test_integration():
    """Integration test"""
    print_header("Integration Test")
    
    try:
        # Test multiple goals
        test_goals = [
            "learn Python programming",
            "exercise daily",
            "save money"
        ]
        
        success_count = 0
        
        for i, goal in enumerate(test_goals, 1):
            print(f"\n📋 Test {i}: '{goal}'")
            
            advice_data = {"goal": goal}
            
            try:
                start_time = time.time()
                response = requests.post(f"{FLASK_URL}/api/llama-advice", json=advice_data, timeout=100)
                end_time = time.time()
                
                response_time = end_time - start_time
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        advice = result.get("advice", "")
                        print(f"✅ Success! ({response_time:.2f}s)")
                        print(f"📝 Advice preview: {advice[:100]}...")
                        success_count += 1
                    else:
                        print(f"❌ Failed: {result.get('error')}")
                else:
                    print(f"❌ HTTP error: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Exception: {e}")
        
        print(f"\n� Integration test results: {success_count}/{len(test_goals)} successful")
        
        return success_count == len(test_goals)
        
    except Exception as e:
        print(f"�💥 Integration test error: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Starting Ollama Integration Diagnosis")
    print(f"⏰ Start time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        "ollama_direct": False,
        "flask_server": False,
        "integration": False
    }
    
    # 1. Direct Ollama test
    results["ollama_direct"] = test_ollama_direct()
    
    # 2. Flask server test
    if results["ollama_direct"]:
        results["flask_server"] = test_flask_server()
        
        # 3. Integration test
        if results["flask_server"]:
            results["integration"] = test_integration()
    
    # Final results
    print_header("Final Diagnosis Results")
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        test_english = {
            "ollama_direct": "Direct Ollama Connection",
            "flask_server": "Flask Server Integration", 
            "integration": "Full Integration Test"
        }
        print(f"{test_english[test_name]}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 All tests passed! System is working correctly.")
        print("🚀 Ready to connect with frontend.")
    else:
        print("\n⚠️ Some tests failed. Please resolve issues and try again.")
        
        print("\n💡 Troubleshooting guide:")
        if not results["ollama_direct"]:
            print("   1. Ollama server: Run 'ollama serve' command")
            print("   2. Install model: Run 'ollama pull llama3:latest' command")
        if not results["flask_server"]:
            print("   3. Flask server: Run 'python app_simple.py' command")
        if not results["integration"]:
            print("   4. Network: Check firewall and port settings")
    
    print(f"\n⏰ Completion time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
        # 1. Flask 서버 상태 확인
        print("🚀 Flask 서버 연결 확인...")
        response = requests.get(f"{FLASK_URL}/api/health", timeout=10)
        
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Flask 서버 연결 성공!")
            print(f"📊 상태: {health_data.get('status')}")
            print(f"💬 메시지: {health_data.get('message')}")
            
            # 2. Ollama 상태 확인 (Flask를 통해)
            print("\n🦙 Flask를 통한 Ollama 상태 확인...")
            response = requests.get(f"{FLASK_URL}/api/ollama-status", timeout=10)
            
            if response.status_code == 200:
                ollama_status = response.json()
                print(f"🔗 Ollama 상태: {ollama_status.get('status')}")
                print(f"📋 사용 가능한 모델: {ollama_status.get('available_models', [])}")
                print(f"🤖 현재 모델: {ollama_status.get('current_model')}")
                print(f"✅ 모델 사용 가능: {ollama_status.get('model_available')}")
                
                # 3. 조언 API 테스트
                print("\n🧠 조언 API 테스트...")
                test_goal = "daily exercise routine"
                advice_data = {"goal": test_goal}
                
                print(f"🎯 테스트 목표: '{test_goal}'")
                print("⏱️ 조언 생성 중 (최대 90초 대기)...")
                
                start_time = time.time()
                response = requests.post(f"{FLASK_URL}/api/llama-advice", json=advice_data, timeout=100)
                end_time = time.time()
                
                response_time = end_time - start_time
                print(f"⏱️ 총 응답 시간: {response_time:.2f}초")
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        advice = result.get("advice", "")
                        print("✅ 조언 API 성공!")
                        print(f"📏 조언 길이: {len(advice)}자")
                        print(f"📝 생성된 조언:\n{advice}")
                        return True
                    else:
                        print(f"❌ 조언 API 실패: {result.get('error')}")
                        return False
                else:
                    print(f"❌ 조언 API HTTP 오류: {response.status_code}")
                    print(f"📄 오류 내용: {response.text}")
                    return False
                    
            else:
                print(f"❌ Ollama 상태 확인 실패: {response.status_code}")
                print(f"📄 오류 내용: {response.text}")
                return False
                
        else:
            print(f"❌ Flask 서버 연결 실패: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Flask 서버에 연결할 수 없습니다.")
        print("💡 해결 방법:")
        print("   1. 'python app.py' 명령으로 Flask 서버를 시작하세요")
        print("   2. 포트 5000이 사용 가능한지 확인하세요")
        return False
    except requests.exceptions.Timeout:
        print("⏰ Flask 서버 응답 시간 초과")
        return False
    except Exception as e:
        print(f"💥 예상치 못한 오류: {e}")
        return False

def test_integration():
    """전체 통합 테스트"""
    print_header("전체 시스템 통합 테스트")
    
    test_cases = [
        {"goal": "learn Python programming", "description": "프로그래밍 학습"},
        {"goal": "start a meditation practice", "description": "명상 연습"},
        {"goal": "improve sleep quality", "description": "수면 개선"},
    ]
    
    success_count = 0
    total_tests = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        goal = test_case["goal"]
        description = test_case["description"]
        
        print(f"\n🧪 테스트 케이스 {i}/{total_tests}: {description}")
        print(f"🎯 목표: '{goal}'")
        
        try:
            start_time = time.time()
            response = requests.post(
                f"{FLASK_URL}/api/llama-advice",
                json={"goal": goal},
                timeout=60
            )
            end_time = time.time()
            
            response_time = end_time - start_time
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    advice = result.get("advice", "")
                    print(f"✅ 성공! (응답 시간: {response_time:.2f}초)")
                    print(f"📏 조언 길이: {len(advice)}자")
                    success_count += 1
                else:
                    print(f"❌ 실패: {result.get('error')}")
            else:
                print(f"❌ HTTP 오류: {response.status_code}")
                
        except Exception as e:
            print(f"💥 오류: {e}")
    
    print(f"\n📊 통합 테스트 결과: {success_count}/{total_tests} 성공")
    return success_count == total_tests

def main():
    """메인 함수"""
    print("🧪 Space Fantasy Todo Backend 진단 시작")
    print(f"⏰ 시작 시간: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        "ollama_direct": False,
        "flask_server": False,
        "integration": False
    }
    
    # 1. Ollama 직접 테스트
    results["ollama_direct"] = test_ollama_direct()
    
    # 2. Flask 서버 테스트
    if results["ollama_direct"]:
        results["flask_server"] = test_flask_server()
        
        # 3. 통합 테스트
        if results["flask_server"]:
            results["integration"] = test_integration()
    
    # 최종 결과
    print_header("최종 진단 결과")
    
    for test_name, result in results.items():
        status = "✅ 통과" if result else "❌ 실패"
        test_korean = {
            "ollama_direct": "Ollama 직접 연결",
            "flask_server": "Flask 서버 연동", 
            "integration": "전체 통합 테스트"
        }
        print(f"{test_korean[test_name]}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 모든 테스트 통과! 시스템이 정상적으로 작동합니다.")
        print("🚀 프론트엔드와 연결할 준비가 완료되었습니다.")
    else:
        print("\n⚠️ 일부 테스트 실패. 문제를 해결하고 다시 시도하세요.")
        
        print("\n💡 문제 해결 가이드:")
        if not results["ollama_direct"]:
            print("   1. Ollama 서버: 'ollama serve' 명령 실행")
            print("   2. 모델 설치: 'ollama pull llama3:latest' 명령 실행")
        if not results["flask_server"]:
            print("   3. Flask 서버: 'python app.py' 명령 실행")
        if not results["integration"]:
            print("   4. 네트워크: 방화벽 및 포트 설정 확인")
    
    print(f"\n⏰ 완료 시간: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
