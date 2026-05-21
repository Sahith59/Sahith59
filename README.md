<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:8B0000,50:4A0000,100:FFD700&height=220&section=header&text=SAHITH%20REDDY%20THUMMALA&fontSize=45&fontColor=FFD700&animation=twinkling&fontAlignY=38&desc=AI%20%7C%20ML%20ENGINEER%20%7C%20GenAI%20ARCHITECT%20%7C%20FULL-STACK%20BUILDER&descAlignY=63&descSize=17&descColor=C0C0C0" width="100%"/>

<img src="https://readme-typing-svg.demolab.com?font=Orbitron&weight=900&size=18&pause=800&color=FFD700&background=00000000&center=true&vCenter=true&width=740&height=55&lines=J.A.R.V.I.S.+INITIALIZING+AGENT+PROFILE...;IDENTITY%3A+SAHITH+REDDY+THUMMALA+%5BCONFIRMED%5D;DESIGNATION%3A+AI%2FML+ENGINEER+%7C+GenAI+ARCHITECT;FULL-STACK+BUILDER+%7C+DATA+SCIENTIST+%5BONLINE%5D;FedEx+Innovation+Award+%5BCLASSIFIED%5D" alt="Typing Animation" />

<br/>

[![LinkedIn](https://img.shields.io/badge/LINKEDIN-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/sahith-reddy-thummala59)
[![Gmail](https://img.shields.io/badge/COMMS-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:tsahith59@gmail.com)
[![GitHub](https://img.shields.io/badge/GITHUB-181717?style=for-the-badge&logo=github&logoColor=FFD700)](https://github.com/Sahith59)
![Views](https://komarev.com/ghpvc/?username=Sahith59&style=for-the-badge&color=FF3333&label=PROFILE+VIEWS)

</div>

<br/>

---

<div align="center">
<img src="assets/header-tech.svg" width="100%"/>
</div>

<br/>

<div align="center">

**INTELLIGENCE SYSTEMS**

<img src="https://skillicons.dev/icons?i=py,pytorch,tensorflow,sklearn&theme=dark" />

<br/>

**LANGUAGES**

<img src="https://skillicons.dev/icons?i=java,ts,js,cpp,bash&theme=dark" />

<br/>

**AGENT & GenAI**

![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=FFD700)
![LangGraph](https://img.shields.io/badge/LangGraph-8B0000?style=for-the-badge&logoColor=FFD700)
![ChromaDB](https://img.shields.io/badge/ChromaDB-FFD700?style=for-the-badge&logoColor=0d0d0d)
![Ollama](https://img.shields.io/badge/Ollama-FF3333?style=for-the-badge&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD700?style=for-the-badge&logo=huggingface&logoColor=black)
![MLflow](https://img.shields.io/badge/MLflow-0194E2?style=for-the-badge&logo=mlflow&logoColor=white)
![RAG](https://img.shields.io/badge/RAG_Systems-4A0000?style=for-the-badge&logoColor=FFD700)

<br/>

**BACKEND & FULL-STACK**

<img src="https://skillicons.dev/icons?i=fastapi,spring,react,nextjs,nodejs,flask&theme=dark" />

<br/>

**INFRASTRUCTURE**

<img src="https://skillicons.dev/icons?i=docker,kubernetes,aws,redis,postgres,neo4j,git,linux&theme=dark" />

</div>

<br/>

---

<div align="center">
<img src="assets/header-projects.svg" width="100%"/>
</div>

<br/>

### [AgentMem-OS](https://github.com/Sahith59/AgentMem-OS)
`Python` `FastAPI` `Redis` `ChromaDB` `NetworkX` `DBSCAN` `LiteLLM` `SQLAlchemy`

Every LLM agent I worked with had the same flaw — context windows that either overflow or forget. AgentMem-OS is a four-tier memory architecture: Redis working cache, SQLite episodic store, ChromaDB vector index, and a NetworkX knowledge graph, with DBSCAN offline consolidation to clean noise between sessions. On a 49-turn stress test, the system recalled 6/6 facts versus 1/6 for a sliding-window baseline — at 66% lower token usage and 3x cheaper API cost. The knowledge graph scaled to 867 entities and 16,200 edges per session.

---

### [LogSage](https://github.com/Sahith59/LogSage)
`FastAPI` `LangGraph` `LangChain` `Next.js` `Neo4j` `Redis` `Ollama` `Docker`

A production SRE cockpit where AI agents investigate problems instead of just labeling them. A LangGraph cyclic state machine runs an Investigator that drafts root cause analyses and a Lead Critic that validates and rejects hallucinations in a self-reflective loop — every diagnosis is grounded in live system metrics queried through Python tool bindings. Real-time logs stream via WebSocket into a Next.js dashboard. The full stack runs as isolated Docker microservices deployed to AWS EC2, with all inference local via Ollama.

---

### [Nexus](https://github.com/Sahith59/IDE_Agent)
`LangGraph` `ChromaDB` `Ollama` `Qwen2.5` `nomic-embed-text` `llama3.2-vision`

Built for environments where internet access is restricted or unreliable. A fully offline IDE expert agent where LangGraph's semantic router classifies every query into one of five specialized retrieval tracks via MMR. Wired llama3.2-vision to extract and embed diagrams from `.docx`, `.pptx`, and `.pdf` files directly into ChromaDB, with nomic-embed-text for fully local embedding. Validated at 85% retrieval precision on a 20-query benchmark, end-to-end under 2 seconds on CPU with lazy-loading for fast startup.

---

### [QueryMesh](https://github.com/Sahith59/QueryMesh)
`Java 17` `Spring Boot` `PostgreSQL` `React 19` `TypeScript` `WebSockets` `Docker` `nginx`

Built to answer the question every engineer dreads before a migration: what breaks if I change this? Spring Boot runs BFS traversal to map FK dependency chains and LEFT JOIN scans to detect orphaned rows, with severity classification and auto-generated SQL remediation scripts. The React 19 + React Flow frontend renders the full schema dependency graph interactively. Validated core graph algorithms with JUnit 5 and deployed to AWS EC2 via Docker Compose with nginx as reverse proxy.

---

### [SecureChat](https://github.com/Sahith59/Encrypted_Chat_applicaition)
`Python` `Flask` `JavaScript` `WebSockets` `Noise Protocol XX` `ChaCha20-Poly1305`

An exercise in serious cryptography — no TLS wrappers, built from the protocol up. Implemented the Noise Protocol XX handshake pattern for mutual authentication, the same handshake used by WireGuard and Signal. All messages encrypted with ChaCha20-Poly1305 with per-message counters that block replay attacks. Delivered as both a Flask web app and a CLI client, supporting multi-room chat and encrypted file transfers up to 50MB. Benchmarked the full stack against TLS 1.3 and unencrypted on handshake time, throughput, and CPU overhead.

<br/>

---

<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Orbitron&weight=700&size=13&pause=2000&color=555555&background=00000000&center=true&vCenter=true&width=620&height=35&lines=%22Build+what+matters.+Ship+what+works.%22+%E2%80%94+Sahith+Reddy+Thummala" alt="Footer Quote"/>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:FFD700,50:4A0000,100:8B0000&height=120&section=footer" width="100%"/>

</div>
