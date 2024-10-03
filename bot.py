import nonebot
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter
from nonebot import logger


import os
import shutil

def load_config(cfilename: str):
    pass


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