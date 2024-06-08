from celery import shared_task
from .coinmarketcap import CoinMarketCap
import logging

logger = logging.getLogger(__name__)

@shared_task
def scrape_coin_data(coin):
    try:
        logger.info(f"Scraping data for coin: {coin}")
        scraper = CoinMarketCap()
        result = scraper.scrape_coin(coin)
        logger.info(f"Scraping successful for coin: {coin}")
        return result
    except Exception as e:
        logger.error(f"Error scraping data for coin {coin}: {e}")
        raise
