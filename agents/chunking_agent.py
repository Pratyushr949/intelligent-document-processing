import logging
import re
from typing import Any, Dict, List
from agents.base import BaseDocumentAgent

logger = logging.getLogger("agents.chunking_agent")


class DocumentChunkingAgent(BaseDocumentAgent):
    """
    Agent responsible for splitting raw page text into configurable chunks
    while preserving page boundaries, semantic context, and handling large inputs.
    """

    def __init__(self, **kwargs):
        instruction = (
            "You are a text chunking agent. Your goal is to split raw text inputs "
            "into clean, readable chunks that fit within size specifications "
            "while maintaining page boundaries and semantic continuity."
        )
        super().__init__(
            name="chunking_agent",
            instruction=instruction,
            **kwargs
        )

    def process_document(self, file_path: str, **kwargs) -> Dict[str, Any]:
        """
        Base override required by BaseDocumentAgent. Not used directly.
        """
        return {"agent": self.name, "status": "active"}

    def chunk_page(
        self,
        page_input: Dict[str, Any],
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        chunk_id_prefix: str = ""
    ) -> List[Dict[str, Any]]:
        """
        Splits a single page input into a list of chunks.

        Input schema:
            {
                "raw_text": "...",
                "page_number": int
            }

        Output schema:
            [
                {
                    "chunk_id": "...",
                    "page_start": int,
                    "page_end": int,
                    "content": "..."
                }
            ]

        Args:
            page_input (Dict[str, Any]): Dictionary with keys "raw_text" and "page_number".
            chunk_size (int): Max character count of each chunk.
            chunk_overlap (int): Max character overlap between chunks.
            chunk_id_prefix (str): Prefix to unique-ify chunk IDs.

        Returns:
            List[Dict[str, Any]]: List of generated chunks with page numbers.
        """
        raw_text = page_input.get("raw_text", "") or ""
        page_num = page_input.get("page_number", 1)

        if not raw_text.strip():
            return []

        # Split text into sentences using simple regex to preserve punctuation contexts
        sentence_endings = re.compile(r'(?<=[.!?])\s+')
        sentences = [s.strip() for s in sentence_endings.split(raw_text) if s.strip()]

        if not sentences:
            # Fallback to single string block if no endings found
            sentences = [raw_text.strip()]

        chunks = []
        current_chunk_sentences = []
        current_chunk_len = 0
        chunk_idx = 1

        sentence_idx = 0
        while sentence_idx < len(sentences):
            sentence = sentences[sentence_idx]

            # If a single sentence exceeds the chunk size, we force-split it by words
            if len(sentence) > chunk_size:
                # Flush the current chunk before handling the large sentence
                if current_chunk_sentences:
                    chunk_text = " ".join(current_chunk_sentences)
                    prefix = f"{chunk_id_prefix}_" if chunk_id_prefix else ""
                    chunks.append({
                        "chunk_id": f"{prefix}{chunk_idx}",
                        "page_start": page_num,
                        "page_end": page_num,
                        "content": chunk_text
                    })
                    chunk_idx += 1
                    current_chunk_sentences = []
                    current_chunk_len = 0

                # Force word-level split of the large sentence
                words = sentence.split()
                word_idx = 0
                while word_idx < len(words):
                    chunk_words = []
                    chunk_word_len = 0
                    while word_idx < len(words) and chunk_word_len + len(words[word_idx]) + 1 <= chunk_size:
                        chunk_words.append(words[word_idx])
                        chunk_word_len += len(words[word_idx]) + 1
                        word_idx += 1

                    if chunk_words:
                        chunk_text = " ".join(chunk_words)
                        prefix = f"{chunk_id_prefix}_" if chunk_id_prefix else ""
                        chunks.append({
                            "chunk_id": f"{prefix}{chunk_idx}",
                            "page_start": page_num,
                            "page_end": page_num,
                            "content": chunk_text
                        })
                        chunk_idx += 1

                sentence_idx += 1
                continue

            # Check if this sentence fits in the current chunk
            added_len = len(sentence) + (1 if current_chunk_sentences else 0)
            if current_chunk_len + added_len <= chunk_size:
                current_chunk_sentences.append(sentence)
                current_chunk_len += added_len
                sentence_idx += 1
            else:
                # Save chunk
                chunk_text = " ".join(current_chunk_sentences)
                prefix = f"{chunk_id_prefix}_" if chunk_id_prefix else ""
                chunks.append({
                    "chunk_id": f"{prefix}{chunk_idx}",
                    "page_start": page_num,
                    "page_end": page_num,
                    "content": chunk_text
                })
                chunk_idx += 1

                # Calculate sliding window sentence overlap
                overlap_sentences = []
                overlap_len = 0
                for rollback_s in reversed(current_chunk_sentences):
                    added_overlap = len(rollback_s) + (1 if overlap_sentences else 0)
                    if overlap_len + added_overlap <= chunk_overlap:
                        overlap_sentences.insert(0, rollback_s)
                        overlap_len += added_overlap
                    else:
                        break

                current_chunk_sentences = overlap_sentences
                current_chunk_len = overlap_len
                # Loop back without incrementing sentence_idx to re-evaluate the current sentence

        # Flush final chunk
        if current_chunk_sentences:
            chunk_text = " ".join(current_chunk_sentences)
            prefix = f"{chunk_id_prefix}_" if chunk_id_prefix else ""
            chunks.append({
                "chunk_id": f"{prefix}{chunk_idx}",
                "page_start": page_num,
                "page_end": page_num,
                "content": chunk_text
            })

        return chunks
