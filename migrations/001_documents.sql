
BEGIN;

CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    document_type TEXT NOT NULL,
    document_date DATE,
    source_system TEXT,
    source_id TEXT,
    source_uri TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE document_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL
        REFERENCES documents(id),
    version_number INTEGER NOT NULL
        CHECK (version_number > 0),
    file_path TEXT NOT NULL,
    sha256 CHAR(64) NOT NULL,
    mime_type TEXT,
    indexed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (document_id, version_number)
);

CREATE TABLE document_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    version_id UUID NOT NULL
        REFERENCES document_versions(id) ON DELETE CASCADE,
    chunk_number INTEGER NOT NULL
        CHECK (chunk_number >= 0),
    content TEXT NOT NULL,
    page_number INTEGER CHECK (page_number > 0),
    section_reference TEXT,
    UNIQUE (version_id, chunk_number)
);

CREATE INDEX idx_chunks_fulltext
ON document_chunks
USING GIN (to_tsvector('swedish', content));

COMMIT;
