import re
from typing import Dict, Optional
from pathlib import Path

import hashlib

import httpx
import anyio
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Message, MessageSegment, helpers


def parse_msg(msg: str) -> str:
    """
    :说明: `parse_msg`
    > 替换回答中的 `/at`, `/self`, `/atself`

    :参数:
      * `msg: str`: 待处理的消息

    :返回:
      - `str`: 消息
    """
    msg = re.sub(r"{", "{{", msg)
    msg = re.sub(r"}", "}}", msg)
    msg = re.sub(r"/at\s*(\d+)", lambda s: f"[CQ:at,qq={s.group(1)}]", msg)
    msg = re.sub(r"/self", "{nickname}", msg)
    msg = re.sub(r"/atself", "{sender_id:at}", msg)
    return msg


async def get_img(url: str) -> Optional[bytes]:
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",  # noqa
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53",  # noqa
    }
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers)
            return resp.content
    except httpx.TimeoutException:
        logger.warning(f"图片下载失败：{url}")
        return None


async def save_img(img: bytes, filepath: Path):
    async with await anyio.open_file(filepath, "wb") as f:
        await f.write(img)


async def save_and_convert_img(msg: Message, img_dir: Path):
    """
    :说明: `save_and_convert_img`
    > 保存消息中的图片，并替换 `file` 中的文件名为本地路径

    :参数:
      * `msg: Message`: 待处理的消息
      * `img_dir: Path`: 图片保存路径
    """
    p_list = helpers.extract_image_urls(msg)
    logger.info(f"开始下载图片：{p_list}")
    for url in p_list:
       # 检查图片文件夹中有无同名文件
        images = [f.name for f in img_dir.iterdir() if f.is_file()]
        md5_val = hashlib.md5(url.encode('utf8')).hexdigest()
        filepath = img_dir / md5_val
        if url not in images:
            data = await get_img(url)
            if not data:
                continue
            await save_img(data, filepath)



def compare_msgseg(msg1: MessageSegment, msg2: MessageSegment) -> bool:
    """
    :说明: `compare_msgseg`
    > 判断两个消息段是否一致，目前仅判断 text, face, at, image 类型

    :参数:
      * `msg1: MessageSegment`: 消息段1
      * `msg2: MessageSegment`: 消息段2

    :返回:
      - `bool`: 是否一致
    """
    if msg1.type != msg2.type:
        return False
    msg_type = msg1.type
    if msg_type == "text":
        return msg1.data["text"] == msg2.data["text"]
    elif msg_type == "face":
        return msg1.data["id"] == msg2.data["id"]
    elif msg_type == "at":
        return msg1.data["qq"] == msg2.data["qq"]
    elif msg_type == "image":
        return msg1.data["file"] == msg2.data["file"]
    return False


def compare_msg(msg1: Message, msg2: Message) -> bool:
    """
    :说明: `compare_msg`
    > 判断两个消息是否一致

    :参数:
      * `msg1: Message`: 消息1
      * `msg2: Message`: 消息2

    :返回:
      - `bool`: 是否一致
    """
    for m1, m2 in zip(msg1, msg2):
        if m1.type != m2.type:
            return False
        if not compare_msgseg(m1, m2):
            return False
    return True


def include_msg(msg1: Message, msg2: Message) -> bool:
    """
    :说明: `include_msg`
    > 判断 消息1 是否包含 消息2，用于模糊匹配

    :参数:
      * `msg1: Message`: 消息1
      * `msg2: Message`: 消息2

    :返回:
      - `bool`: 是否包含
    """
    for m1, m2 in zip(msg1, msg2):
        if m1.type != m2.type:
            return False
        if m1.type == "text":
            if str(m2.data["text"]).strip() not in m1.data["text"]:
                return False
        elif not compare_msgseg(m1, m2):
            return False
    return True


def to_json(msg: Message, name: str, bot_id: str) -> Dict:
    return {
        "type": "node",
        "data": {
            "name": name,
            "uin": bot_id,
            "content": msg,
        },
    }
