# Software-Patterns-for-LLMs

This project implements a modular **state machine** using **LangGraph** and **FastAPI**, designed to handle workflows through independent nodes. The nodes interact via a shared state, ensuring flexibility and scalability.

---

## Installation

1. **Set OpenAI API Key**:

   - Rename `.env.example` to `.env` and add your `OPENAI_API_KEY` to the `.env` file:
     ```plaintext
     OPENAI_API_KEY=your_openai_api_key
     ```

2. **Install Dependencies**:

   - Use Poetry as the dependency manager to install the required packages:
     ```bash
     poetry install
     ```

3. **Run the FastAPI Server**:
   - Start the server:
     ```bash
     poetry run uvicorn main:app --reload
     ```

---
