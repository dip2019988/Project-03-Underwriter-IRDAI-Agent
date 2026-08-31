import json

from pathlib import Path

from langchain_core.documents import Document

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_openai import OpenAIEmbeddings

from langchain_community.vectorstores import FAISS

from config.settings import settings

from services.document_ingestion_service import document_ingestion_service


class InsuranceVectorStore:

    def __init__(self):

        self.embeddings = OpenAIEmbeddings(
            api_key=settings.OPENAI_API_KEY
        )

        self.vector_store = None

        self.index_path = Path(
            "faiss_index"
        )

    def build_index(self):

        documents = (
            document_ingestion_service
            .load_json_documents(
                str(settings.KB_FILE_PATH)
            )
        )

        chunks = (
            document_ingestion_service
            .chunk_documents(
                documents
            )
        )

        self.vector_store = (
            FAISS.from_documents(
                chunks,
                self.embeddings
            )
        )

        self.vector_store.save_local(
            str(self.index_path)
        )

    def load_index(self):

        if self.index_path.exists():

            self.vector_store = (
                FAISS.load_local(
                    str(self.index_path),
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
            )

            return True

        return False


    def similarity_search(
            self,
            query: str,
            k: int = 5
        ):
            """
            Hybrid Retrieval

            Step 1:
            Semantic retrieval via FAISS.

            Step 2:
            Apply lightweight business-domain boosting
            to improve insurance relevance.
            """

            if self.vector_store is None:

                loaded = self.load_index()

                if not loaded:

                    self.build_index()

            # ----------------------------------
            # Semantic Search
            # ----------------------------------

            results = (
                self.vector_store.similarity_search(
                    query,
                    k=10
                )
            )

            query_lower = query.lower()

            boosted_results = []

            for doc in results:

                score = 0

                category = (
                    doc.metadata.get(
                        "category",
                        ""
                    )
                    .upper()
                )

                # ----------------------------------
                # IRDAI Compliance Queries
                # ----------------------------------

                if (
                    "section 45" in query_lower
                    or "free look" in query_lower
                    or "irdai" in query_lower
                ):

                    if category == "IRDAI_COMPLIANCE":

                        score += 10

                # ----------------------------------
                # ULIP Queries
                # ----------------------------------

                if "ulip" in query_lower:

                    if category == "ULIP":

                        score += 10

                # ----------------------------------
                # HLV Queries
                # ----------------------------------

                if (
                    "hlv" in query_lower
                    or "income" in query_lower
                    or "cover" in query_lower
                ):

                    if category == "HLV":

                        score += 10

                # ----------------------------------
                # Medical Queries
                # ----------------------------------

                if (
                    "diabetes" in query_lower
                    or "asthma" in query_lower
                    or "medical" in query_lower
                ):

                    if category in (
                        "MEDICAL_RULES",
                        "UNDERWRITING_RULES"
                    ):

                        score += 10

                # ----------------------------------
                # Family History
                # ----------------------------------

                if (
                    "father" in query_lower
                    or "mother" in query_lower
                    or "bypass" in query_lower
                ):

                    if category == "FAMILY_HISTORY":

                        score += 10

                boosted_results.append(
                    (
                        score,
                        doc
                    )
                )

            boosted_results.sort(
                key=lambda x: x[0],
                reverse=True
            )

            return [
                doc
                for _, doc
                in boosted_results[:k]
            ]


insurance_vector_store = (
    InsuranceVectorStore()
)