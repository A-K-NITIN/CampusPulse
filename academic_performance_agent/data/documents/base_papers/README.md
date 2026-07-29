# Base papers folder

Drop the actual PDF files here, named to match `file_path` in `metadata.csv`
(e.g. `BP001.pdf`). Every time you add/remove a paper here, update
`metadata.csv` with its `paper_id`, `title`, `keywords`, and `file_path`,
then re-run:

    python -m rag.ingest

to rebuild the vector index. Only the metadata (title + keywords) is
embedded for retrieval — the PDF itself is just linked by file path and
sent/attached when the agent matches it to a request.
