"""
Multi-Agent Stock Analysis Team using LangGraph with Groq API
4 Sub-agents + 1 Coordinator for multi-step logical reasoning
"""

import os
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from typing import TypedDict, List, Annotated
import operator
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.tools import tool

GROQ_API_KEY = os.environ.get(
    "GROQ_API_KEY", ""
)  # Set via: export GROQ_API_KEY="your_key"

llama_model = ChatOpenAI(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)


class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    stock_symbol: str
    research_summary: str
    technical_summary: str
    fundamental_summary: str
    final_recommendation: str
    step: str


research_system = """You are a Stock Research Analyst. Your role is to search and gather the latest news, 
market sentiment, and relevant information about specific stocks or the overall market.
Provide comprehensive news summaries and market context.
Focus on: recent news, market sentiment, competitor analysis, industry trends.
Always respond in Korean."""

technical_system = """You are a Technical Analysis Expert. Your role is to analyze stock price movements 
and chart patterns. Provide technical insights including:
- Trend analysis (uptrend, downtrend, sideways)
- Support and resistance levels
- Key technical indicators (RSI, MACD, Moving Averages)
- Chart patterns and signals
Always respond in Korean."""

fundamental_system = """You are a Fundamental Analysis Expert. Your role is to analyze a company's 
financial health and intrinsic value. Focus on:
- Financial statements analysis (revenue, earnings, cash flow)
- Key metrics (P/E ratio, P/B ratio, EPS, Dividend yield)
- Growth indicators and projections
- Industry comparison and valuation
Always respond in Korean."""

portfolio_system = """You are a Portfolio Manager. Your role is to synthesize analysis from other agents 
and provide portfolio-level recommendations. Consider:
- Risk management and diversification
- Asset allocation strategies
- Position sizing recommendations
- Entry/exit points
- Overall investment thesis
Provide clear, actionable portfolio recommendations.
Always respond in Korean."""


def create_agent_node(system_prompt, agent_name):
    def node(state: AgentState):
        messages = state["messages"]
        stock = state["stock_symbol"]

        full_prompt = f"{system_prompt}\n\n주식 심볼: {stock}"

        response = llama_model.invoke([HumanMessage(content=full_prompt)] + messages)

        return {"messages": [response]}

    return node


def research_node(state: AgentState):
    print("[Research Agent] Gathering latest news and information...")
    stock = state["stock_symbol"]

    prompt = f"""Search and summarize the latest news and market information about stock: {stock}

Include:
- Recent news and events
- Market sentiment and investor outlook
- Competitor analysis
- Industry trends"""

    response = llama_model.invoke([HumanMessage(content=prompt)])
    summary = response.content

    print(f"[Research Agent] Completed. Summary length: {len(summary)} chars")

    return {
        "messages": [response],
        "research_summary": summary,
        "step": "research_complete",
    }


def technical_node(state: AgentState):
    print("[Technical Analysis Agent] Analyzing price patterns...")
    stock = state["stock_symbol"]

    prompt = f"""Provide technical analysis for stock: {stock}

Include:
- Trend analysis (uptrend/downtrend/sideways)
- Support and resistance levels
- Key technical indicators (RSI, MACD, Moving Averages)
- Chart patterns and signals"""

    response = llama_model.invoke([HumanMessage(content=prompt)])
    summary = response.content

    print(f"[Technical Analysis Agent] Completed. Summary length: {len(summary)} chars")

    return {
        "messages": [response],
        "technical_summary": summary,
        "step": "technical_complete",
    }


def fundamental_node(state: AgentState):
    print("[Fundamental Analysis Agent] Analyzing financials...")
    stock = state["stock_symbol"]

    prompt = f"""Provide fundamental analysis for stock: {stock}

Include:
- Financial statements analysis (revenue, earnings, cash flow)
- Key metrics (P/E ratio, P/B ratio, EPS, Dividend yield)
- Growth indicators and projections
- Industry comparison and valuation"""

    response = llama_model.invoke([HumanMessage(content=prompt)])
    summary = response.content

    print(
        f"[Fundamental Analysis Agent] Completed. Summary length: {len(summary)} chars"
    )

    return {
        "messages": [response],
        "fundamental_summary": summary,
        "step": "fundamental_complete",
    }


def portfolio_node(state: AgentState):
    print("[Portfolio Manager] Synthesizing recommendations...")
    stock = state["stock_symbol"]
    research = state.get("research_summary", "")
    technical = state.get("technical_summary", "")
    fundamental = state.get("fundamental_summary", "")

    prompt = f"""Based on the following analyses, provide a comprehensive investment recommendation for {stock}:

RESEARCH ANALYSIS:
{research}

TECHNICAL ANALYSIS:
{technical}

FUNDAMENTAL ANALYSIS:
{fundamental}

Provide:
1. Overall recommendation (Buy/Hold/Sell)
2. Key reasons for the recommendation
3. Risk factors to consider
4. Suggested position size
5. Target price and time horizon"""

    response = llama_model.invoke([HumanMessage(content=prompt)])
    recommendation = response.content

    print(f"[Portfolio Manager] Completed.")

    return {
        "messages": [response],
        "final_recommendation": recommendation,
        "step": "complete",
    }


