# Todo 앱 백엔드 서버

이 백엔드 서버는 React 프론트엔드와 함께 동작하는 Flask 기반 API 서버입니다.

## 주요 기능

- **Llama3 조언 API**: 사용자의 목표에 대한 AI 조언 제공
- **CORS 지원**: React 프론트엔드에서 API 호출 가능
- **목표별 맞춤 조언**: 운동, 공부, 독서, 다이어트, 코딩 등 카테고리별 조언

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

3. 서버 실행:

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
  "advice": "💪 운동을 시작하려면 먼저 작은 목표부터 설정하세요. 매일 10분씩 걷기부터 시작해보세요."
}
```

### GET /api/health

서버 상태를 확인합니다.

**응답 예시:**

```json
{
  "status": "healthy",
  "message": "Flask 서버가 정상적으로 실행 중입니다."
}
```

## 실제 Llama3 연동

현재는 시뮬레이션 모드로 동작하고 있습니다. 실제 Llama3 모델을 사용하려면 `simulate_llama3_advice` 함수를 실제 Llama3 API 호출로 대체해야 합니다.

## 포트 설정

- 백엔드 서버: http://localhost:5000
- 프론트엔드 개발 서버: http://localhost:3000
