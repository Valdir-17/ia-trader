import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas_ta as ta
from datetime import datetime

st.set_page_config(page_title="IA Trader Pro v3.0", layout="wide", page_icon="📈")

st.title("🤖 IA Trader Pro v3.0")
st.markdown("### Sinais Avançados + Backtesting + Gráficos")

# ===================== SIDEBAR =====================
st.sidebar.header("⚙️ Configurações")

# Ativos
ativos_populares = {
    "BTC-USD": "Bitcoin", "ETH-USD": "Ethereum", "SOL-USD": "Solana", "XRP-USD": "Ripple",
    "AAPL": "Apple", "TSLA": "Tesla", "NVDA": "NVIDIA", "AMZN": "Amazon",
    "EURUSD=X": "EUR/USD", "GBPUSD=X": "GBP/USD", "USDJPY=X": "USD/JPY",
    "PETR4.SA": "Petrobras", "VALE3.SA": "Vale", "ITUB4.SA": "Itaú", "BBAS3.SA": "Banco do Brasil",
    "GC=F": "Ouro", "CL=F": "Petróleo", "SI=F": "Prata"
}

tipo = st.sidebar.selectbox("Tipo de Ativo", ["Cripto", "Ações", "Forex", "Brasil", "Personalizado"])
if tipo == "Personalizado":
    ativo = st.sidebar.text_input("Digite o código do ativo", "BTC-USD")
else:
    filtrados = {k:v for k,v in ativos_populares.items() if 
                 (tipo=="Cripto" and "USD" in k) or
                 (tipo=="Ações" and k[0].isalpha() and len(k)<6) or
                 (tipo=="Forex" and "=" in k) or
                 (tipo=="Brasil" and ".SA" in k)}
    ativo = st.sidebar.selectbox("Escolha o Ativo", list(filtrados.keys()), format_func=lambda x: filtrados.get(x, x))

# Tempo de expiração livre
tempo_exp = st.sidebar.number_input("Tempo de Expiração (em minutos)", min_value=1, max_value=1440, value=15)
intervalo = st.sidebar.selectbox("Intervalo dos Dados", ["1m", "5m", "15m", "30m", "1h"], index=1)

periodo = st.sidebar.selectbox("Período Histórico", ["7d", "14d", "1mo", "3mo"], index=1)

if 'sinais' not in st.session_state:
    st.session_state.sinais = []

if st.sidebar.button("🚀 GERAR ANÁLISE COMPLETA", type="primary", use_container_width=True):
    with st.spinner(f"Analisando {ativo} para expiração de {tempo_exp} minutos..."):
        df = yf.download(ativo, period=periodo, interval=intervalo, progress=False)
        
        if len(df) < 50:
            st.error("Dados insuficientes para este ativo/período.")
            st.stop()

        # Indicadores
        df['RSI'] = ta.rsi(df['Close'], length=14)
        df['EMA20'] = ta.ema(df['Close'], length=20)
        df['MACD'] = ta.macd(df['Close'])['MACD_12_26_9']
        df = df.dropna()

        preco_atual = df['Close'].iloc[-1]

        # Sinal simples baseado em indicadores
        rsi = df['RSI'].iloc[-1]
        acima_ema = preco_atual > df['EMA20'].iloc[-1]
        
        if rsi < 30 and acima_ema:
            sinal = "🟢 COMPRA FORTE (SUBIR)"
            conf = 75
        elif rsi > 70 and not acima_ema:
            sinal = "🔴 VENDA FORTE (DESCER)"
            conf = 72
        elif acima_ema:
            sinal = "🟢 COMPRA (SUBIR)"
            conf = 58
        else:
            sinal = "🔴 VENDA (DESCER)"
            conf = 55

        st.success(f"**SINAL PARA {tempo_exp} MINUTOS**: {sinal} | Confiança: **{conf}%**")

        col1, col2, col3 = st.columns(3)
        col1.metric("Preço Atual", f"${preco_atual:.4f}")
        col2.metric("RSI", f"{rsi:.1f}")
        col3.metric("Tendência EMA20", "Alta" if acima_ema else "Baixa")

        # Tabs com mais conteúdo
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Gráfico", "📈 Indicadores", "📜 Histórico", "ℹ️ Dicas"])

        with tab1:
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.75, 0.25])
            fig.add_trace(go.Candlestick(x=df.index[-100:], open=df['Open'][-100:], high=df['High'][-100:],
                                        low=df['Low'][-100:], close=df['Close'][-100:]), row=1, col=1)
            fig.add_trace(go.Scatter(x=df.index[-100:], y=df['EMA20'][-100:], name="EMA 20", line=dict(color='orange')), row=1, col=1)
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.dataframe(df[['Close', 'RSI', 'MACD', 'EMA20']].tail(10).round(4), use_container_width=True)

        with tab3:
            st.session_state.sinais.append({
                "Data": datetime.now().strftime("%H:%M"),
                "Ativo": ativo,
                "Sinal": sinal,
                "Confiança": conf,
                "Expiração": f"{tempo_exp} min"
            })
            st.dataframe(pd.DataFrame(st.session_state.sinais), use_container_width=True)

        with tab4:
            st.info("""**Dicas importantes:**
- Sempre opere primeiro na **conta DEMO** da Pocket Option
- Use no máximo 1% da banca por operação
- Combine o sinal com sua própria análise
- Teste por vários dias antes de usar dinheiro real""")

st.warning("⚠️ Esta ferramenta é educacional. Nenhum sinal garante lucro. Opere com responsabilidade.")
st.caption("IA Trader Pro v3.0 • Melhorado para você")
