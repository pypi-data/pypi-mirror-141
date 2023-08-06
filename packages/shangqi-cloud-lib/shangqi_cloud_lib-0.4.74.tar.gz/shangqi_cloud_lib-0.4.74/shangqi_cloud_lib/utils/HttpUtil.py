import json
import logging
import traceback

import requests

from shangqi_cloud_lib.context import config


def send_http_post(route, data, is_module=False, ip=config.data_server_ip, port=config.data_server_port):
    result = None
    url = "http://{}:{}/{}".format(ip, port, route)
    try:
        if is_module:
            result = json.loads(requests.post(url, data=json.dumps(data)).content)
        else:
            result = json.loads(requests.post(url, data=json.dumps(data)).content).get("data", None)
    except:
        logging.info(traceback.format_exc())
    finally:
        return result


def send_http_get(route, param_dict,ip=config.data_server_ip, port=config.data_server_port):
    url = "http://{}:{}/{}?".format(ip, port, route)
    for param in param_dict:
        url = url + param + "=" + str(param_dict[param]) + "&"
    result = None
    try:
        result = json.loads(requests.get(url[:-1]).content).get("data", None)
    except:
        logging.info(traceback.format_exc())
    finally:
        return result
