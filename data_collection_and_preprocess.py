#!pip install arxiv
import arxiv, re, nltk, time
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

def remove_urls(text):
    """Remove URLs, website links, and common domains from text"""
    return re.sub(r'(http[s]?://\S+)|(www\.\S+)|(\b\S+\.(?:com|edu|org|net|gov|io|co)(?:/\S*)?)', '', text, flags=re.IGNORECASE).strip()
    
def remove_latex_commands(text: str) -> str:
    """Remove LaTeX commands while preserving some formatting and handling special cases. Extended to handle complex formulas like \frac{}{}, \sum, \int, etc."""
    keep_arguments = {"textit": True, "underline": True, "textbf": True}
    lines = text.splitlines(keepends=True)
    cleaned_lines = []
    
    for line in lines:
        line = re.sub(r'\$?\^\{?([^}\$]+)\}?\$?', r'^\1', line)
        line = re.sub(r'_\{(.*?)\}', r'_\1', line)
        line = re.sub(r'\$+', '', line)  # Remove remaining $ symbols
        line = re.sub(r'\\begin\{.*?\}.*?\\end\{.*?\}', ' ', line, flags=re.DOTALL)
        line = re.sub(r'\\(?!(textit|underline|textbf)\b)[a-zA-Z]+\{.*?\}', ' ', line)
        line = re.sub(r'\\([%&_])', r'\1', line)
        while re.search(r"\\(textit|underline|textbf)\{(.*?)\}", line):
            match = re.search(r"\\(textit|underline|textbf)\{(.*?)\}", line)
            if match:
                cmd = match.group(1)
                arg = match.group(2)
                line = re.sub(r"\\%s\{%s\}" % (re.escape(cmd), re.escape(arg)), arg, line, count=1)
        
        line = re.sub(r'\\frac\{.*?\}\{.*?\}', ' ', line)  
        line = re.sub(r'\\sqrt\{.*?\}', ' ', line)         
        line = re.sub(r'\\(?:sum|int|prod)(?:\s*\^.*?)?\{.*?\}', ' ', line)
        line = line.replace('\\', ' ')
        cleaned_lines.append(line)
    
    result = "".join(cleaned_lines)
    result = re.sub(r'\s+', ' ', result).strip()  # Collapse multiple spaces
    return result
    
def clean_text(text: str, lowercase: bool = True) -> str:
    """Combine all cleaning steps: LaTeX, URLs, extra spaces, and optional lowercase"""
    text = remove_latex_commands(text)
    text = remove_urls(text)
    if lowercase:
        text = text.lower() 
    text = re.sub(r'\s+', ' ', text)  # Collapse multiple spaces
    return text.strip()

def extract_keywords(text, top_k=10):
    """Extract keywords from cleaned text (assumes text is already cleaned)"""
    text = re.sub(r'[^a-z0-9\s]', ' ', text)  # Additional cleaning
    words = [w for w in word_tokenize(text) 
             if w not in stopwords.words('english') and len(w) > 1]
    return [word for word, _ in Counter(words).most_common(top_k)]

client = arxiv.Client(page_size=100, delay_seconds=3.0, num_retries=3)
categories = ["cs.AI", "cs.AR", "cs.CC", "cs.CE", "cs.CG", "cs.CL", "cs.CR", "cs.CV", "cs.CY", "cs.DB", "cs.DC", "cs.DL", "cs.DM", "cs.DS", "cs.ET", "cs.FL", "cs.GR", "cs.GT", "cs.HC",
            "cs.IR", "cs.IT", "cs.LG", "cs.LO", "cs.MA", "cs.MM", "cs.MS", "cs.NA", "cs.NE", "cs.NI", "cs.OS", "cs.PF", "cs.PL", "cs.RO", "cs.SC", "cs.SD", "cs.SE", "cs.SI", "cs.SY", "cs.GL", "cs.OH"]

papers, collected_titles = [], set()
target_papers = 50000

for category in categories:
    if len(papers) >= target_papers:
        break
    print(f"Fetching {category}... Collected: {len(papers)}/{target_papers}")
    search = arxiv.Search(query=f'cat:{category}',max_results=min(5000, target_papers - len(papers)),sort_by=arxiv.SortCriterion.SubmittedDate)

    try:
        for paper in client.results(search):
            if len(papers) >= target_papers:
                break
            title_clean = clean_text(paper.title)
            if title_clean in collected_titles:
                continue
            collected_titles.add(title_clean)
            abstract_clean = clean_text(paper.summary)
            keywords = sorted(set( extract_keywords(title_clean) + extract_keywords(abstract_clean)))
            papers.append({'title_original': paper.title,'title_cleaned': title_clean,'abstract_original': paper.summary,'abstract_cleaned': abstract_clean,'keywords': ', '.join(keywords),
                'arxiv_url': paper.entry_id,'pdf_url': paper.pdf_url,'category': paper.categories[0] if paper.categories else category,'published': str(paper.published.date()) if paper.published else ''})
            
    except Exception as e:
        time.sleep(5)

df = pd.DataFrame(papers).drop_duplicates(subset=['title_cleaned']).iloc[:target_papers]
output_filename = f'arxiv_{len(df)}_papers.csv'
df.to_csv(output_filename, index=False)
print(f"\nFinished! Collected {len(df)} papers.")
