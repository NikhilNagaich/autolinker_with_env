-- Enable required extensions
create extension if not exists vector;
create extension if not exists pgcrypto; -- for gen_random_uuid()

-- Table: blogs
create table if not exists blogs (
  id uuid primary key default gen_random_uuid(),
  url text unique not null,
  title text,
  slug text,
  content text,
  content_html text,
  embedding vector(1536),
  sentences jsonb,
  seed_url text,
  created_at timestamp default now()
);

-- Table: link_suggestions
create table if not exists link_suggestions (
  id uuid primary key default gen_random_uuid(),
  source_blog_id uuid references blogs(id) on delete cascade,
  target_blog_id uuid references blogs(id) on delete cascade,
  suggestion_json jsonb,
  created_at timestamp default now()
);

-- ANN (Approximate Nearest Neighbor) index for embedding vector search
create index if not exists blogs_embedding_ann_idx
  on blogs using ivfflat (embedding vector_cosine_ops)
  with (lists = 100);

-- Example ANN similarity query
-- SELECT top 5 most similar blog posts to a given embedding
-- Replace [...] with the embedding vector as text (e.g., '[0.1, 0.2, ...]')
-- SELECT *, embedding <=> '[...]' as similarity
-- FROM blogs
-- WHERE url LIKE 'https://example.com/blog/%'
-- ORDER BY embedding <=> '[...]'
-- LIMIT 5;
