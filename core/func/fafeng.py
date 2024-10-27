"""
发疯nonebot2插件
调用api https://fb.viki.moe/ 
并将返回的文本中的[name]替换返回给用户
"""
import requests
import nonebot as nb
from nonebot.adapters.onebot.v11 import Message,Event
from nonebot.params import CommandArg


def fadian(name):
    url = "https://fb.viki.moe/"
    headers = {
       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    # get 页面的text
    response = requests.get(url, headers=headers)
    text = response.text
    # 替换可能有多个的[name]
    text = text.replace("[name]", name)
    return text

e = nb.on_command("发疯", aliases={"发颠", "发病"})
@e.handle()
async def _(event: Event , args: Message = CommandArg()):
    # 检查消息中有没有at
    msg = event.get_message()
    for i in msg:
        if i.type == "at":
            name = i.data.get("name","unknown")
            name = name.replace("@", "")
            break
        else:
            name = "unknown"
    if name == "unknown":
        if temp := args.extract_plain_text():
            name = temp
        else:
            await e.finish("你没有填写要发疯的名字~")
    try:
        text = fadian(name)
    except:
        text = "api寄了..."
    finally:
        await e.send(text)
        await e.finish()
        
if __name__ == "__main__":
    print(
        "以下为测试\n",
        fadian("Jerry")
    )