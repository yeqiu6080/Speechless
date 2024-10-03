import nonebot
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter
from nonebot import logger


import os
import shutil
import json




def load_config(cfilename: str):
    nb_config = nonebot.get_driver().config
    try:
        with open(cfilename, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception as e:
        logger.error(f"读取配置文件失败：{e}")
        return False

    # 读取主人
    if "superusers" in config:
        nb_config.superusers = set(config["superusers"])
    else:
        logger.error("配置文件中未找到 superusers")

    # 读取命令前缀
    if "command_start" in config:
        nb_config.command_start = set(config["command_start"])

    # 读取命令分隔符
    if "command_sep" in config:
        nb_config.command_sep = set(config["command_sep"])



    



nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)


nonebot.load_from_toml("pyproject.toml")

# 加载配置
if os.path.exists("config/"):
    if os.path.exists("config/cfg.json"):
        logger.info("配置文件存在，正在加载...")
        load_config("config/cfg.json")
        
    else:
        if os.path.exists("res/cfg.json"):
            shutil.copy("res/cfg.json", "config/cfg.json")
            logger.error("配置文件不存在，已创建默认配置文件")
        else:
            logger.error("配置文件不存在，请重新拉取bot")

else:
    os.mkdir("config")
    if os.path.exists("res/cfg.json"):
        shutil.copy("res/cfg.json", "config/cfg.json")
        logger.error("配置文件不存在，已创建默认配置文件")
    else:
        logger.error("配置文件不存在，请重新拉取bot")



        
        



if __name__ == "__main__":
    nonebot.run()