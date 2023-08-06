import json
import redis
import logging

from shangqi_cloud_lib.context import config
from shangqi_cloud_lib.utils.CommonUtil import CJsonEncoder


def redis_connect(host=None, port=None, **options):
    if not host:
        host = config.redis_ip
    if not port:
        port = config.redis_port
    try:
        redis_conn = redis.Redis(host=host, port=port, **options)
    except ConnectionError as e:
        logging.warning(f"缓存服务连接失败：{e}")
        redis_conn = {}
    return redis_conn


def get_cache(key, decode=True):
    value = redis_connect().get(key)
    if value:
        if decode:
            result = json.loads(value.decode())
        else:
            result = value
        logging.info("hit cache: {}".format(key))
        return result
    logging.debug("miss cache: {}".format(key))
    return None


def set_cache(key, value, ex=6 * 3600, px=None, nx=False, xx=False, keepttl=False):
    logging.debug(f"set cache: {key}")
    try:
        redis_conn = redis_connect()
        if isinstance(value, dict):
            redis_conn.set(key, json.dumps(value, cls=CJsonEncoder, ensure_ascii=False), ex, px, nx, xx, keepttl)
        else:
            redis_conn.set(key, value, ex, px, nx, xx, keepttl)
    except ConnectionError as e:
        logging.warning(f"缓存服务连接失败：{e}")
    except TimeoutError as e:
        logging.warning(f"缓存连接超时: {e}")
