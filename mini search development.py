"""A small in-memory search engine for local text documents."""

from __future__ import annotations

import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass


STOP_WORDS = {
	"a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
	"in", "is", "it", "of", "on", "or", "that", "the", "this", "to",
	"was", "with",
}


def tokenize(text: str) -> list[str]:
	"""Return normalized, searchable words from text."""
	return [
		word for word in re.findall(r"[a-zA-Z0-9]+", text.lower())
		if word not in STOP_WORDS
	]


@dataclass
class Document:
	title: str
	text: str


class MiniSearchEngine:
	def __init__(self) -> None:
		self.documents: dict[int, Document] = {}
		self.index: dict[str, set[int]] = defaultdict(set)
		self.term_counts: dict[int, Counter[str]] = {}

	def add_document(self, title: str, text: str) -> int:
		doc_id = len(self.documents)
		document = Document(title, text)
		self.documents[doc_id] = document
		counts = Counter(tokenize(f"{title} {text}"))
		self.term_counts[doc_id] = counts
		for term in counts:
			self.index[term].add(doc_id)
		return doc_id

	def search(self, query: str, limit: int = 10) -> list[tuple[float, Document]]:
		terms = tokenize(query)
		if not terms:
			return []

		scores: Counter[int] = Counter()
		total_docs = len(self.documents)
		for term in terms:
			matching_docs = self.index.get(term, set())
			if not matching_docs:
				continue
			# TF-IDF: frequent query terms in a document score higher,
			# while terms appearing in many documents matter less.
			idf = math.log((1 + total_docs) / (1 + len(matching_docs))) + 1
			for doc_id in matching_docs:
				counts = self.term_counts[doc_id]
				scores[doc_id] += (1 + math.log(counts[term])) * idf

		ranked = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
		return [(score, self.documents[doc_id]) for doc_id, score in ranked[:limit]]


def main() -> None:
	engine = MiniSearchEngine()
	print("Mini Search Engine (type 'quit' to exit)")
	print("Add documents with: add <title> | <text>")

	while True:
		try:
			command = input("> ").strip()
		except (EOFError, KeyboardInterrupt):
			print()
			break
		if command.lower() in {"quit", "exit"}:
			break
		if command.lower().startswith("add ") and "|" in command[4:]:
			title, text = command[4:].split("|", 1)
			engine.add_document(title.strip(), text.strip())
			print("Document added.")
		elif command.lower().startswith("search "):
			results = engine.search(command[7:])
			if not results:
				print("No results.")
			for score, document in results:
				print(f"{score:.2f}  {document.title}: {document.text}")
		else:
			print("Use 'add <title> | <text>', 'search <query>', or 'quit'.")


if __name__ == "__main__":
	main()
