from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

#== Request agent header =======================================================
_user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '\
                    'AppleWebKit/537.36 (KHTML, like Gecko) '\
                    'Chrome/39.0.2171.95 Safari/537.36'
HEADERS = {'User-Agent': _user_agent}