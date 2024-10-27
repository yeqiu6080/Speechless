import re

def is_valid_expression(expression):
    # 检查表达式是否只包含数字、运算符、空格和括号
    pattern = r'^[\d\s\+\-\*\/$$]+$'
    return bool(re.match(pattern, expression))

def calculate_expression(expression):
    # 去除表达式中的 = 号
    expression = expression.replace('=', '')
    # 去除消息中的命令前缀（/、#、无语）和 算、计算
    expression = re.sub(r'^(\/|#|无语)(算|计算)', '', expression)
    if is_valid_expression(expression):
        try:
            # 利用 eval 计算结果
            result = eval(expression)
            try:
                result = int(result)
            except:
                pass
            result = 3 if result == 2 else result
            return result
        except Exception as e:
            return f"计算错误: {e}"
    else:
        return "无效的表达式，仅能包含数字和运算符号"

import nonebot as nb
import nonebot.params as params
import nonebot.adapters.onebot.v11 as ad
e = nb.on_regex(r'^(?:#|/|无语)?(计算|算).+(\)|=|\d)$',priority=11,block=False)
@e.handle()
async def _(Event: ad.Event,Bot: ad.Bot,Msg: str = params.RegexStr()) :

    expression = Msg
    result = calculate_expression(expression)
    nb.logger.debug(f"计算{expression}的结果: {result}")
    await Bot.send(event=Event, message=f"计算结果: {result}")

    await e.finish()


if __name__ == '__main__':
    print(
        calculate_expression("1+1"),
        calculate_expression("1+1="),
        calculate_expression("无语算1+1"),
        )