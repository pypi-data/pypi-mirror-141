from datetime import datetime
from http.client import IncompleteRead
from socket import timeout
import sys
from time import mktime
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from xml.etree.ElementTree import fromstring, ElementTree, ParseError

from bs4 import BeautifulSoup
import dateutil.parser
import feedparser
import requests

PODCAST_NAMESPACE_URI = 'https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md'
HEADERS = {'User-Agent': 'feedparsley'}

PARSER_FEEDPARSER = 1
PARSER_ELEMENTTREE = 2

def _parse_feed_datetime(dt):
    if not dt:
        return None
    try:
        return datetime.fromtimestamp(mktime(dt))
    except ValueError:
        return None
    except OverflowError:
        return None

def _parse_datetime(dt):
    return dateutil.parser.parse(dt)

def _parse_rss_item(item):
    description_el = item.find('description')
    enclosure = None
    enclosure_el = item.find('enclosure')
    if enclosure_el is not None:
        enclosure = {'href': enclosure_el.get('url'), 'type': enclosure_el.get('type'), 'length': enclosure_el.get('length')}
    link = item.find('link')
    if link is not None:
        url = link.text
    elif enclosure:
        url = enclosure['href']
    else:
        url = None
    return {'title': item.find('title').text,
            'url': url,
            'content': description_el.text if description_el is not None else None,
            'enclosure': enclosure,
            'updated_at': _parse_datetime(item.find('pubDate').text)}

def _parse_feed_item(item):
    enclosure_links = [l for l in item['links'] if l['rel'] == 'enclosure']
    url = item.get('link')
    if not url and enclosure_links:
        url = enclosure_links[0]['href']
    updated_at = _parse_feed_datetime(item.get('updated_parsed')) or (_parse_datetime(item['updated']) if item['updated'] else None)
    return {'title': item['title'],
            'url': url,
            'content': item['content'][0]['value'] if item.get('content') else item.get('summary'),
            'enclosure': enclosure_links[0] if enclosure_links else None,
            'updated_at': updated_at}

def _parse_valuespec(root):
    value_spec = None
    value_recipients = []

    value_el = root.find('channel/{%s}value' % PODCAST_NAMESPACE_URI)
    if value_el is not None:
        value_spec = {}
        value_spec['protocol'] = value_el.attrib['type']
        value_spec['method'] = value_el.attrib['method']
        value_spec['suggested_amount'] = float(value_el.attrib.get('suggested', 0))
        for value_recipient_el in value_el.findall('{%s}valueRecipient' % PODCAST_NAMESPACE_URI):
            value_recipient = {}
            value_recipient['name'] = value_recipient_el.attrib.get('name')
            value_recipient['address_type'] = value_recipient_el.attrib['type']
            value_recipient['address'] = value_recipient_el.attrib['address']
            value_recipient['custom_key'] = value_recipient_el.attrib.get('customKey')
            value_recipient['custom_value'] = value_recipient_el.attrib.get('customValue')
            value_recipient['split'] = int(value_recipient_el.attrib['split'])
            value_recipients.append(value_recipient)

    return value_spec, value_recipients

def parse_feed(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if not response.ok:
            return
        content = response.text
    except Exception as e:
        return
    if len(content) < 10:
        return

    parsed_feed = None

    try:
        f = feedparser.parse(content)
    except RuntimeError:
        f = None

    if f and f['feed'] and f['feed'].get('title') and f['feed'].get('link'):
        value_spec = None
        value_recipients = []
        # HACK: feedparser doesn't yet parse the "podcast" namespace properly
        # (see https://github.com/kurtmckee/feedparser/issues/301)
        # so we should parse this part separately
        if 'podcast' in f['namespaces']:
            root = None
            try:
                root = fromstring(content)
            except ParseError as e:
                pass
            if root:
                value_spec, value_recipients = _parse_valuespec(root)
        items = []
        for e in f['entries']:
            if e and e.get('title'):
                item = _parse_feed_item(e)
                if item['url']:
                    items.append(item)
        return {'title': f['feed']['title'],
                'updated_at': _parse_feed_datetime(f['feed'].get('updated_parsed')),
                'items': items,
                'value_spec': value_spec, 'value_recipients': value_recipients,
                'parser': PARSER_FEEDPARSER}

    try:
        root = fromstring(content)
    except ParseError as e:
        return

    title_el = root.find('channel/title')
    if title_el is None:
        return
    date_el = root.find('channel/lastBuildDate')

    value_spec, value_recipients = _parse_valuespec(root)

    items = []
    for item in root.findall('channel/item'):
        item = _parse_rss_item(item)
        if item['url']:
            items.append(item)
    return {'title': title_el.text,
            'updated_at': _parse_datetime(date_el.text) if date_el else None,
            'items': items,
            'value_spec': value_spec, 'value_recipients': value_recipients,
            'parser': PARSER_ELEMENTTREE}

def extract_feed_links(url, content):
    parsed_url = urlparse(url)
    netloc = parsed_url.netloc
    netloc_nowww = netloc
    if netloc_nowww.startswith("www."):
        netloc_nowww = netloc_nowww[len("www."):]
    base_url = f"{parsed_url.scheme}://{netloc}"
    soup = BeautifulSoup(content, 'html.parser')
    alt_links = []
    for link in soup.find_all('link', rel='alternate'):
        if link.attrs.get('type') in ['application/atom+xml', 'application/rss+xml']:
            href = (link.attrs['href'] or "").strip()
            if not href:
                continue
            title = link.attrs.get('title')
            if href.startswith(f"//{netloc}") or href.startswith(f"//{netloc_nowww}"):
                href = f"{parsed_url.scheme}:{href}"
            elif href.startswith('/'):
                href = f"{base_url}{href}"
            elif href.startswith('../') or '/' not in href:
                href = f"{base_url}/{href}"
            if "://" not in href:
                href = f"http://{href}"

            alt_links.append((href, title))

    presumably_comment_feed_urls = {l[0] for l in alt_links
        if l[1] and any(c in l[1].lower() for c in ["comments", "commentaires", "kommentar", "comentarios"])
        or "/comments/" in l[0]}

    alt_links_without_presumably_comment_feeds = [l for l in alt_links if l[0] not in presumably_comment_feed_urls]

    return alt_links_without_presumably_comment_feeds or alt_links

def main():
    url = sys.argv[1]
    content = requests.get(url).text
    feed_links = extract_feed_links(url, content)
    if feed_links:
        print(feed_links)
    else:
        parsed_feed = parse_feed(url)
        print(f"TITLE: {parsed_feed['title']} UPDATED: {parsed_feed['updated_at']} ITEMS: {len(parsed_feed['items'])} VALUE SPEC: {bool(parsed_feed['value_spec'])}")
