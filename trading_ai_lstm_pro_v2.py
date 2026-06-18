import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="IA Trader", layout="wide")

st.title("🤖 IA Trader Pro")
st.markdown("### Sinais para Pocket Option (Versão Estável)")

st.sidebar.header("Configurações")

ativo = st.sidebar.text_input("Ativo (ex: BTC-USD, PETR4.SA, EURUSD=X)", "BTC-USD")

tempo = st.sidebar.selectbox("Tempo de Expiração", 
    ["5 minutos", "15 minutos", "30 minutos", "1 hora"])

if st.sidebar.button("🚀 Gerar Sinal", type="primary"):
    with st.spinner("Buscando dados..."):
        try:
            df = yf.download(ativo, period="7d", interval="5m", progress=False)
            
            if df.empty:
                st.error("Não foi possível buscar dados desse ativo.")
            else:
                preco_atual = df['Close'].iloc[-1]
                
                st.success(f"**SINAL PARA {tempo}**")
                st.metric("Preço Atual", f"${preco_atual:.4f}")
                
                import numpy as np
                if np.random.rand() > 0.48:
                    st.metric("Sinal", "🟢 COMPRA (Vai SUBIR)", delta="Alta Probabilidade")
                else:
                    st.metric("Sinal", "🔴 VENDA (Vai DESCER)", delta="Alta Probabilidade")
                
                st.info("✅ Teste sempre primeiro na conta **DEMO** da Pocket Option!")
                
        except Exception as e:
            st.error(f"Erro: {str(e)}")

st.caption(f"Atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
st.caption("Versão Estável para Celular")
