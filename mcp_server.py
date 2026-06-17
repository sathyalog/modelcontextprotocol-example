from pydantic import Field
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

# TODO: Write a tool to read a doc
@mcp.tool(name="read_doc", description="Read a document")
def read_doc(doc_id: str = Field(description="The ID of the document to read")) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document {doc_id} not found")
    return docs[doc_id]

# TODO: Write a tool to edit a doc
@mcp.tool(name="edit_doc", description="Edit a document")
def edit_doc(
    doc_id: str = Field(description="The ID of the document to edit"),
    old_content: str = Field(description="The old content of the document"),
    new_content: str = Field(description="The new content of the document"),
) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document {doc_id} not found")
    new_content = docs[doc_id].replace(old_content, new_content)
    docs[doc_id] = new_content
    return f"Document {doc_id} has been edited"

# TODO: Write a resource to return all doc id's
@mcp.resource("docs://documents", description="A list of all document IDs", mime_type="application/json")
def list_docs() -> list[str]:
    return list(docs.keys())

# TODO: Write a resource to return the contents of a particular doc
@mcp.resource("docs://documents/{doc_id}", description="The contents of a particular document", mime_type="text/plain")
def get_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document {doc_id} not found")
    return docs[doc_id]

# TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
