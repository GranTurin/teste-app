import streamlit as st
import pandas as pd
import urllib.parse

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Gran Turin - Cardápio",
    page_icon="🍱",
    initial_sidebar_state="collapsed",
)

# Meta tags para o preview no WhatsApp
st.markdown(
    """
    <head>
        <meta charset="utf-8">
        <meta property="og:title" content="🍱 Gran Turin - Cardápio Digital" />
        <meta property="og:description" content="Monte seu pedido e envie pelo WhatsApp!" />
        <meta property="og:image" content="https://raw.githubusercontent.com/GranTurin/gran_turin_app/main/logo.png" />
    </head>
    """, unsafe_allow_html=True
)

# Estilização CSS
st.markdown("""
    <style>
    .main { overflow-y: auto; }
    .stButton button { 
        width: 100%; 
        border-radius: 12px; 
        height: 3.5em; 
        background-color: #25D366; 
        color: white; 
        font-weight: bold;
        border: none;
    }
    .stButton button:hover { border: 1px solid #128C7E; color: white; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    </style>
    """, unsafe_allow_html=True)

# 2. CARREGAMENTO DE DADOS
ID_PLANILHA = "1iXXBhK5lt0Eml_VE1BPXbxgSesjeVK9DJFCZAuklGd4"
URL_PLANILHA = f"https://docs.google.com/spreadsheets/d/{ID_PLANILHA}/export?format=csv"

@st.cache_data(ttl=30) # Reduzi para 30 segundos para atualizar mais rápido
def carregar_dados():
    try:
        # sep=None e engine='python' detectam automaticamente se o Google mudou de , para ;
        df = pd.read_csv(URL_PLANILHA, encoding='utf-8', sep=None, engine='python')
        # Limpeza de espaços e garantia de texto puro
        df.columns = df.columns.str.strip()
        for col in df.columns:
            df[col] = df[col].astype(str).str.strip()
        return df
    except Exception as e:
        st.error(f"Erro ao conectar com a planilha: {e}")
        return None

df = carregar_dados()

# 3. INTERFACE
st.image("https://raw.githubusercontent.com/GranTurin/gran_turin_app/main/logo.png", width=100)
st.title("🍱 Cardápio do Dia")
st.write("Selecione suas opções abaixo e envie seu pedido.")

if df is not None:
    try:
        # Extração das listas (removendo 'nan' que o pandas cria em células vazias)
        opcoes_carne = [x for x in df['Carnes'].tolist() if x != 'nan']
        opcoes_acomp = [x for x in df['Acompanhamentos'].tolist() if x != 'nan']
        opcoes_tamanho = [x for x in df['Tamanho'].tolist() if x != 'nan']

        # Formulário de Identificação
        with st.container(border=True):
            nome = st.text_input("👤 Seu Nome:", placeholder="Como quer ser chamado?")
            end = st.text_input("📍 Endereço/Loja:", placeholder="Ex: Rua Direita, 123 ou Loja B")

        # Seleção do Pedido
        st.subheader("📝 Monte seu prato")
        tamanho = st.selectbox("📏 Tamanho da Marmita:", ["Selecione..."] + opcoes_tamanho)
        carne = st.selectbox("🥩 Proteína Principal:", ["Selecione..."] + opcoes_carne)
        acomps = st.multiselect("🥗 Acompanhamentos:", opcoes_acomp)
        obs = st.text_area("🗒️ Observações (Opcional):", placeholder="Ex: Sem feijão, mandar talher, etc.")

        st.divider()

        # 4. LÓGICA DE ENVIO
        if st.button("🚀 ENVIAR PEDIDO"):
            if nome and end and carne != "Selecione..." and tamanho != "Selecione...":
                
                txt_acomps = ", ".join(acomps) if acomps else "Padrão da casa"
                
                # Formatação da mensagem
                texto_pedido = (
                    f"*🍱 NOVO PEDIDO - GRAN TURIN*\n"
                    f"━━━━━━━━━━━━━━━━━━━━━\n"
                    f"*👤 CLIENTE:* {nome}\n"
                    f"*📍 ENDEREÇO:* {end}\n"
                    f"━━━━━━━━━━━━━━━━━━━━━\n"
                    f"*📏 TAMANHO:* {tamanho}\n"
                    f"*🥩 PROTEÍNA:* {carne}\n"
                    f"*🥗 ACOMPS:* {txt_acomps}\n"
                    f"*🗒️ OBS:* {obs if obs else 'Nenhuma'}\n"
                    f"━━━━━━━━━━━━━━━━━━━━━\n"
                    f"✅ _Enviado via Cardápio Digital_"
                )
                
                # Link do WhatsApp com encoding UTF-8 garantido
                numero_whatsapp = "5521986577315"
                texto_url = urllib.parse.quote(texto_pedido.encode('utf-8'))
                link = f"https://wa.me/{numero_whatsapp}?text={texto_url}"
                
                st.success("Tudo certo! Clique no botão abaixo para finalizar no WhatsApp.")
                st.link_button("🟢 ABRIR WHATSAPP PARA CONCLUIR", link)
            else:
                st.error("⚠️ Por favor, preencha Nome, Endereço, Tamanho e Proteina!")

    except KeyError as e:
        st.error(f"Erro: A coluna {e} não foi encontrada na planilha. Verifique os títulos!")
else:
    st.info("Aguardando carregamento dos dados da planilha...")

st.markdown("---")
st.caption("Gran Turin - Sistema de Pedidos v2.5")
