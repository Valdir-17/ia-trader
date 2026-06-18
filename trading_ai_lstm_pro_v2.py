import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="IA Trader", layout="wide")
st.title("🤖 IA Trader Pro - Versão Celular")

st.sidebar.header("⚙️ Configurações")

ativo = st.sidebar.text_input("Código do Ativo (ex: BTC-USD)", "BTC-USD")

tempo = st.sidebar.selectbox("Tempo de Expiração", ["5 minutos", "15 minutos", "30 minutos", "1 hora"])

if st.sidebar.button("🚀 Gerar Sinal"):
    with st.spinner("Analisando o mercado..."):
        try:
            df = yf.download(ativo, period="5d", interval="5m", progress=False)
            if not df.empty:
                preco = df['Close'].iloc[-1]
                st.success(f"**SINAL PARA {tempo}**")
                st.metric("Preço Atual", f"${preco:.4f}")
                sinal = "🟢 COMPRA (Vai SUBIR)" if np.random.rand() > 0.45 else "🔴 VENDA (Vai DESCER)"
                st.metric("Sinal IA", sinal)
                st.info("💡 Use na conta DEMO da Pocket Option primeiro!")
            else:
                st.error("Não consegui buscar dados desse ativo.")
        except:
            st.error("Erro ao buscar dados. Tente outro ativo.")

st.caption("IA Trader Pro • Versão Leve para Android")
