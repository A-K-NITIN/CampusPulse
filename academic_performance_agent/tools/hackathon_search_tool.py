"""
Function 1 helper: hackathon discovery.
Hybrid — checks the locally-seeded/periodically-scraped CSV first, falls
back to a live web search when nothing recent/relevant is found locally.
"""
import pandas as pd
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

import config

_web_search = DuckDuckGoSearchRun()


@tool
def search_local_hackathons(domain_keyword: str = "") -> str:
    """
    Looks up hackathons already collected in the local dataset
    (data/csv/hackathons_seed.csv, refreshed periodically by a separate
    scraper job — not built in this project yet).

    Args:
        domain_keyword: optional keyword to filter by domain/description
                         (e.g. 'iot', 'web', 'ai')
    """
    try:
        df = pd.read_csv(config.HACKATHONS_CSV)
    except FileNotFoundError:
        return "No local hackathon data found."

    if domain_keyword:
        mask = (
            df["domain"].str.contains(domain_keyword, case=False, na=False)
            | df["description"].str.contains(domain_keyword, case=False, na=False)
        )
        df = df[mask]

    if df.empty:
        return "No matching hackathons found locally."

    return df.to_string(index=False)


@tool
def search_hackathons_live(query: str) -> str:
    """
    Live web search fallback for hackathons, used only when the local
    dataset has nothing relevant.

    Args:
        query: search query, e.g. 'upcoming AI hackathons India August 2026'
    """
    return _web_search.run(query)
