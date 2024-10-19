import nonebot
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter
from nonebot import logger


import os
import shutil
import json
import re




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
    
    # 读取自定义外显
    if "word_image_name" in config:
        nb_config.word_image_name = config["word_image_name"]
    else:
        nb_config.word_image_name = "Jerry来了！"




    



nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)








# 加载配置
if os.path.exists("data/config/"):
    if os.path.exists("data/config/cfg.json"):
        logger.info("配置文件存在，正在加载...")
        load_config("data/config/cfg.json")
        
    else:
        if os.path.exists("core/res/cfg.json"):
            shutil.copy("core/res/cfg.json", "data/config/cfg.json")
            logger.error("配置文件不存在，已创建默认配置文件")
        else:
            logger.error("配置文件不存在，请重新拉取bot")

else:
    os.mkdir("data/config/")

    if os.path.exists("core/res/cfg.json"):
        shutil.copy("core/res/cfg.json", "data/config/cfg.json")
        logger.error("配置文件不存在，已创建默认配置文件")
    else:
        logger.error("配置文件不存在，请重新拉取bot")


# 词库图片外显
if os.path.exists("data/word_bank/bank.json"):
    with open("data/word_bank/bank.json", "r", encoding="utf-8") as f:
        bank = json.load(f)
        logger.info(f"词库{bank}")

    nb_config = nonebot.get_driver().config
    for lev in bank:
        for fw in bank[lev]:
            try:
                for key in bank[lev][fw]:
                    try:
                        listt = []
                        for value in bank[lev][fw][key]:
                            
                            logger.debug(f"修改词库图片外显前：{value}")

                            i = re.sub(r',summary=(.*?),', f',summary={nb_config.word_image_name},', value)
                            listt.append(i)
                            logger.debug(f"修改词库图片外显后：{i}")
                        bank[lev][fw][key] = listt

                    except Exception as e:
                        logger.debug(f"修改词库图片外显失败：{e}")
            except Exception as e:
                    logger.debug(f"修改词库图片外显失败：{e}")

    with open("data/word_bank/bank.json", "w", encoding="utf-8") as f:
        json.dump(bank, f, indent=4, ensure_ascii=False)
    logger.info("词库图片外显修改成功")

    
        
    
    

        
        



if __name__ == "__main__":
    nonebot.load_from_toml("pyproject.toml")
    nonebot.run()