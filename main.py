#!/usr/bin/env python3

import sys
sys.path.append("libs")
from workflow import Workflow, web


def main(wf: Workflow):
    """Alfred workflow that gets a word/phrase as input and returns synonyms found by scraping google"""

    from bs4 import BeautifulSoup

    query = sys.argv[1]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    params = {
        'q': f'synonyms for {query.replace(" ", "+")}',
        'ie': 'UTF-8',
        'oe': 'UTF-8',
        'client': 'safari',
        'rls': 'en',
        'hl': 'en',
    }

    r = web.get('https://www.google.com/search', headers=headers, params=params)
    soup = BeautifulSoup(r.content, features='html.parser')

    items = []

    try:
        results = soup.select('.EmSASc.gWUzU.MR2UAc.F5z5N.jEdCLc.LsYFnd.p9F8Cd.I6a0ee.rjpYgb.gjoUyf > span')

        for result in results:
            item = wf.add_item(
                title=result.text,
                arg=result.text,
                valid=True,
            )
            item.add_modifier('cmd', subtitle=f'Search for "{query}"', arg=r.url)
            items.append(item)
    except (AttributeError, IndexError):
        item = wf.add_item(
            title=f"No results for '{query}'",
            subtitle='Try searching another word/phrase',
            valid=False
        )
        item.add_modifier('cmd', subtitle=f'Search for "{query}"', arg=r.url)

    if len(items) < 2:
        item = wf.add_item(
            title=f'End of list.',
            valid=False
        )
        item.add_modifier('cmd', subtitle=f'Search for "{query}"', arg=r.url)

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow(update_settings={
        'github_slug': 'OmerAvital/AlfredSynonym',
    })

    if wf.update_available:
        # Download new version and tell Alfred to install it
        wf.start_update()

    sys.exit(wf.run(main))
