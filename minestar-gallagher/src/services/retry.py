from tenacity import retry, stop_after_attempt, wait_exponential

# Reusable retry decorator
default_retry = retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    reraise=True
)