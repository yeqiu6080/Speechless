from nonebot import on_command,logger,get_driver
from nonebot.permission import SUPERUSER
from nonebot.params import ArgPlainText,CommandArg
from nonebot.adapters.onebot.v11 import Message,event
from nonebot.adapters import Event


import os,shutil,json,random,hashlib

def add_master(id: str):
    if os.path.exists("config/"):
        if os.path.exists("config/cfg.json"):
            logger.debug("发现配置文件")
        
    else:
        if os.path.exists("res/cfg.json"):
            shutil.copy("res/cfg.json", "config/cfg.json")
            logger.error("配置文件不存在，已创建默认配置文件")
        else:
            logger.error("配置文件不存在，请重新拉取bot")
            raise FileNotFoundError("配置文件不存在，请重新拉取bot")

    with open("config/cfg.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    if "superusers" in config:
        config["superusers"].append(id)
    else:
        config["superusers"] = [id]

    with open("config/cfg.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

    logger.info(f"已添加主人{id}")
    try:
        nb_config = get_driver().config
        nb_config.superusers = set(config["superusers"])
    except Exception as e:
        raise e
def out_code():
    code = ''
    for i in range(6):
        n = random.randint(0, 9)
        b = chr(random.randint(65, 90))
        s = chr(random.randint(97, 122))
        code += str(random.choice([n, b, s]))
    return hashlib.sha384(code.encode()).hexdigest()
    



    
    

add = on_command("增加主人", priority=1, permission=SUPERUSER,block=False)

@add.handle()
async def _(arg: Message = CommandArg()):
    if id:= arg.extract_plain_text():
        try:
            add_master(id)
        except Exception as e:
            await add.finish(f"设置主人时失败：{e}")
        else:
            await add.finish(f"已添加主人{id}")

@add.got("id", prompt="请输入要添加的主人的账号id")
async def _(id: str = ArgPlainText()):
    try:
        add_master(id)
    except Exception as e:
        await add.finish(f"设置主人时失败：{e}")
    else:
        await add.finish(f"已添加主人{id}")


async def is_not_master(event: Event):
    if event.get_user_id() not in get_driver().config.superusers:
        return True
    else:
        return False

set_master = on_command("设置主人", priority=1, permission=is_not_master,block=False)
@set_master.handle()
async def _():
    global code
    code = out_code()
    logger.opt(colors=True).warning(f"验证码：<blue>{code}</blue>")


@set_master.got("ans", prompt="请输入验证码")
async def _(event: Event, ans: str = ArgPlainText() ):
    id = event.get_user_id()

    global code
    if ans == code:
        await set_master.send("验证成功")
        try:
            add_master(id)
        except Exception as e:
            await set_master.finish(f"设置主人时失败：{e}")
        else:
            await set_master.finish(f"已添加主人{id}")

is_master = on_command("设置主人", priority=1, permission=SUPERUSER,block=False)
@is_master.handle()
async def _():
    await is_master.finish("你已经是主人了，无需设置")