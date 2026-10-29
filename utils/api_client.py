import json
import time
import requests
import allure

from utils.config_reader import get_property
from utils.logger import get_logger

logger = get_logger("api_client")


class ApiClient:
    def __init__(self, base_url=None, context=None):
        if not base_url:
            base_url = get_property("API_BASE_URL", context=context) or get_property("api.base_url", context=context) or "https://reqres.in"
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.last_response = None

    def _build_url(self, endpoint):
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            return endpoint
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def _execute(self, method, endpoint, **kwargs):
        url = self._build_url(endpoint)
        logger.info(f"API Request: {method.upper()} {url}")

        start_time = time.time()
        try:
            response = self.session.request(method=method, url=url, **kwargs)
            duration_ms = int((time.time() - start_time) * 1000)
            self.last_response = response

            logger.info(f"API Response: {response.status_code} [{duration_ms}ms]")

            # Attach request & response details to Allure
            try:
                payload_str = json.dumps(kwargs.get("json", {}), indent=2) if "json" in kwargs else str(kwargs.get("data", ""))
                try:
                    resp_body = json.dumps(response.json(), indent=2)
                except Exception:
                    resp_body = response.text

                allure_content = (
                    f"URL: {method.upper()} {url}\n"
                    f"Headers: {dict(response.request.headers)}\n"
                    f"Payload: {payload_str}\n\n"
                    f"Status Code: {response.status_code}\n"
                    f"Duration: {duration_ms} ms\n"
                    f"Response Body:\n{resp_body}"
                )
                allure.attach(
                    allure_content,
                    name=f"{method.upper()} {endpoint} [{response.status_code}]",
                    attachment_type=allure.attachment_type.TEXT
                )
            except Exception as allure_err:
                logger.debug(f"Could not attach API call to Allure: {allure_err}")

            return response
        except requests.RequestException as e:
            logger.error(f"API Request Failed: {method.upper()} {url} - Error: {e}")
            raise

    def get(self, endpoint, **kwargs):
        return self._execute("GET", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self._execute("POST", endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self._execute("PUT", endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self._execute("DELETE", endpoint, **kwargs)

