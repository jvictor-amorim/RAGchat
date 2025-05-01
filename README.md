
# 🧠 RAG Chat Application

Este projeto é uma aplicação de chat que utiliza **RAG (Retrieval-Augmented Generation)** com **LangChain**, **Qdrant**, **LLMs da Groq (LLaMA 3)**, e **transformers da Hugging Face** para fornecer respostas contextualizadas com base em um conjunto de dados.

A aplicação possui:

- Backend com **FastAPI** e integração com LangChain + LLM
- Frontend com **Next.js** (React)
- Comunicação entre serviços via **Docker Compose**
- Suporte ao modo **RAG** e **Padrão**

---

## 📂 Estrutura do Projeto

```
.
├── backend
│   ├── app
│   │   └── main.py              # Código principal da API FastAPI
│   ├── data
│   │   └── casos.csv            # Arquivo de dados utilizado no RAG
│   └── Dockerfile               # Dockerfile da API
├── frontend
│   ├── components               # Componentes reutilizáveis de UI
│   ├── app                      # Página principal com chat
│   └── Dockerfile               # Dockerfile do Frontend
├── docker-compose.yml
└── README.md
```

---

## 🚀 Como Executar

### Pré-requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Configuração

1. **Crie um arquivo `.env` dentro da pasta `backend` com sua chave da Groq API:**

```env
API_KEY_LLM=sua_chave_da_groq_aqui
```

2. **Garanta que o arquivo `casos.csv` esteja em `backend/data/`.**

3. **Execute a aplicação com:**

```bash
docker-compose up --build
```

4. Acesse:

- Frontend: [http://localhost:3000](http://localhost:3000)
- API: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 💬 Funcionalidades

- **Modo Padrão:** O LLM responde com base apenas na mensagem do usuário.
- **Modo RAG:** A pergunta é enriquecida com contexto extraído do `casos.csv` usando busca semântica com Qdrant + embeddings.
- Alternância entre modos no frontend com botão.

---

## 🛠️ Tecnologias Utilizadas

### Backend

- [FastAPI](https://fastapi.tiangolo.com/)
- [LangChain](https://www.langchain.com/)
- [Qdrant (in-memory)](https://qdrant.tech/)
- [Transformers - HuggingFace](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [OpenAI Compatibility via Groq API (LLaMA3)](https://console.groq.com/)

### Frontend

- [Next.js (React)](https://nextjs.org/)
- [TailwindCSS](https://tailwindcss.com/)
- [Lucide Icons](https://lucide.dev/)

---

## 📦 Exemplos de Uso

1. Abra o frontend.
2. Digite uma pergunta como:
   - "Qual é a história do caso 1?"
   - "Quem está envolvido no caso que fala sobre fraude?"
3. Ative o modo "Usando RAG" para respostas baseadas nos dados do `casos.csv`.

---

## 📌 Observações

- O Qdrant está em modo **in-memory**, ou seja, os dados são perdidos a cada reinício da API.
- Para produção, recomenda-se usar Qdrant em container ou serviço persistente.
- Apenas as **3 primeiras linhas** do CSV são carregadas neste exemplo. Você pode expandir para o dataset completo conforme necessidade.

---

## ✅ Futuras Melhorias

- Adicionar autenticação de usuários.
- Persistência de conversas.
- Interface para upload de novos dados.
- Uso de banco de dados real para histórico e contexto.
