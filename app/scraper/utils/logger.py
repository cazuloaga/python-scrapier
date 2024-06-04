import logging

class ExcludeHTTPFilter(logging.Filter):
    def filter(self, record):
        # Exclude log messages that start with "http"
        return not record.getMessage().startswith("HTTP")


# Logger to use in project
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger()

