import arxiv, re, nltk, time
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from google.colab import files
def remove_urls(text):
    return re.sub(r'(http[s]?://\S+)|(www\.\S+)|(\b\S+\.(com|edu|org|net|gov|io|co)(/\S*)?)', '', text).strip()

def remove_latex_commands(text: str) -> str:
    """Removes LaTeX commands and math environments from the text.Keeps arguments for specific commands like 'textit' and 'underline'."""
    keep_arguments = {"textit": True, "underline": True}

    lines = text.splitlines(keepends=True)
    cleaned_lines = []

    for line in lines:
        # https://regex-vis.com/?r=%5C%5C%28.*%3F%29%5C%7B%28.*%3F%29%5C%7D%7C%5C%24%28.*%3F%29%5C%24
        while re.search(r"\\(.*?)\{(.*?)\}|\$(.*?)\$", line):
            match = re.search(r"\\(.*?)\{(.*?)\}|\$(.*?)\$", line)
            if match:
                cmd = match.group(1) # Command name (e.g., 'textit')
                arg = match.group(2) # Argument of the command
                math = match.group(3) # Content within $...$

                if math is not None:
                    line = re.sub(
                        r"\$(.*?)\$", "", line, count=1
                    )
                    continue

                if cmd is not None:
                    if keep_arguments.get(cmd, False):
                        line = re.sub(
                            r"\\%s{%s}" % (re.escape(cmd), re.escape(arg)),
                            arg,
                            line,
                            count=1,
                        )
                    else:
                        line = re.sub(
                            r"\\%s{.*?}" % re.escape(cmd), "", line, count=1
                        )
            else:
                break

        cleaned_lines.append(line)

    return "".join(cleaned_lines)

def extract_keywords(text, top_k=10):
    text = re.sub(r'[^a-z0-9\s]', ' ', text.lower())
    words = [w for w in word_tokenize(text) if w not in stopwords.words('english') and len(w) > 1]
    return [word for word, _ in Counter(words).most_common(top_k)]

client = arxiv.Client(page_size=200, delay_seconds=1.0, num_retries=3)
categories = ["cs.AR","cs.AI", "cs.CC", "cs.CE", "cs.CG", "cs.CL", "cs.CR", "cs.CV", "cs.CY", "cs.DB", "cs.DC", "cs.DL", "cs.DM", "cs.DS", "cs.ET", "cs.FL", "cs.GR", "cs.GT", "cs.HC",
            "cs.IR", "cs.IT", "cs.LG", "cs.LO", "cs.MA", "cs.MM", "cs.MS", "cs.NA", "cs.NE", "cs.NI", "cs.OS", "cs.PF", "cs.PL", "cs.RO", "cs.SC", "cs.SD", "cs.SE", "cs.SI", "cs.SY", "cs.GL", "cs.OH"]
papers, collected_titles = [], set()

for category in categories:
    if len(papers) >= 50000:
        break
    print(f"{category}, have collected: {len(papers)}")
    search = arxiv.Search(query=f'cat:{category}', max_results=min(1500, 50000 - len(papers)), sort_by=arxiv.SortCriterion.SubmittedDate)

    try:
        for paper in client.results(search):
            if len(papers) >= 50000:
                break
            title_clean = remove_urls(remove_latex_commands(paper.title)).lower().strip()
            if title_clean in collected_titles:
                continue
            collected_titles.add(title_clean)
            abstract_clean = remove_urls(remove_latex_commands(paper.summary)).lower()
            keywords = sorted(set(extract_keywords(title_clean) + extract_keywords(abstract_clean)))
            papers.append({
                'title_original': paper.title, 'title_cleaned': title_clean, 'abstract_original': paper.summary, 'abstract_cleaned': abstract_clean,
                'keywords': ', '.join(keywords), 'arxiv_url': paper.entry_id, 'pdf_url': paper.pdf_url,
                'category': paper.categories[0] if paper.categories else category, 'published': str(paper.published.date()) if paper.published else ''
            })
    except Exception as e:
        time.sleep(5)

df = pd.DataFrame(papers).drop_duplicates(subset=['title_cleaned']).iloc[:50000]
df.to_csv('arxiv_50k_multi_cat.csv', index=False)
files.download('arxiv_50k_multi_cat.csv')
print(f"Finished: {len(df)} papers")