def technical_node(state: AgentState):
    print("[Technical Analysis Agent] Analyzing price patterns...")
    stock = state["stock_symbol"]

    prompt = f"""다음 주식에 대한 기술적 분석을 제공해주세요: {stock}

다음 내용을 포함해주세요:
- 트렌드 분석 (상승趋势/하락趋势/횡보)
- 지지선과 저항선
- 주요 기술 지표 (RSI, MACD, 이동평균선)
- 차트 패턴 및 시그널

한국어로 상세하게 작성해주세요."""

    response = llama_model.invoke([HumanMessage(content=prompt)])
    summary = response.content

    print(f"[Technical Analysis Agent] Completed. Summary length: {len(summary)} chars")

    return {
        "messages": [response],
        "technical_summary": summary,
        "step": "technical_complete",
    }


def fundamental_node(state: AgentState):
    print("[Fundamental Analysis Agent] Analyzing financials...")
    stock = state["stock_symbol"]

    prompt = f"""다음 주식에 대한 기본적 분석을 제공해주세요: {stock}

다음 내용을 포함해주세요:
- 재무제표 분석 (매출, 이익, 현금흐름)
- 주요 지표 (P/E ratio, P/B ratio, EPS, 배당수익률)
- 성장 지표 및 전망
- 산업 비교 및 가치평가

한국어로 상세하게 작성해주세요."""

    response = llama_model.invoke([HumanMessage(content=prompt)])
    summary = response.content

    print(
        f"[Fundamental Analysis Agent] Completed. Summary length: {len(summary)} chars"
    )

    return {
        "messages": [response],
        "fundamental_summary": summary,
        "step": "fundamental_complete",
    }


def portfolio_node(state: AgentState):
    print("[Portfolio Manager] Synthesizing recommendations...")
    stock = state["stock_symbol"]
    research = state.get("research_summary", "")
    technical = state.get("technical_summary", "")
    fundamental = state.get("fundamental_summary", "")

    prompt = f"""다음 주식에 대한 종합적인 투자 권장 사항을 제공해주세요:

주식 심볼: {stock}

연구 분석:
{research}

기술적 분석:
{technical}

기본적 분석:
{fundamental}

다음 내용을 포함해주세요:
1. 전반적인 권장 (매수/보유/매도)
2. 권장 이유
3. 고려해야 할 리스크 요인
4. 권장 포지션 크기
5. 목표가 및 투자 기간

한국어로 상세하게 작성해주세요."""

    response = llama_model.invoke([HumanMessage(content=prompt)])
    recommendation = response.content

    print(f"[Portfolio Manager] Completed.")

    return {
        "messages": [response],
        "final_recommendation": recommendation,
        "step": "complete",
    }


def build_stock_analysis_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("research", research_node)
    workflow.add_node("technical", technical_node)
    workflow.add_node("fundamental", fundamental_node)
    workflow.add_node("portfolio", portfolio_node)

    workflow.set_entry_point("research")
    workflow.add_edge("research", "technical")
    workflow.add_edge("technical", "fundamental")
    workflow.add_edge("fundamental", "portfolio")
    workflow.add_edge("portfolio", END)

    return workflow.compile()


def analyze_stock(symbol: str):
    """Main function to analyze a stock using the multi-agent team."""

    print(f"\n{'=' * 60}")
    print(f"Starting Multi-Agent Stock Analysis for: {symbol}")
    print(f"{'=' * 60}\n")

    app = build_stock_analysis_graph()

    initial_state = {
        "messages": [],
        "stock_symbol": symbol,
        "research_summary": "",
        "technical_summary": "",
        "fundamental_summary": "",
        "final_recommendation": "",
        "step": "start",
    }

    result = app.invoke(initial_state)

    print(f"\n{'=' * 60}")
    print(f"Final Investment Recommendation for {symbol}")
    print(f"{'=' * 60}\n")
    print(result["final_recommendation"])

    return result


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("MULTI-AGENT STOCK ANALYSIS TEAM")
    print("Using LangGraph with Groq API (Llama 3.3 70B)")
    print("=" * 60 + "\n")

    symbol = (
        input("분석할 주식 심볼을 입력하세요 (예: AAPL, TSLA, GOOGL): ").strip().upper()
    )
    if not symbol:
        symbol = "AAPL"

    result = analyze_stock(symbol)
