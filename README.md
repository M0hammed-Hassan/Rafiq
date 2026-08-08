<div align="center">

# Rafiq

Building a real AI assistant, one episode at a time, from a simple chatbot to a full RAG + multi-agent system.

[![YouTube](https://img.shields.io/badge/YouTube-Watch_the_series-red?logo=youtube&logoColor=white)](https://youtube.com/playlist?list=PLcIPbLAATTWg&si=iqf87k4DNqPLd9xq)
[![Subscribe](https://img.shields.io/badge/Subscribe-AI_with_M._Hassan-3EDBEE?logo=youtube&logoColor=white)](https://youtube.com/@aiwithmhassan?sub_confirmation=1)

</div>

---

## About this project

This repo holds the code for **Rafiq**, an AI assistant built in public across the *RAG From Scratch* series on the **Muhammad Hassan** YouTube channel.

Every episode ships real working code.

> We don't just learn AI. We build it together.

---

## Repository Structre
```
app/
|  ├── main.py              
|  ├── config/
|  │   └── settings.py       
|  ├── prompts/
|  │   └── system_prompts.py  
|  ├── dto/
|  │   └── ask.py              
|  ├── core/                    
|  │   ├── llm_client.py           
|  │   ├── vector_store.py         
|  │   ├── document_loader.py      
|  │   ├── chunking.py              
|  │   ├── retrieval.py             
|  │   └── synthesis.py              
|  ├── routes/
|  │   └── ask_routes.py           
|  ├── ingestion/
|  ├── └── ingest.py    
|  ├── frontend/
|  │   └── rafiq.html             
data/
|  ├── docs/                
|  └── chroma_db/  
|  episodes/
|  ├── ep01/                 
|  └── ep02/  
└── requirements.txt
```

## Series roadmap

| Ep | Title | Status | Watch |
|----|-------|------|-------|
| 01 | Baseline Chatbot | ✅ Live | [▶ Watch](https://www.youtube.com/watch?v=5wWKk_nD6dg&t=2537s) |
| 02 | RAG With ChromaDB | ✅ Live | [▶ Watch]() |

## Tech stack

`Python` · `FastAPI` · `OpenAI API`  . `ChromaDB`

## Getting started
```bash
git clone git@github.com:M0hammed-Hassan/Rafiq.git
cd Rafiq
```

## Installation
  
```bash
conda create -n rafiq python=3.10
conda activate rafiq
 
pip install -r requirements.txt
```

## Run it
 
**1. Ingest the documents (do this first, and any time `data/docs/` changes)**
 
```bash
python -m app.ingestion.ingest
```
 
You should see each file's chunk count printed.
 
**2. Start the server**
 
```bash
uvicorn app.main:app --reload --port 8000
```
 
Check `http://localhost:8000/health` — `indexed_chunks` should be greater than 0.

**3. Run frontend**
```bash
cd app/frontend
python -m http.server 5500 
```
 
 
## Follow Me
 
- 💼 LinkedIn: [Muhammad Hassan](https://www.linkedin.com/in/muhammad-hassan-a152b9229/)
- 📘 Facebook: [Muhamamd Hassan](https://www.facebook.com/aiwithmhassan)

---

<div align="center">
<sub>Learn AI. Build AI. Ship AI.</sub>
</div>