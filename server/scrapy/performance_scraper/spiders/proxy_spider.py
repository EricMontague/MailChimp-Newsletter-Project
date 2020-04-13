"""This module contains a class to scrape https://free-proxy-list.net/
for proxies. Only Elite proxies are used to avoid IP address detection
and to prevent a server from knowing that the request came from a proxy server.
"""

import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class EliteProxySpider(CrawlSpider):
    """Spider to crawl https://free-proxy-list.net to collect
    a list of elite proxies to be used in crawls.
    """
    
    name = "elite_proxy_spider"
    allowed_domains = ["free-proxy-list.net"]
    start_urls = ["https://free-proxy-list.net"]
    
    def parse(self, response):
        """Parse the response for elite proxies and store each proxy in
        the file defined for ROTATING_PROXY_LIST_PATH in the settings module.
        """
        ipv4_address_regex = re.compile(r"(\d{1,3}\.){3}\d{1,3}")
        proxy_list_table_rows = response.xpath("//table[@id='proxylisttable']").xpath("//tr").getall()
        elite_proxies = []
        for row in proxy_list_table_rows:
            if "elite proxy" in row:
                match = ipv4_address_regex.search(row)
                ip_address = row[match.start(): match.end()]
                elite_proxies.append(ip_address)
        self.write_to_file(elite_proxies)
        yield response

    def write_to_file(self, elite_proxies):
        """Write IPv4 addresses to a text file."""
        with open(self.settings.attributes["ROTATING_PROXY_LIST_PATH"].value, "w") as proxy_file:
            for proxy in elite_proxies:
                proxy_file.write(proxy + "/n")
    

        