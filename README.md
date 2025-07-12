#  PubMed Company-Affiliated Paper Finder

A command-line tool that:

- Queries PubMed using user-defined keywords
- Retrieves paper metadata
- Filters for research papers with at least one **non-academic** author (e.g., from pharmaceutical or biotech companies)

-------------------------------------------------------------------------------------------------------------------------

##  Installation

Requires:
•   Python 3.11+
•   [Poetry](https://python-poetry.org/)
•   git clone https://github.com/ishaambasta/pubmed-paper-fetcher.git
•   cd pubmed-paper-fetcher
•   poetry install
•   poetry shell

💡 How to Use
•   python cli.py get-papers-list --query "covid vaccine" --file results.csv --debug

🔧 CLI Options
•   --query, -q: Keywords to search on PubMed (required)

•   --file, -f: Output CSV filename to save results

•   --debug, -d: Show debug output while running


📦 Tools Used
•   Typer: Build the CLI interface

•   BioPython: Access PubMed and parse MEDLINE data

•   csv module: Export results to file

•   re module: Extract emails from affiliations

•   Python typing: Used throughout for clarity and maintainability

🛠 Developer Notes
•   Modular code:

    •   main.py: Logic

    •   cli.py: CLI

•   Managed via Poetry — no requirements.txt needed

    •   Error handling covers:

    •   No search results

    •   PubMed API issues

    •   Missing metadata fields

•   Heuristics used to detect company affiliations (e.g., domain names, company keywords)
    •   Email domains

    •   Keywords in affiliations

•   Built with a learning mindset, guided by LLM assistance

✅ Example Output
📄 A Phase 1 Trial of XYZ Therapeutics...
🏢 ABC Pharmaceuticals, XYZ Biosciences
📬 author@example.com
🆔 PMID: 12345678

🧪 Testing

•   Query: 
python cli.py get-papers-list --query "cancer vaccine" --debug

•   Nonsense word:
python cli.py get-papers-list --query asdfghjkllololol

•   Expected output:
❗ No paper IDs found for this query. Try using more common terms.

🤖 LLM Assistance Disclosure
•   This project was built with help from OpenAI ChatGPT, used for:

•   Understanding Typer and BioPython quickly

•   Improving function design and code clarity

•   Following clean, modular coding best practices

🙋‍♀️ Author
Isha Ambasta
GitHub: @ishaambasta
