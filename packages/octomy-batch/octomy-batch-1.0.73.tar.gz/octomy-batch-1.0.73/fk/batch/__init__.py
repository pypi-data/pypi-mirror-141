import logging
import pprint
import json
import datetime
from fk.utils import human_delta

logger = logging.getLogger(__name__)


def log_item(item):
    # logger.info(pprint.pformat(item))
    logger.info(item_to_str(item))


def item_to_str(item):
    prefix = "#=- "
    ret = "\n"
    if not item:
        ret = f"""
{prefix}
{prefix}Job:    NONE
{prefix}
"""
        return ret
    ret += f"{prefix}\n"
    type = item.get("type", "unknown-type")
    id = item.get("id", "XXXXXXX")
    ret += f"{prefix}BATCH JOB {type}: {id}\n"
    try:
        now = datetime.now()
        created_ago = human_delta(now - item.get("created_at"), None)
        updated_ago = human_delta(now - item.get("updated_at"), None)
        ret += f"{prefix}Created: {created_ago}, Updated: {updated_ago} ####\n"
    except:
        pass
    try:
        source = item.get("source")
        if source:
            ret += f"{prefix}Source: {source}\n"
        status = item.get("status")
        if status:
            ret += f"{prefix}Status: {status}\n"
    except:
        pass
    data_raw = item.get("data")
    if data_raw:
        ret += f"{prefix}Data:\n\n"
        try:
            data = json.loads(data_raw)
            data_str = json.dumps(data, indent=3, sort_keys=True, default=str)
            ret += data_str + "\n\n"
        except json.JSONDecodeError as e:
            ret += f"{prefix}JSON PARSE ERROR\n"
    result_raw = item.get("result")
    if result_raw:
        ret += f"{prefix}Result:\n\n"
        try:
            result = json.loads(result_raw)
            result_str = json.dumps(result, indent=3, sort_keys=True, default=str)
            ret += result_str + "\n\n"
        except json.JSONDecodeError as e:
            ret += result_raw + "\n\n"
    ret += f"{prefix}\n"
    return ret
