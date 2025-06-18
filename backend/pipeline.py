def run_autolinker_pipeline(input_url):
    from dotenv import load_dotenv; 
    load_dotenv()
    from input.crawl_urls import crawl_blog_urls
    from input.extract_content import extract_blog_data
    from input.preprocess import clean_text
    from embeddings.generate_embeddings import embed_blog, get_embedding
    from matching.gpt_anchor_suggester import suggest_anchor
    import random
    import os
    from tqdm import tqdm
    from urllib.parse import urlparse, urldefrag
    from db.supabase_client import get_supabase
    import ast
    import logging
    from bs4 import BeautifulSoup

    logging.basicConfig(level=logging.INFO)

    def remove_hyperlinked_text(html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        for a in soup.find_all("a"):
            a.decompose()  # Removes the <a> tag and its contents
        return soup.get_text()

    def get_blogs_for_seed(seed_url):
        supabase = get_supabase()
        return supabase.table("blogs").select("*").eq("url", seed_url).execute().data

    def get_blog_by_url(url):
        supabase = get_supabase()
        data = supabase.table("blogs").select("*").eq("url", url).execute().data
        return data[0] if data else None

    def insert_blog(blog):
        supabase = get_supabase()
        existing = get_blog_by_url(blog["url"])
        if not existing:
            supabase.table("blogs").insert(blog).execute()

    def get_blog_pattern(input_url):
        parsed = urlparse(input_url)
        path_parts = parsed.path.strip("/").split("/")
        if len(path_parts) > 1:
            pattern = "/" + "/".join(path_parts[:-1]) + "/"
        else:
            pattern = parsed.path
        return pattern

    def is_valid_blog_url(url, pattern):
        url, _ = urldefrag(url)
        parsed = urlparse(url)
        path = parsed.path

        if not path.startswith(pattern):
            return False

        if path.rstrip("/") == pattern.rstrip("/"):
            return False

        if "/page/" in path or "-page-" in path or "?page=" in url or parsed.query:
            return False

        if path.rstrip("/").endswith("/blogs"):
            return False

        if not parsed.scheme.startswith("http"):
            return False

        return True

    pattern = get_blog_pattern(input_url)
    seed_url = input_url[:input_url.find(pattern) + len(pattern)]

    supabase = get_supabase()
    blogs = supabase.table("blogs").select("*").like("url", f"{seed_url}%").execute().data
    input_blog_db = get_blog_by_url(input_url)

    if blogs and input_blog_db:
        print("✅ Using cached blogs from Supabase.")
    else:
        if not blogs:
            print("🔎 Crawling and extracting all blogs for this site...")
            urls = crawl_blog_urls(seed_url, path_prefix=(pattern,))

            def normalize_url(url):
                url, _ = urldefrag(url)
                return url

            urls = list({normalize_url(u) for u in urls})

            filtered_urls = [u for u in urls if is_valid_blog_url(u, pattern)]
            filtered_urls = list(set(filtered_urls))

            print(f"\nFound {len(filtered_urls)} blog URLs after filtering:")
            for url in filtered_urls:
                print("-", url)

            print("\nExtracting content...\n")
            extracted = [extract_blog_data(url) for url in tqdm(filtered_urls, desc="Extracting blog content")]
            blogs = [b for b in extracted if b]

            def is_article_title(title):
                return not any([
                    "Page" in title,
                    "Index" in title,
                    "Archive" in title,
                ])

            blogs = [b for b in blogs if is_article_title(b["title"])]

            print(f"\n✅ Extracted {len(blogs)} valid blog posts.")

            for blog in blogs:
                sentences = clean_text(blog["content"])
                blog["sentences"] = sentences

            print(f"\n✅ Sentence split complete.")
            print(f"Example from first blog:\n")
            print(f"Title: {blogs[0]['title']}")
            for s in blogs[0]["sentences"][:5]:
                print("-", s)
            print("\n🔗 Generating embeddings from OpenAI...\n")
            embedded_blogs = [embed_blog(blog) for blog in tqdm(blogs)]
            for blog in tqdm(blogs):
                blog["embedding"] = get_embedding(blog["title"] + "\n\n" + blog["content"])
                blog["seed_url"] = seed_url
                insert_blog(blog)
        if not input_blog_db:
            print("➕ Extracting and embedding the input blog...")
            blog = extract_blog_data(input_url)
            if blog:
                blog["embedding"] = get_embedding(blog["title"] + "\n\n" + blog["content"])
                blog["seed_url"] = seed_url
                insert_blog(blog)
                blogs.append(blog)

    blogs = supabase.table("blogs").select("*").like("url", f"{seed_url}%").execute().data
    input_blog = get_blog_by_url(input_url)

    import numpy as np
    from sklearn.metrics.pairwise import cosine_similarity

    dataset_vectors = np.array([ast.literal_eval(b["embedding"]) for b in blogs if b["url"] != input_url])
    input_vector = np.array(ast.literal_eval(input_blog["embedding"])).reshape(1, -1)
    sims = cosine_similarity(input_vector, dataset_vectors)[0]

    top_indices = np.argsort(sims)[::-1]
    top_matches = []
    seen_slugs = set()
    print("\nTop 5 cosine similarity matches:")
    count = 0
    for idx in top_indices:
        if blogs[idx]["slug"] == input_blog["slug"]:
            continue
        if blogs[idx]["slug"] in seen_slugs:
            continue
        seen_slugs.add(blogs[idx]["slug"])
        score = sims[idx]
        print(f"{count+1}. {blogs[idx]['title']} (slug: {blogs[idx]['slug']}) - Score: {score:.4f}")
        top_matches.append(blogs[idx])
        count += 1
        if count == 5:
            break

    top_matches = top_matches[:3]

    def is_relevant_paragraph(paragraph):
        if not paragraph or len(paragraph.strip()) < 50:
            return False
        irrelevant_phrases = [
            "your cart is currently empty",
            "no posts found",
            "404 not found",
            "page not found",
            "subscribe to our newsletter"
        ]
        para_lower = paragraph.lower()
        return not any(phrase in para_lower for phrase in irrelevant_phrases)

    clean_content = remove_hyperlinked_text(input_blog["content_html"])
    max_chars = 6000
    full_content = clean_content[:max_chars]

    anchor_suggestions = []
    for match in top_matches:
        gpt_result = suggest_anchor(input_blog["title"], full_content, match["title"])
        print(f"\n🔗 {input_blog['title']} ➜ {match['title']}")
        print(f"Target Link   : {match['url']}")
        for suggestion in gpt_result.get("suggestions", []):
            print(f"Anchor Sentence: {suggestion['sentence']}")
            print(f"Anchor Text   : {suggestion['anchor_text']}")
            anchor_suggestions.append({
                "target_link": match["url"],
                "anchor_sentence": suggestion["sentence"],
                "anchor_text": suggestion["anchor_text"]
            })

    return {
        "anchor_suggestions": anchor_suggestions
    }