# Todo 앱 백엔드 서버 (Ollama Llama3 연동)

이 백엔드 서버는 React 프론트엔드와 Ollama Llama3 모델을 연결하는 Flask 기반 API 서버입니다.

## 주요 기능

- **Ollama Llama3 연동**: 로컬에서 실행되는 Ollama Llama3 모델과 통신
- **AI 조언 API**: 사용자의 목표에 대한 실질적인 AI 조언 제공
- **CORS 지원**: React 프론트엔드에서 API 호출 가능
- **Ollama 상태 모니터링**: Ollama 서버 연결 상태 확인

## 사전 요구사항

1. **Ollama 설치**: https://ollama.ai/download
2. **Llama3 모델 다운로드**:
   ```bash
   ollama pull llama3
   ```
3. **Ollama 서버 실행**:
   ```bash
   ollama serve
   ```

## 설치 및 실행

1. Python 가상환경 생성 (권장):

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

2. 의존성 설치:

```bash
pip install -r requirements.txt
```

3. Ollama 서버 실행 확인:

```bash
ollama serve
```

4. Flask 서버 실행:

```bash
python app.py
```

## API 엔드포인트

### POST /api/llama-advice

사용자의 목표에 대한 Llama3 조언을 제공합니다.

**요청 예시:**

```json
{
  "goal": "매일 운동하기"
}
```

**응답 예시:**

```json
{
  "success": true,
  "advice": "🏃‍♂️ 매일 운동하는 목표를 달성하기 위해서는...\n\n1. 구체적인 행동 계획:\n- 아침 7시에 30분간 조깅\n- 주 3회는 헬스장 방문\n- 주말에는 등산이나 자전거 타기\n\n2. 주의할 점:\n- 급격한 강도 증가는 부상 위험\n- 충분한 휴식과 수분 섭취 필요\n\n3. 동기부여 방법:\n- 운동 일지 작성\n- 친구와 함께 운동하기\n- 작은 목표부터 달성하며 성취감 느끼기\n\n4. 성공 팁:\n- 일정한 시간에 운동하여 습관화\n- 다양한 운동으로 지루함 방지\n- 운동 후 자신에게 보상 주기 🎯"
}
```

### GET /api/ollama-status

Ollama 서버 연결 상태를 확인합니다.

**응답 예시:**

```json
{
  "status": "connected",
  "message": "Ollama 서버가 정상적으로 실행 중입니다.",
  "available_models": ["llama3", "codellama"],
  "current_model": "llama3",
  "model_available": true
}
```

### GET /api/health

Flask 서버 상태를 확인합니다.

**응답 예시:**

```json
{
  "status": "healthy",
  "message": "Flask 서버가 정상적으로 실행 중입니다.",
  "endpoints": {
    "llama_advice": "/api/llama-advice",
    "ollama_status": "/api/ollama-status",
    "health": "/api/health"
  }
}
```

## 설정

### Ollama 설정

- **Ollama URL**: `http://localhost:11434` (기본값)
- **모델**: `llama3`
- **포트**: 11434 (Ollama 기본 포트)

### Flask 설정

- **포트**: 5000
- **호스트**: 0.0.0.0 (모든 인터페이스)

## 문제 해결

### 1. Ollama 서버 연결 오류

```
Ollama 서버에 연결할 수 없습니다.
```

**해결책**:

- `ollama serve` 명령으로 Ollama 서버 시작
- 포트 11434가 사용 가능한지 확인

### 2. 모델 없음 오류

```
model "llama3" not found
```

**해결책**:

- `ollama pull llama3` 명령으로 모델 다운로드

### 3. 응답 시간 초과

```
Ollama API 호출 시간이 초과되었습니다.
```

**해결책**:

- 더 강력한 하드웨어 사용
- 모델 설정에서 max_tokens 값 조정

## 아키텍처

```
Frontend (React) → Flask API → Ollama API → Llama3 Model
     ↓                ↓            ↓            ↓
  사용자 입력    →   조언 요청   →   AI 처리   →   조언 생성
```

## 개발 모드

개발 중에는 다음 명령으로 실시간 변경사항 확인 가능:

```bash
flask --app app.py --debug run
```
