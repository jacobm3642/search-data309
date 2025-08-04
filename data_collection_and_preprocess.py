import requests
import pandas as pd
import re, time
import xml.etree.ElementTree as ET
import nltk
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

class ArXivCollector:
    def __init__(self):
        self.base_url = "http://export.arxiv.org/api/query"
        self.data = []
        self.collected_ids = set()
        for corpus in ['punkt', 'stopwords', 'wordnet']:
            nltk.download(corpus, quiet=True)
        self.stopwords = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
    def _get_text(self, element, xpath):
        found = element.find(xpath)
        return found.text.strip() if found is not None and found.text else ""
    def clean_text(self, text):
        if not text: return ""
        text = re.sub(r'(https?://[^\s]+|arxiv:\d+\.\d+)', ' ', text)
        text = re.sub(r'[^\w\s\.\-,;:!?%]', ' ', text)
        return re.sub(r'\s+', ' ', text).strip().lower()
    def extract_keywords(self, text, num=5):
        if not text: return ""
        tokens = word_tokenize(text.lower())
        words = [self.lemmatizer.lemmatize(word) for word in tokens
                if word.isalpha() and word not in self.stopwords and len(word) > 2]
        return "; ".join([word for word, count in Counter(words).most_common(num)])
    def fetch_papers(self, max_papers=50000, categories=['cs.AI']):
        self.data.clear()
        self.collected_ids.clear()
        target_per_category = 8000
        category_counts = Counter()
        for i, category in enumerate(categories):
            start = 0
            print(f"\n--- Fetching category: {category} ({i+1}/{len(categories)}) ---")
            while category_counts[category] < target_per_category and len(self.data) < max_papers:
                results_to_fetch = min(100, 
                                       target_per_category - category_counts[category], 
                                       max_papers - len(self.data))
                if results_to_fetch <= 0: 
                    break
                params = {'search_query': f'cat:{category}', 'start': start,'max_results': results_to_fetch, 'sortBy': 'submittedDate', 'sortOrder': 'descending'}
                try:
                    response = requests.get(self.base_url, params=params, timeout=30)
                    response.raise_for_status()
                    root = ET.fromstring(response.content)
                    entries = root.findall('{http://www.w3.org/2005/Atom}entry')
                    if not entries: 
                        break
                    collected_in_batch = 0
                    for entry in entries:
                        if len(self.data) >= max_papers: 
                            break 
                        paper_id = self._get_text(entry, '{http://www.w3.org/2005/Atom}id').split('/')[-1]
                        if paper_id in self.collected_ids: 
                            continue 
                        self.data.append({'id': paper_id,'original_title': self._get_text(entry, '{http://www.w3.org/2005/Atom}title'),'clean_title': self.clean_text(self._get_text(entry, '{http://www.w3.org/2005/Atom}title')),
                            'original_abstract': self._get_text(entry, '{http://www.w3.org/2005/Atom}summary'),'clean_abstract': self.clean_text(self._get_text(entry, '{http://www.w3.org/2005/Atom}summary')),
                            'keywords': self.extract_keywords(self.clean_text(self._get_text(entry, '{http://www.w3.org/2005/Atom}title') + " " + self._get_text(entry, '{http://www.w3.org/2005/Atom}summary'))),
                            'authors': '; '.join([self._get_text(auth, '{http://www.w3.org/2005/Atom}name') for auth in entry.findall('{http://www.w3.org/2005/Atom}author')]),
                            'published': self._get_text(entry, '{http://www.w3.org/2005/Atom}published')[:10],
                            'category': category,'arxiv_url': f"https://arxiv.org/abs/{paper_id}",'pdf_url': f"https://arxiv.org/pdf/{paper_id}.pdf"})
                        self.collected_ids.add(paper_id)
                        collected_in_batch += 1
                        category_counts[category] += 1 
                    start += len(entries) 
                except Exception as e:
                    break
            print(f"Category {category} finsih: {category_counts[category]} paper")
            if len(self.data) >= max_papers: 
                break
        return pd.DataFrame(self.data)
    def save_data(self, df, filename="arxiv_papers.csv"):
        df.to_csv(filename, index=False)
        print(f"\nDataset saved: {filename}, Total papers: {len(df)}")
def main():
    collector = ArXivCollector()
    df = collector.fetch_papers(max_papers=50000, categories=["cs.AI", "cs.AR", "cs.CC", "cs.CE", "cs.CG", "cs.CL", "cs.CR", "cs.CV", "cs.CY", "cs.DB", "cs.DC", "cs.DL", "cs.DM", "cs.DS", "cs.ET", "cs.FL", "cs.GR", "cs.GT", "cs.HC",
                     "cs.IR", "cs.IT", "cs.LG", "cs.LO", "cs.MA", "cs.MM", "cs.MS", "cs.NA", "cs.NE", "cs.NI", "cs.OS", "cs.PF", "cs.PL", "cs.RO", "cs.SC", "cs.SD", "cs.SE", "cs.SI", "cs.SY","cs.GL","cs.OH"])
    collector.save_data(df)
if __name__ == "__main__":
    main()