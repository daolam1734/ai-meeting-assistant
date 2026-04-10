import os
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from typing import List

class VectorStoreService:
    def __init__(self, api_key: str):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=api_key
        )
        self.index_path = "faiss_index"

    def add_meeting_transcript(self, meeting_id: int, transcript: str):
        """
        Chunks the transcript and adds it to the FAISS index.
        """
        # Simple chunking logic (could be improved with RecursiveCharacterTextSplitter)
        chunks = [transcript[i:i+1000] for i in range(0, len(transcript), 800)]
        docs = [
            Document(page_content=chunk, metadata={"meeting_id": meeting_id})
            for chunk in chunks
        ]
        
        if os.path.exists(self.index_path):
            vector_store = FAISS.load_local(self.index_path, self.embeddings, allow_dangerous_deserialization=True)
            vector_store.add_documents(docs)
        else:
            vector_store = FAISS.from_documents(docs, self.embeddings)
            
        vector_store.save_local(self.index_path)

    def search_knowledge(self, query: str, k: int = 4) -> List[Document]:
        """
        Searches the FAISS index for relevant meeting chunks.
        """
        if not os.path.exists(self.index_path):
            return []
            
        vector_store = FAISS.load_local(self.index_path, self.embeddings, allow_dangerous_deserialization=True)
        return vector_store.similarity_search(query, k=k)

vector_service = VectorStoreService(api_key=os.getenv("GOOGLE_API_KEY", ""))
