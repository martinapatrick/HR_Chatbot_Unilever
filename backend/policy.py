import re

from pypdf import PdfReader
from rank_bm25 import BM25Okapi

from config import POLICY_PDF

CHUNK_SIZE = 800
OVERLAP = 150

_chunks: list[str] = []
_bm25: BM25Okapi | None = None


def _tokenize(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


def load_policy() -> int:
    """Read the PDF, split into chunks, build the search index. Returns chunk count."""
    global _chunks, _bm25
    if not POLICY_PDF.exists():
        return 0
    text = "\n".join(page.extract_text() or "" for page in PdfReader(POLICY_PDF).pages)
    text = re.sub(r"\s+", " ", text).strip()
    step = CHUNK_SIZE - OVERLAP
    _chunks = [text[i:i + CHUNK_SIZE] for i in range(0, len(text), step)]
    _bm25 = BM25Okapi([_tokenize(c) for c in _chunks]) if _chunks else None
    return len(_chunks)


def search(question: str, k: int = 4) -> list[str]:
    if not _bm25:
        return []
    scores = _bm25.get_scores(_tokenize(question))
    top = sorted(range(len(_chunks)), key=lambda i: scores[i], reverse=True)[:k]
    return [_chunks[i] for i in top if scores[i] > 0]
