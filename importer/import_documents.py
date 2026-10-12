
import hashlib
import os
import re
from datetime import date
from pathlib import Path

import psycopg

ROOT = Path("/documents")
WORD = ROOT / "word"
EXTRACTED = ROOT / "extracted"

PATTERN = re.compile(
    r"Protokoll Styrelsemöte Nr (\d+) (\d{4}-\d{2}-\d{2})\.docx$",
    re.IGNORECASE,
)


def make_chunks(text, max_chars=1500):
    """Dela text vid styckegränser."""
    paragraphs = [
        p.strip()
        for p in text.split("\n\n")
        if p.strip()
    ]

    chunks = []
    current = ""

    for paragraph in paragraphs:
        if current and len(current) + len(paragraph) + 2 > max_chars:
            chunks.append(current)
            current = ""

        # Hantera även ovanligt långa stycken
        while len(paragraph) > max_chars:
            if current:
                chunks.append(current)
                current = ""
            chunks.append(paragraph[:max_chars])
            paragraph = paragraph[max_chars:]

        if paragraph:
            current = (
                current + "\n\n" + paragraph
                if current else paragraph
            )

    if current:
        chunks.append(current)

    return chunks


def import_document(conn, file):
    match = PATTERN.fullmatch(file.name)

    if not match:
        print(f"HOPPAR ÖVER: {file.name}")
        return

    number = int(match.group(1))
    meeting_date = date.fromisoformat(match.group(2))

    text_file = EXTRACTED / (file.stem + ".txt")

    if not text_file.exists():
        raise FileNotFoundError(text_file)

    text = text_file.read_text(encoding="utf-8")
    if not text.strip():
        raise ValueError(f"Tom textfil: {text_file}")

    checksum = hashlib.sha256(file.read_bytes()).hexdigest()
    chunks = make_chunks(text)

    if not chunks:
        raise ValueError(f"Inga textavsnitt: {file.name}")

    source_id = f"styrelsemote-{number}"
    relative_path = f"documents/word/{file.name}"

    with conn.transaction():
        document = conn.execute(
            """
            SELECT id FROM documents
            WHERE source_system = %s AND source_id = %s
            ORDER BY created_at LIMIT 1
            """,
            ("word_archive", source_id),
        ).fetchone()

        if document:
            doc_id = document[0]
        else:
            doc_id = conn.execute(
                """
                INSERT INTO documents
                    (title, document_type, document_date,
                     source_system, source_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    f"Styrelsemöte nr {number}",
                    "styrelseprotokoll",
                    meeting_date,
                    "word_archive",
                    source_id,
                ),
            ).fetchone()[0]

        existing = conn.execute(
            """
            SELECT id FROM document_versions
            WHERE document_id = %s AND sha256 = %s
            """,
            (doc_id, checksum),
        ).fetchone()

        if existing:
            print(f"OFÖRÄNDRAD: Möte {number}")
            return

        version_number = conn.execute(
            """
            SELECT COALESCE(MAX(version_number), 0) + 1
            FROM document_versions
            WHERE document_id = %s
            """,
            (doc_id,),
        ).fetchone()[0]

        version_id = conn.execute(
            """
            INSERT INTO document_versions
                (document_id, version_number, file_path,
                 sha256, mime_type, indexed_at)
            VALUES (%s, %s, %s, %s, %s, now())
            RETURNING id
            """,
            (
                doc_id,
                version_number,
                relative_path,
                checksum,
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ),
        ).fetchone()[0]

        for i, chunk in enumerate(chunks):
            conn.execute(
                """
                INSERT INTO document_chunks
                    (version_id, chunk_number, content)
                VALUES (%s, %s, %s)
                """,
                (version_id, i, chunk),
            )

    print(
        f"IMPORTERAD: Möte {number}, "
        f"version {version_number}, {len(chunks)} textavsnitt"
    )


def main():
    files = sorted(WORD.glob("*.docx"))
    print(f"Hittade {len(files)} Word-filer")

    with psycopg.connect(
        host="db",
        dbname="brf_knowledge",
        user="brf_importer",
        password=os.environ["IMPORTER_PASSWORD"],
    ) as conn:
        for file in files:
            import_document(conn, file)


if __name__ == "__main__":
    main()
