🧠 **Resume Matcher API**

An intelligent Resume–Job Description Matching System built with FastAPI, Sentence Transformers, ChromaDB, and LLaMA for smart scoring and explanations.
It automatically parses resumes and job descriptions, generates semantic embeddings, and uses a large language model to evaluate skill match, missing skills, and explanation — creating a human-like review of candidate fit.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

🚀 **Features**

🧾 Upload resumes (PDF/DOCX) and extract text automatically

🧠 Generate vector embeddings using **all-mpnet-base-v2**

💾 Store vectors locally with **ChromaDB** (no server setup needed)

🔍 Search for semantically similar resumes or jobs

🤖 Use LLM scoring (LLaMA) for:

- Match percentage
- Missing skills
- Explanation of candidate fit

⚙️ Clean modular FastAPI architecture (Routers + CRUD + Models)

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

🏗️ **Tech Stack**

| Layer                  | Technology                                |
| ---------------------- | ----------------------------------------- |
| Backend API            | FastAPI                                   |
| Database ORM           | SQLAlchemy                                |
| Vector Database        | ChromaDB                                  |
| Embedding Model        | SentenceTransformer (`all-mpnet-base-v2`) |
| Resume Parsing         | pdfminer.six, python-docx                 |
| Config Management      | Pydantic Settings                         |
| LLM Model              | meta-llama/llama-4-scout-17b-16e-instruct |

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
📦 **API Flow**

 **Upload Resume**

POST /resume/upload-resume/
Uploads a PDF/DOCX file and stores its embedding in ChromaDB.

 **Upload Job Description**

POST /jd/upload/
Stores JD text and embedding.

 **Match Job ↔ Resume**

POST /match/run/
Returns similarity score, match percentage, and missing skills.
