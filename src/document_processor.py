from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class Document(BaseModel):
    id: int
    title: str
    authors: List[str]
    is_published: bool
    metadata: Optional[Dict[str, Any]] = None


import json
from typing import List

from pydantic import ValidationError


def load_and_validate_documents(file_path: str) -> List[Document]:
    validated_documents: List[Document] = []
    try:
        with open(file_path, "r") as f:
            data = json.load(f)

        for doc_data in data:
            try:
                document = Document(**doc_data)
                validated_documents.append(document)
            except ValidationError as e:
                print(f"Validation error for document: {doc_data}. Error: {e}")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{file_path}'.")
    return validated_documents


def display_document_info(document: Document) -> None:
    print(f"--- Document ID: {document.id} ---")
    print(f"Title: {document.title}")
    print(f"Authors: {', '.join(document.authors)}")
    print(f"Published: {'Yes' if document.is_published else 'No'}")
    if document.metadata:
        print(f"Metadata: {document.metadata}")
    print("-" * 20)


if __name__ == "__main__":
    documents = load_and_validate_documents("../data/documents.json")
    for doc in documents:
        display_document_info(doc)
