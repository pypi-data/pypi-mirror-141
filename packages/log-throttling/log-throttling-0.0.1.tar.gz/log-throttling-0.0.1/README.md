# log-throttling
A light-weight python log throttling utility

```python
import time
import logging
import log_throttling

logger = logging.getLogger(__name__)

start = time.monotonic()
while time.monotonic() - start < 10:
    log_throttling.by_time(logger, interval=1).info(
        "This line will be logged once every second."
    )
    time.sleep(0.01)

for i in range(100):
    log_throttling.by_count(logger, once_every=10).info(
        "This line will only log values that are multiples of 10: %s", i
    )
```