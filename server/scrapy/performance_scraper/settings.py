"""This module contains settings for the Scrapy project."""


import os 

BASEDIR = os.path.abspath(os.path.dirname(__file__))

SCRAPY_USERNAME = os.environ.get("SCRAPY_USERNAME", "scrapy")
SCRAPY_PASSWORD = os.environ.get("SCRAPY_PASSWORD", "password")
SCRAPY_EMAIL = os.environ.get("SCRAPY_EMAIL", "scrapy@gmail.com")
IMAGE_DOWNLOAD_DIRECTORY = BASEDIR + "/artist_images"
TOKEN_FILE_PATH =  BASEDIR + "/flask_api/token.json"

BOT_NAME = "performance_scraper"

SPIDER_MODULES = ["performance_scraper.spiders"]
NEWSPIDER_MODULE = "performance_scraper.spiders"


ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 3

# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False


# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
  "Accept-Language": "en",
}

SPIDER_MIDDLEWARES = {
   "scrapy_splash.SplashDeduplicateArgsMiddleware": 100
}

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
   "scrapy_splash.SplashCookiesMiddleware": 723,
   "scrapy_splash.SplashMiddleware": 725,
   "scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware": 810,
   "performance_scraper.middlewares.PerformanceScraperDownloaderMiddleware": 543,
}

SPLASH_URL = "http://0.0.0.0:8050"
DUPEFILTER_CLASS = "scrapy_splash.SplashAwareDupeFilter"
HTTPCACHE_STORAGE = "scrapy_splash.SplashAwareFSCacheStorage"


# Configure item pipelines
ITEM_PIPELINES = {
   "performance_scraper.pipelines.ArtistImagePipeline": 1,
   "performance_scraper.pipelines.APIPipeline": 300
}

IMAGES_STORE = BASEDIR + "/artist_images"
IMAGES_URLS_FIELD = "image"
IMAGES_RESULT_FIELD = "path"

# Enable and configure the AutoThrottle extension (disabled by default)
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

