# Multi-Agent Stock Analysis Team

## 개요
다단계 논리적 추론을 활용한 주식 분석 에이전트 팀 구현

## 무료 API 사용 관련

이 프로젝트 수행 과정에서 다양한 무료 API를 시도했습니다:
- **Ollama (로컬)**: 로컬 모델은 tool calling 미지원 → deepagents 사용 불가능
- **OpenAI**: 유료, 무료 티어 제한적
- **Anthropic (Claude)**: 무료 티어 있으나 카드 필요
- **Google Gemini**: 무료 할당량 초과 (quota exceeded)
- **Groq API**: 무료 티어 사용 가능 (30 RPM, 6000 TPM, 카드 불필요)

=> 다양한 무료 API 시도했으나 모두 제한이 있어 **Groq API**로 구현

## 분석 지표 (stock_agent.py lines 138-140 참조)

Fundamental Agent에서 분석하는 핵심 지표:
- **P/E ratio**: 주가수익비율
- **P/B ratio**: 주가순자산비율  
- **EPS**: 주당순이익
- **Dividend yield**: 배당수익률

---

## 에이전트 목표

4개 이상의 서브에이전트를 활용하여 종합적인 주식 분석 수행:
- 최신 뉴스 및 시장 정보 수집
- 기술적 분석 (차트, 지표)
- 기본적 분석 (재무제표, 가치평가)
- 포트폴리오 권장 사항 생성

## 동작원리

### 아키텍처
```
┌─────────────────┐
│  사용자 입력     │ (주식 심볼 입력)
└────────┬────────┘
         ▼
┌─────────────────┐
│  리서치 에이전트 │ ──► 최신 뉴스, 시장 심리
└────────┬────────┘
         ▼
┌─────────────────┐
│  기술적 분석     │ ──► RSI, MACD, 지지/저항선
└────────┬────────┘
         ▼
┌─────────────────┐
│  기본적 분석     │ ──► P/E, EPS, 재무제표
└────────┬────────┘
         ▼
┌─────────────────┐
│  포트폴리오 관리 │ ──► 종합 투자 권장
└────────┬────────┘
         ▼
┌─────────────────┐
│  최종 결과       │ (Buy/Hold/Sell 권장)
└─────────────────┘
```

### 기술 스택
- **LangGraph**: Multi-agent 워크플로우 구성
- **Groq API**: Llama 3.3 70B 모델 (무료 티어)
- **Python**: 3.14

### 사용된 무료 API
- **Groq API**: https://console.groq.com
  - 무료 티어: 30 RPM, 6000 TPM
  - 카드 불필요

---

## 실행결과

### 실행 예시
```
============================================================
MULTI-AGENT STOCK ANALYSIS TEAM
Using LangGraph with Groq API (Llama 3.3 70B)
============================================================

분석할 주식 심볼을 입력하세요 (예: AAPL, TSLA, GOOGL): AAPL

============================================================
Starting Multi-Agent Stock Analysis for: AAPL
============================================================

[Research Agent] Gathering latest news and information...
[Research Agent] Completed. Summary length: 1501 chars
[Technical Analysis Agent] Analyzing price patterns...
[Technical Analysis Agent] Completed. Summary length: 1405 chars
[Fundamental Analysis Agent] Analyzing financials...
[Fundamental Analysis Agent] Completed. Summary length: 1967 chars
[Portfolio Manager] Synthesizing recommendations...
[Portfolio Manager] Completed.

============================================================
Final Investment Recommendation for AAPL
============================================================

**종합적인 투자 권장 사항**

애플(AAPL) 주식에 대한 종합적인 분석을 기반으로, 다음과 같은 투자 권장 사항을 제공합니다.

1. 전반적인 권장: 보유
2. 권장 이유 - 지속적인 성장, 안정적인 재무 구조
3. 리스크 요인 - 경쟁, 기술 발전, 경제적 불확실성
4. 권장 포지션 크기 - 5%~10%
5. 목표가 - 180~200달러, 투자 기간 6~12개월
```

---

## 코드

### 파일 구조
```
mid_project/
├── stock_agent.py    # 메인 에이전트 코드
└── venv/             # 가상환경
```

### 핵심 코드 설명

1. **에이전트 정의**: 각 에이전트는 고유한 시스템 프롬프트 보유
2. **LangGraph 워크플로우**: 순차적 노드 실행 (Research → Technical → Fundamental → Portfolio)
3. **상태 관리**: AgentState로 에이전트 간 데이터 전달

### 실행 방법
```bash
# 가상환경 활성화
source venv/bin/activate

# 실행
python stock_agent.py

# 입력 예시
AAPL
```

---

## GitHub 업로드 방법

```bash
git init
git add .
git commit -m "Initial commit: Multi-Agent Stock Analysis Team"
git remote add origin https://github.com/[username]/stock-agent.git
git push -u origin main
```

업로드 후 URL: `https://github.com/[username]/stock-agent`
