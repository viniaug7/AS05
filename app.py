import streamlit as st
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS

from langchain.document_loaders import YoutubeLoader
from langchain.chains.question_answering import load_qa_chain

from langchain.prompts import PromptTemplate
import os

# --- Configuração da API Key ---
# Para rodar localmente, crie um arquivo .env na raiz do projeto com a linha:
# GOOGLE_API_KEY="SUA_API_KEY_AQUI"
# Para deploy no Streamlit Community Cloud, use o gerenciador de segredos (secrets).
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Configuração da chave de API através dos segredos do Streamlit (preferencial para deploy)
api_key = st.secrets["GOOGLE_API_KEY"]
os.environ['GOOGLE_API_KEY'] = api_key


# --- Funções Auxiliares ---

def get_pdf_text(pdf_docs):
    """Extrai o texto de uma lista de documentos PDF."""
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    """Divide o texto em chunks menores."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

@st.cache_resource
def get_vector_store(_chunks):
    """Cria e armazena os embeddings vetoriais."""
    if not _chunks:
        return None
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = FAISS.from_texts(_chunks, embedding=embeddings)
        return vector_store
    except Exception as e:
        st.error(f"Erro ao criar o vector store: {e}")
        return None

def get_conversational_chain():
    """Cria a cadeia de conversação com o LLM."""
    prompt_template = """
    Você é um assistente especialista em responder perguntas com base em um contexto fornecido.
    Analise o contexto abaixo e responda à pergunta do usuário de forma detalhada e completa.
    Se a resposta não estiver claramente presente no contexto, diga: "A resposta não está disponível no contexto fornecido".
    Não invente informações que não estão nos documentos.

    Contexto:
    {context}

    Pergunta:
    {question}

    Resposta:
    """
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

# --- Interface do Streamlit ---

st.set_page_config(page_title="Assistente de Documentos PDF", layout="wide")

st.title("Assistente Conversacional Baseado em LLM")
st.markdown("Faça upload dos seus documentos PDF e converse com eles!")

with st.sidebar:
    st.header("Seus Documentos")
    pdf_docs = st.file_uploader("Carregue seus arquivos PDF aqui", accept_multiple_files=True, type="pdf")

    if st.button("Processar Documentos"):
        if pdf_docs:
            with st.spinner("Processando... Por favor, aguarde."):
                # Extrai o texto dos PDFs
                raw_text = get_pdf_text(pdf_docs)
                if not raw_text.strip():
                    st.error("Não foi possível extrair texto dos PDFs. Verifique se os arquivos contêm texto selecionável.")
                else:
                    # Divide o texto em chunks
                    text_chunks = get_text_chunks(raw_text)
                    st.session_state.text_chunks = text_chunks
                    
                    # Cria e armazena o vector store
                    vector_store = get_vector_store(text_chunks)
                    st.session_state.vector_store = vector_store
                    
                    st.success("Documentos processados com sucesso! Pronto para responder.")
        else:
            st.warning("Por favor, carregue ao menos um arquivo PDF.")

st.header("Faça sua Pergunta")

# Inicializa o histórico do chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe as mensagens do histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Captura a pergunta do usuário
if prompt := st.chat_input("Qual a sua pergunta sobre os documentos?"):
    # Adiciona a pergunta do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Verifica se os documentos foram processados
    if "vector_store" not in st.session_state or st.session_state.vector_store is None:
        with st.chat_message("assistant"):
            st.warning("Por favor, processe os documentos na barra lateral primeiro.")
        st.session_state.messages.append({"role": "assistant", "content": "Por favor, processe os documentos na barra lateral primeiro."})
    else:
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                vector_store = st.session_state.vector_store
                
                # Realiza a busca por similaridade
                docs = vector_store.similarity_search(prompt)
                
                # Obtém a cadeia conversacional e a resposta
                chain = get_conversational_chain()
                response = chain({"input_documents": docs, "question": prompt}, return_only_outputs=True)
                
                response_text = response["output_text"]
                st.markdown(response_text)
        
        # Adiciona a resposta do assistente ao histórico
        st.session_state.messages.append({"role": "assistant", "content": response_text})