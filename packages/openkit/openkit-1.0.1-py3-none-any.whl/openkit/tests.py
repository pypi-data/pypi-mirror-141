import logging
import time

from api.openkit import Openkit

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(funcName)s - %(message)s"))
logger.addHandler(handler)


def main():
    beacon_url = "https://bf08232drt.bf-dev.dynatracelabs.com/mbeacon"
    app_id = "7b0476b7-bcb4-4f10-806f-45c2df271ec0"
    ok = Openkit(beacon_url, app_id, "1", logger=logger)

    session = ok.create_session("192.168.15.1")
    time.sleep(2)
    session.end()
    time.sleep(5)

    ok.shutdown()


if __name__ == "__main__":
    main()
