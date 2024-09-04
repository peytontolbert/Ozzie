import requests
from bs4 import BeautifulSoup
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class WebScraper:
    def __init__(self):
        self.logger = Logger("WebScraper")
        self.error_handler = ErrorHandler()

    def scrape_webpage(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        except requests.RequestException as e:
            self.error_handler.handle_error(e, f"Failed to scrape webpage: {url}")
            return None

    def extract_text(self, soup):
        return soup.get_text()

    def extract_links(self, soup):
        return [link.get('href') for link in soup.find_all('a')]

    def extract_structured_data(self, soup):
        # This method would be customized based on the specific webpage structure
        data = {}
        # Example: Extract all h1 and p tags
        data['headings'] = [h1.text for h1 in soup.find_all('h1')]
        data['paragraphs'] = [p.text for p in soup.find_all('p')]
        return data

    def enrich_knowledge_graph(self, url, knowledge_graph):
        soup = self.scrape_webpage(url)
        if not soup:
            return False

        try:
            # Create a node for the webpage
            webpage_node = knowledge_graph.create_node("Webpage", {"url": url})

            # Add extracted text as a property
            text = self.extract_text(soup)
            knowledge_graph.update_node_property(webpage_node, "content", text)

            # Add links as relationships
            links = self.extract_links(soup)
            for link in links:
                link_node = knowledge_graph.create_node("Webpage", {"url": link})
                knowledge_graph.create_relationship(webpage_node, link_node, "LINKS_TO")

            # Add structured data
            structured_data = self.extract_structured_data(soup)
            for key, value in structured_data.items():
                knowledge_graph.update_node_property(webpage_node, key, value)

            return True
        except Exception as e:
            self.error_handler.handle_error(e, f"Error enriching knowledge graph with data from {url}")
            return False