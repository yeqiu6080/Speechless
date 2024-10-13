from nonebot import on_command
from nonebot.adapters.onebot.v11 import event,bot


sl = on_command("点赞",priority=1,block=False,aliases={"赞我"})

@sl.handle()
async def _(bot:bot.Bot,event:event.Event):
    user_id = event.get_user_id()
    for i in range(20):
        await bot.send_like(user_id=user_id,times=1)
    await sl.finish("给你赞了几下哦，记得回我~ (如赞失败请添加好友)")