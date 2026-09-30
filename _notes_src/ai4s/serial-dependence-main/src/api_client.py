import time
import re
import requests
from typing import List, Dict, Any, Optional

class DMXClient:
    def __init__(self, base_url: str, api_key: str, timeout: int = 60):
        if not api_key:
            raise RuntimeError("api_key is required. Provide it via --api_key or config.yaml.")
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })

    def chat_completion(self, model: str, messages: List[Dict[str, str]], temperature: float = 0.0,
                        extra: Optional[Dict[str, Any]] = None, max_retries: int = 5, backoff_base: float = 1.5) -> str:
        """Call DMXAPI's OpenAI-compatible /chat/completions endpoint and return the message content string."""
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }
        if extra:
            payload.update(extra)

        url = f"{self.base_url}/chat/completions"
        for attempt in range(max_retries):
            try:
                resp = self._session.post(url, json=payload, timeout=self.timeout)
                if resp.status_code == 200:
                    data = resp.json()
                    content = data["choices"][0]["message"]["content"]
                    return content
                # recoverable errors
                if resp.status_code in (429, 500, 502, 503, 504):
                    sleep_s = backoff_base ** attempt
                    time.sleep(sleep_s)
                    continue
                # other HTTP errors -> raise
                resp.raise_for_status()
            except requests.RequestException:
                sleep_s = backoff_base ** attempt
                time.sleep(sleep_s)
                continue
        raise RuntimeError("API request failed after retries.")

    @staticmethod
    def parse_rating_1_to_5_decimal(text: str) -> Optional[float]:
        """
        Extract the first numeric value in [1, 5] with up to two decimals,
        then round to exactly two decimals.
        Robust to outputs like '3', '3.5', '3.50'. Returns None if not found.
        """
        if text is None:
            return None

        # 允许 1–4 带 0–2 位小数，5 允许 5, 5.0, 5.00；屏蔽诸如 5.23、0.99、6 等
        m = re.search(r'(?<![\d.])([1-4](?:\.\d{1,2})?|5(?:\.0{0,2})?)(?![\d.])', text)
        if not m:
            return None

        try:
            val = DEC(m.group(1))
        except decimal.InvalidOperation:
            return None

        # 保险起见：夹取范围，并统一四舍五入两位
        if val < DEC("1") or val > DEC("5"):
            return None
        return float(val.quantize(DEC("0.01"), rounding=decimal.ROUND_HALF_UP))
    '''
    def parse_rating_1_to_5(text: str) -> Optional[int]:
        """Extract the first integer between 1 and 5 from the response text."""
        if text is None:
            return None
        m = re.search(r"([1-5])", text)
        if not m:
            return None
        return int(m.group(1))'''
