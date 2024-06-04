from langchain.text_splitter import TokenTextSplitter

def split_text(chunk_size: int, overlap: int, text: str) -> list:
    """
    Split the input text into chunks using a specified chunk size and overlap.

    Parameters:
    - chunk_size: The size of each text chunk.
    - overlap: The overlap between consecutive chunks.
    - text: The input text to be split.

    Returns:
    - split: A list of text chunks.
    """
    # Use TokenTextSplitter to split the text
    text_splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    split = text_splitter.split_text(text)
    return split