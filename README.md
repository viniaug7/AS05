# Assistente Conversacional de Documentos PDF com Gemini

## Autor

**Vinicius Augusto Alves Santos Mello**

## Descrição do Projeto

Este projeto implementa um assistente conversacional inteligente. A aplicação permite que o usuário faça o upload de um ou mais documentos em formato PDF e, em seguida, realize perguntas sobre o conteúdo desses documentos através de uma interface de chat interativa.

O sistema utiliza um Modelo de Linguagem Grande (LLM) da família Gemini, do Google, para compreender o contexto dos documentos e formular respostas precisas, baseando-se exclusivamente nas informações fornecidas. Esta abordagem é conhecida como **RAG (Retrieval-Augmented Generation)**.

## Link para a Aplicação em Funcionamento

A versão funcional e online desta aplicação está disponível no Streamlit Community Cloud através do seguinte link:

**https://vinicius-augusto-as05.streamlit.app/**

## Funcionalidades

* **Upload de Múltiplos Arquivos:** Permite o upload simultâneo de vários documentos PDF.
* **Processamento de Texto:** Extrai e divide o texto dos documentos em fragmentos (chunks) para otimizar a busca.
* **Indexação Vetorial:** Cria embeddings para cada fragmento de texto e os armazena em um banco de dados vetorial FAISS em memória.
* **Chat Interativo:** Oferece uma interface de chat para que o usuário possa fazer perguntas de forma natural.
* **Respostas Contextualizadas:** Gera respostas baseadas estritamente no conteúdo dos documentos carregados, evitando alucinações do modelo.
* **Manutenção de Histórico:** Mantém o histórico da conversa durante a sessão ativa do usuário.

---

## Instruções de Instalação e Execução

Siga os passos abaixo para configurar e rodar o projeto em um ambiente local.

### Passo a Passo

1.  **Clone o Repositório:**
    Abra seu terminal e clone este repositório do GitHub.
    ```bash
    git clone <https://github.com/viniaug7/AS05.git>
    cd <NOME_DA_PASTA_DO_PROJETO>
    ```

2.  **Crie e Ative um Ambiente Virtual:**
    É uma forte recomendação usar um ambiente virtual para isolar as dependências do projeto e evitar conflitos com pacotes do sistema (especialmente em Linux).

    * **No Linux ou macOS:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    * **No Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    Após a ativação, você verá `(venv)` no início do seu prompt de comando.

3.  **Instale as Dependências:**
    Com o ambiente virtual ativo, instale todas as bibliotecas necessárias a partir do arquivo `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure sua API Key do Google Gemini:**

    Para rodar localmente, crie um arquivo .env na raiz do projeto com a linha: GOOGLE_API_KEY="SUA_API_KEY_AQUI"

    O Streamlit possui um sistema de gerenciamento de segredos que funciona tanto localmente quanto na nuvem.

    * Crie uma pasta chamada `.streamlit` na raiz do seu projeto.
    * Dentro da pasta `.streamlit`, crie um arquivo chamado `secrets.toml`.
    * Abra o arquivo `secrets.toml` e adicione sua chave de API do Google Gemini.

    O conteúdo do arquivo `secrets.toml` deve ser:
    ```toml
    # .streamlit/secrets.toml

    GOOGLE_API_KEY = "SUA_API_KEY_AQUI"
    ```

6.  **Execute a Aplicação:**
    Finalmente, execute o seguinte comando no seu terminal:
    ```bash
    streamlit run app.py
    ```
    A aplicação será iniciada e um link será aberto automaticamente no seu navegador.

---
