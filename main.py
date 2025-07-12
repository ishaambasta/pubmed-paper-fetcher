from typing import List, Dict, Union
from Bio import Entrez
import csv
import re

# Set your email; required by NCBI.
Entrez.email = "ishaambasta702@gmail.com"

def fetch_pubmed_ids(query: Union[str, List[str]], max_results: int = 5) -> List[str]:
    """
    Fetch PubMed IDs for a given query string or list of terms.
    """
    if isinstance(query, list):
        query = " ".join(query)
    query = query.strip()

    try:
        with Entrez.esearch(db="pubmed", term=query, retmax=max_results) as handle:
            results = Entrez.read(handle)
        return results.get("IdList", [])
    except Exception as e:
        print(f"❌ Error fetching PubMed IDs: {e}")
        return []

def fetch_pubmed_metadata(paper_ids: List[str]) -> List[Dict]:
    """
    Fetch MEDLINE metadata for given PubMed IDs and return parsed paper info.
    """
    if not paper_ids:
        print("⚠️ No paper IDs provided. Skipping metadata fetch.")
        return []

    try:
        with Entrez.efetch(
            db="pubmed",
            id=",".join(paper_ids),
            rettype="medline",
            retmode="text"
        ) as handle:
            raw_text = handle.read()
        return parse_medline_text(raw_text)
    except Exception as e:
        print(f"❌ Error fetching PubMed metadata: {e}")
        return []

def parse_medline_text(raw_text: str) -> List[Dict]:
    """
    Parse MEDLINE-formatted text into structured paper dictionaries.
    """
    papers = []
    entries = raw_text.strip().split("\n\n")

    for entry in entries:
        paper = {
            "pmid": "",
            "title": "",
            "authors": [],
            "affiliations": [],
            "pub_date": "",
            "email": "N/A",  # Default fallback
            "company_affiliations": []  # Initialize early to avoid KeyErrors
        }

        for line in entry.split("\n"):
            line = line.strip()
            if line.startswith("PMID-"):
                paper["pmid"] = line.replace("PMID- ", "")
            elif line.startswith("TI  -"):
                paper["title"] = line.replace("TI  - ", "")
            elif line.startswith("AU  -"):
                paper["authors"].append(line.replace("AU  - ", ""))
            elif line.startswith("AD  -"):
                affiliation = line.replace("AD  - ", "")
                paper["affiliations"].append(affiliation)

                if "@" in affiliation and paper["email"] == "N/A":
                    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", affiliation)
                    if match:
                        paper["email"] = match.group(0)
            elif line.startswith("DP  -"):
                paper["pub_date"] = line.replace("DP  - ", "")

        if paper["pmid"]:  # Only add valid papers
            papers.append(paper)

    return papers

def is_non_academic_affiliation(affiliation: str) -> bool:
    """
    Heuristically determine if affiliation is from a company, not academia.
    """
    company_keywords = {
        "inc", "ltd", "llc", "pharma", "biotech", "biosciences", "life sciences",
        "lifesciences", "therapeutics", "corporation", "corp", "gmbh", "s.a.",
        "pvt", "pharmaceutical", "laboratories"
    }
    academic_terms = {
        "university", "college", "institute", "hospital", "school", "dept"
    }

    aff_clean = " ".join(affiliation.lower().split())

    if any(term in aff_clean for term in academic_terms):
        return False
    return any(term in aff_clean for term in company_keywords)

def filter_papers_with_company_affiliations(papers: List[Dict]) -> List[Dict]:
    """
    Return only papers with at least one company-like affiliation.
    """
    filtered = []

    for paper in papers:
        company_affils = [aff for aff in paper["affiliations"] if is_non_academic_affiliation(aff)]
        if company_affils:
            paper["company_affiliations"] = company_affils  # Overwrite empty list with matches
            filtered.append(paper)

    return filtered

def save_to_csv(papers: List[Dict], filename: str = "output.csv") -> None:
    """
    Save filtered paper metadata to a CSV file.
    """
    fields = [
        "PubmedID",
        "Title",
        "Publication Date",
        "Non-academic Author(s)",
        "Company Affiliation(s)",
        "Corresponding Author Email"
    ]

    with open(filename, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        for paper in papers:
            writer.writerow({
                "PubmedID": paper.get("pmid", ""),
                "Title": paper.get("title", ""),
                "Publication Date": paper.get("pub_date", ""),
                "Non-academic Author(s)": ", ".join(paper.get("authors", [])),
                "Company Affiliation(s)": ", ".join(paper.get("company_affiliations", [])),
                "Corresponding Author Email": paper.get("email", "N/A")
            })
