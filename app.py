import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from google import genai

# Configuração da página
st.set_page_config(page_title="RiskPulse AI | Monitor de Volatilidade", layout="wide")

st.title("📊 RiskPulse AI: Monitor de Volatilidade e Regimes de Mercado")
st.markdown("Ferramenta de inteligência quantitativa que combina modelagem de séries temporais e IA Generativa para suporte à decisão corporativa.")

# Barra lateral de configurações
with st.sidebar:
    st.header("⚙️ Parâmetros de Análise")
    api_key = st.text_input("Chave da API (Google Gemini):", type="password", help="Obtenha gratuitamente no Google AI Studio.")
    ticker = st.text_input("Ticker do Ativo / Índice:", value="BRL=X", help="Ex: BRL=X (Dólar), ^BVSP (Ibovespa), ITUB4.SA, MELI, PETR4.SA")
    periodo = st.selectbox("Janela Histórica:", options=["1y", "2y", "5y"], index=1)
    janela_vol = st.slider("Janela Móvel de Volatilidade (dias úteis):", min_value=10, max_value=63, value=21)
    perfil_executivo = st.selectbox(
        "Ótica do Relatório Executivo:",
        options=[
            "Tesouraria Corporativa (Hedge e Caixa)",
            "Planejamento Financeiro (FP&A e Orçamento)",
            "Gestão de Risco Atuarial e Solvência"
        ]
    )
    gerar_analise = st.button("🚀 Executar Pipeline e Gerar Resumo IA", use_container_width=True)

@st.cache_data(ttl=3600)
def carregar_e_processar_dados(ticker_symbol, period_str, vol_window):
    df = yf.download(ticker_symbol, period=period_str, progress=False)
    if df.empty:
        return None
    
    # Tratamento para colunas MultiIndex do yfinance
    if isinstance(df.columns, pd.MultiIndex):
        close_series = df['Close'][ticker_symbol]
    else:
        close_series = df['Close']
        
    dados = pd.DataFrame({'Close': close_series}).dropna()
    
    # Retornos logarítmicos diários
    dados['Log_Return'] = np.log(dados['Close'] / dados['Close'].shift(1))
    
    # Volatilidade móvel anualizada (252 dias úteis)
    dados['Vol_Anualizada'] = dados['Log_Return'].rolling(window=vol_window).std() * np.sqrt(252) * 100
    
    # Drawdown histórico
    pico_acumulado = dados['Close'].cummax()
    dados['Drawdown'] = ((dados['Close'] - pico_acumulado) / pico_acumulado) * 100
    
    return dados.dropna()

dados = carregar_e_processar_dados(ticker, periodo, janela_vol)

if dados is None or len(dados) < 30:
    st.error("Não foi possível carregar dados suficientes para o ticker informado. Verifique o código do ativo.")
