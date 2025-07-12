import typer
from typing import Optional, List
from main import (
    fetch_pubmed_ids,
    fetch_pubmed_metadata,
    filter_papers_with_company_affiliations,
    save_to_csv
)

app = typer.Typer()

@app.command()
def get_papers_list(
    query: List[str],
    file: Optional[str] = typer.Option(None, "--file", "-f", help="Save results to this CSV file"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug output"),
    max_results: int = typer.Option(10, "--max", "-m", help="Maximum number of results to fetch")
) -> None:
    """
    Fetch papers from PubMed and filter for company-affiliated authors.
    """
    query_str = " ".join(query)

    if debug:
        typer.echo(f"🔍 Query: {query_str}")
    
    ids = fetch_pubmed_ids(query_str, max_results)
    if debug:
        typer.echo(f"🔎 Found {len(ids)} paper IDs")

    papers = fetch_pubmed_metadata(ids)
    company_papers = filter_papers_with_company_affiliations(papers)

    if file:
        save_to_csv(company_papers, file)
        typer.echo(f"✅ Saved {len(company_papers)} papers to {file}")
    else:
        for p in company_papers:
            typer.echo(f"\n📄 {p['title']}")
            typer.echo(f"🏢 {', '.join(p['company_affiliations'])}")
            typer.echo(f"📬 {p.get('email', 'N/A')}")
            typer.echo(f"🆔 PMID: {p['pmid']}")
            typer.echo("-" * 40)

if __name__ == "__main__":
    app()
