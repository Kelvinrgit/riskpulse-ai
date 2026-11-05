# 📊 RiskPulse AI | Monitor de Volatilidade e Inteligência Financeira

Ferramenta de inteligência quantitativa desenvolvida para a trilha **Finanças - AI Builder**, combinando modelagem estatística de séries temporais e IA Generativa para transformar dados voláteis de mercado em relatórios executivos acionáveis.

---

## 🚀 Sobre o Projeto
Em ambientes corporativos e de tesouraria, a alta volatilidade de ativos e moedas impacta diretamente o planejamento financeiro, o custo de capital e a exposição a riscos. O **RiskPulse AI** elimina a lacuna entre o rigor analítico dos modelos quantitativos e a velocidade de tomada de decisão executiva. 

A aplicação automatiza a ingestão de dados de mercado, calcula métricas complexas de risco (VaR, Volatilidade Anualizada, Drawdown) e utiliza a API do Google Gemini para atuar como um agente analista, redigindo diagnósticos e recomendações de negócio sob medida para perfis de Tesouraria, FP&A ou Gestão de Riscos.

---

## 🛠️ Tecnologias e Stack Utilizada
* **Python**: Linguagem principal para o pipeline de dados.
* **Streamlit**: Framework para construção do dashboard interativo e deploy web.
* **yfinance & Pandas & NumPy**: Extração automatizada de séries temporais, cálculo de retornos logarítmicos e estatísticas descritivas.
* **Plotly**: Visualização de dados dinâmica com limiares de regime de volatilidade.
* **Google GenAI SDK (Gemini)**: Engenharia de prompt estruturada para *Data-to-Text* e geração de pareceres executivos.

---

## 📈 Funcionalidades Principais
1. **Motor Quantitativo Robusto**: Calcula volatilidade móvel com janela configurável, retornos logarítmicos, Value at Risk (VaR Histórico a 95%) e Maximum Drawdown.
2. **Classificação de Regimes de Mercado**: Identifica automaticamente se o ativo está em zona de estresse (Percentil 80), compressão (Percentil 20) ou normalidade.
3. **Agente Executivo Customizável**: Injeta os dados estatísticos calculados em um prompt de sistema especializado, permitindo alternar a ótica analítica entre *Tesouraria Corporativa*, *Planejamento Financeiro (FP&A)* e *Risco Atuarial*.
4. **Interface Pronta para Produção**: Dashboard limpo, responsivo e integrado com gráficos interativos de preços e volatilidade.

---

## ⚙️ Como Executar o Projeto Localmente

Siga os passos abaixo para clonar e rodar a aplicação na sua máquina:

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/SEU-USUARIO/riskpulse-ai.git
   cd riskpulse-ai
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv venv
   # No Windows:
   venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação Streamlit:**
   ```bash
   streamlit run app.py
   ```

5. Acesse o painel localmente no seu navegador através do endereço `http://localhost:8501`.

---

## 🔑 Configuração de Acesso à IA
Para utilizar o recurso de relatórios gerados por IA, insira sua chave de API do Google Gemini (gratuita no [Google AI Studio](https://aistudio.google.com)) na barra lateral da aplicação.

---
*Desenvolvido com foco em automação, pragmatismo e inteligência de dados aplicada a negócios.*