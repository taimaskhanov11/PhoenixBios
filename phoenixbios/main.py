from loguru import logger

from phoenixbios.config import CONFIG
from phoenixbios.phoenix import PhoenixBios

logger.add(
    sink=f"logs/mainlog.log",
    level="TRACE",
    enqueue=True,
    encoding="utf-8",
    diagnose=True,
)

@logger.catch
def main():
    p = PhoenixBios(config=CONFIG)
    p.start()



if __name__ == '__main__':
    main()
