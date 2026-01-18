import re
from typing import List, Tuple, Dict
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load once (module-level) for speed
NLP = spacy.load("en_core_web_sm")

WEAK_TO_STRONG_VERBS = {
    "help": "drive",
    "worked": "delivered",
    "work": "deliver",
    "did": "executed",
    "made": "built",
    "build": "engineered",
    "created": "engineered",
    "create": "engineer",
    "used": "leveraged",
    "use": "leverage",
    "responsible": "owned",
    "handled": "owned",
    "manage": "lead",
    "managed": "led",
    "improved": "optimized",
}

STOPLIKE = set([
    "experience", "skills", "ability", "responsibilities", "requirements",
    "job", "role", "team", "work", "working", "years", "year"
])

def _clean_spaces(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()

def lemmatize_for_match(text: str) -> str:
    doc = NLP(text.lower())
    lemmas = []
    for t in doc:
        if t.is_space or t.is_punct:
            continue
        if t.is_stop:
            continue
        if t.like_num:
            continue
        lemmas.append(t.lemma_)
    return " ".join(lemmas)

def extract_keywords(job_description: str, top_k: int = 12) -> List[str]:
    """
    Keyword extraction = TF-IDF terms + spaCy noun chunks.
    This is not "string replace"; it's data-driven extraction.
    """
    jd = _clean_spaces(job_description)

    # 1) TF-IDF terms
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        stop_words="english",
        min_df=1,
        max_features=2000,
    )
    X = vectorizer.fit_transform([jd])
    scores = X.toarray()[0]
    terms = vectorizer.get_feature_names_out()
    term_scores = list(zip(terms, scores))
    term_scores.sort(key=lambda x: x[1], reverse=True)
    tfidf_terms = []
    for term, score in term_scores:
        if score <= 0:
            continue
        if term in STOPLIKE:
            continue
        # filter very short junk
        if len(term) < 3:
            continue
        tfidf_terms.append(term)
        if len(tfidf_terms) >= top_k:
            break

    # 2) spaCy noun chunks (tech phrases often appear here)
    doc = NLP(jd)
    chunks = []
    for chunk in doc.noun_chunks:
        c = chunk.text.lower().strip()
        c = re.sub(r"[^a-z0-9\+\#\.\- ]", "", c)
        c = _clean_spaces(c)
        if len(c) < 3:
            continue
        if c in STOPLIKE:
            continue
        # ignore chunks made of stopwords
        if all(NLP(tok)[0].is_stop for tok in c.split()):
            continue
        chunks.append(c)

    # Combine + de-dup while keeping order preference: noun chunks first, then tf-idf
    combined = []
    seen = set()
    for k in chunks + tfidf_terms:
        if k not in seen:
            combined.append(k)
            seen.add(k)

    return combined[:top_k]

def similarity_score(bullet: str, job_description: str) -> float:
    """
    Cosine similarity using TF-IDF vectors built on both texts.
    """
    a = _clean_spaces(bullet)
    b = _clean_spaces(job_description)
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    X = vectorizer.fit_transform([a, b])
    sim = cosine_similarity(X[0], X[1])[0][0]
    return float(sim)

def keyword_gap(bullet: str, keywords: List[str]) -> Tuple[List[str], List[str]]:
    """
    Compare keyword presence using lemmatized matching.
    """
    bullet_lem = lemmatize_for_match(bullet)
    matched, missing = [], []
    for kw in keywords:
        kw_lem = lemmatize_for_match(kw)
        # naive contains on lemma space = good enough for a one-day project
        if kw_lem and kw_lem in bullet_lem:
            matched.append(kw)
        else:
            missing.append(kw)
    return matched, missing

def strengthen_leading_verb(bullet: str) -> str:
    """
    If bullet starts with a weak verb, replace with stronger one.
    Uses spaCy POS tagging to find the first verb.
    """
    text = _clean_spaces(bullet)
    doc = NLP(text)
    if not doc:
        return text

    # find first verb token near start
    for i, tok in enumerate(doc[:6]):  # only early tokens
        if tok.pos_ == "VERB":
            base = tok.lemma_.lower()
            if base in WEAK_TO_STRONG_VERBS:
                strong = WEAK_TO_STRONG_VERBS[base]
                # replace exact span token in original string carefully
                before = text[:tok.idx]
                after = text[tok.idx + len(tok.text):]
                return _clean_spaces(before + strong + after)
            break
    return text

def rewrite_bullet(bullet: str, job_description: str) -> Dict:
    """
    Main pipeline: keyword extraction -> overlap -> similarity -> rewrite.
    """
    bullet = _clean_spaces(bullet)
    job_description = _clean_spaces(job_description)

    kws = extract_keywords(job_description, top_k=12)
    matched, missing = keyword_gap(bullet, kws)
    sim = similarity_score(bullet, job_description)

    # Rewrite strategy:
    # 1) Strengthen leading verb
    # 2) Append 1-2 missing keywords as "using/with" phrase (not all; that becomes keyword stuffing)
    # 3) Keep it resume-style and concise

    improved = strengthen_leading_verb(bullet)

    # add up to 2 missing keywords (prioritize 2-grams/phrases)
    missing_sorted = sorted(missing, key=lambda x: (-len(x.split()), -len(x)))
    to_add = missing_sorted[:2]

    if to_add:
        # If bullet already has "using/with", avoid repeating; just append comma phrase
        lower = improved.lower()
        if " using " in lower or " with " in lower:
            improved = improved.rstrip(".")
            improved = f"{improved}; aligned with {', '.join(to_add)}."
        else:
            improved = improved.rstrip(".")
            improved = f"{improved} using {', '.join(to_add)}."

    # tiny cleanup: avoid double punctuation
    improved = re.sub(r"\.\.", ".", improved)
    improved = _clean_spaces(improved)

    return {
        "optimized_bullet": improved,
        "similarity": sim,
        "matched_keywords": matched,
        "missing_keywords": missing,
    }