else:
    # Extração de métricas quantitativas para o contexto do LLM
    preco_atual = float(dados['Close'].iloc[-1])
    retorno_periodo = float(((dados['Close'].iloc[-1] / dados['Close'].iloc[0]) - 1) * 100)
    vol_atual = float(dados['Vol_Anualizada'].iloc[-1])
    vol_media = float(dados['Vol_Anualizada'].mean())
    vol_p80 = float(np.percentile(dados['Vol_Anualizada'], 80))
    vol_p20 = float(np.percentile(dados['Vol_Anualizada'], 20))
    var_95 = float(np.percentile(dados['Log_Return'], 5) * 100)
    max_dd = float(dados['Drawdown'].min())

    # Classificação de Regime de Volatilidade
    if vol_atual >= vol_p80:
        regime = "Estresse / Alta Volatilidade (Acima do Percentil 80)"
    elif vol_atual <= vol_p20:
        regime = "Baixa Volatilidade / Compressão (Abaixo do Percentil 20)"
    else:
        regime = "Normalidade / Volatilidade Moderada"

    # Painel de KPIs Quantitativos
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Cotação Atual", f"{preco_atual:,.2f}")
    col2.metric("Volatilidade Atual (Anual.)", f"{vol_atual:.2f}%", f"{vol_atual - vol_media:+.2f}% vs Média", delta_color="inverse")
    col3.metric("Volatilidade Média Hist.", f"{vol_media:.2f}%")
    col4.metric("VaR Diário (95% Hist.)", f"{var_95:.2f}%")
    col5.metric("Max Drawdown", f"{max_dd:.2f}%")

    st.info(f"**Regime de Mercado Detectado:** {regime}")

    # Gráficos Interativos (Preço + Volatilidade com Bandas de Regime)
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        vertical_spacing=0.08,
        subplot_titles=(f"Série Histórica de Preços ({ticker})", f"Volatilidade Móvel Anualizada ({janela_vol}d) e Limiares de Regime"),
        row_heights=[0.55, 0.45]
    )

    fig.add_trace(go.Scatter(x=dados.index, y=dados['Close'], name="Preço", line=dict(color="#1f77b4", width=2)), row=1, col=1)
    fig.add_trace(go.Scatter(x=dados.index, y=dados['Vol_Anualizada'], name="Volatilidade Anualizada (%)", line=dict(color="#ff7f0e", width=2)), row=2, col=1)
    
    # Linhas de referência na volatilidade
    fig.add_hline(y=vol_p80, line_dash="dash", line_color="red", annotation_text="Limiar de Estresse (P80)", row=2, col=1)
    fig.add_hline(y=vol_media, line_dash="dot", line_color="gray", annotation_text="Média Histórica", row=2, col=1)

    fig.update_layout(height=550, margin=dict(l=20, r=20, t=40, b=20), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # Seção do Agente de IA (Executive Summary)
    st.subheader("🤖 AI Executive Summary & Recomendações de Negócio")
    
    if gerar_analise:
        if not api_key:
            st.warning("Por favor, insira sua chave de API do Google Gemini na barra lateral para gerar o relatório executivo.")
        else:
            with st.spinner("Analisando métricas quantitativas e redigindo diagnóstico executivo..."):
                try:
                    client = genai.Client(api_key=api_key)
                    
                    prompt = f"""
                    Você é um Especialista Sênior em Risco Quantitativo e Inteligência Financeira.
                    Analise os indicadores estatísticos extraídos agora da série temporal do ativo/índice '{ticker}' (janela de {periodo}) e elabore um Relatório Executivo direcionado para a área de: {perfil_executivo}.

                    DADOS QUANTITATIVOS EXTRAÍDOS DO MOTOR ESTATÍSTICO:
                    - Cotação Atual: {preco_atual:.2f} (Retorno acumulado no período: {retorno_periodo:.2f}%)
                    - Volatilidade Móvel Atual ({janela_vol} dias úteis, anualizada): {vol_atual:.2f}%
                    - Volatilidade Média Histórica no Período: {vol_media:.2f}%
                    - Limiar de Estresse (Percentil 80): {vol_p80:.2f}% | Limiar de Baixa Volatilidade (Percentil 20): {vol_p20:.2f}%
                    - Classificação Atual do Regime: {regime}
                    - Value at Risk (VaR Histórico Diário 95%): {var_95:.2f}%
                    - Maximum Drawdown registrado na janela: {max_dd:.2f}%

                    ESTRUTURA OBRIGATÓRIA DA RESPOSTA (seja direto, analítico e sem jargões vazios):
                    1. **Diagnóstico do Regime de Volatilidade**: Interprete o estado atual da volatilidade em relação à média e ao percentil 80, explicando o que o VaR diário indica sobre o risco de cauda imediato.
                    2. **Impacto Prático para {perfil_executivo}**: Como esse comportamento específico do ativo afeta caixa, previsibilidade orçamentária, custo de oportunidade ou exposição a risco hoje.
                    3. **Plano de Ação Recomendado (3 pontos)**: Recomende 3 diretrizes táticas e objetivas baseadas nos números acima.
                    """

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt
                    )
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Erro ao conectar com a API de IA: {e}")
    else:
        st.caption("Configure os parâmetros à esquerda e clique em **Executar Pipeline e Gerar Resumo IA** para produzir o parecer executivo.")
