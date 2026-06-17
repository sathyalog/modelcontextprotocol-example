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
@mcp.prompt(
    name="format",
    description="Rewrites the contents of the document in Markdown format.",
)

def format_document(
    doc_id: str = Field(description="Id of the document to format"),
) -> list[base.Message]:
    prompt = f"""
    Your goal is to reformat a document to be written with markdown syntax.

    The id of the document you need to reformat is:
    <document_id>
    {doc_id}
    </document_id>

    Add in headers, bullet points, tables, etc as necessary. Feel free to add in extra text, but don't change the meaning of the report.
    Use the 'edit_document' tool to edit the document. After the document has been edited, respond with the final version of the doc. Don't explain your changes.
    """

    return [base.UserMessage(prompt)]



if __name__ == "__main__":
    mcp.run(transport="stdio")
