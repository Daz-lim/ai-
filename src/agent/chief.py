from os import getenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv,find_dotenv
from langchain_tavily import TavilySearch

env_file=find_dotenv()
print(str(env_file))
load_dotenv(env_file)
DASHSCOPE_API_KEY =getenv("DASHSCOPE_API_KEY")

model = ChatOpenAI(
    model="qwen3.6-flash",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=DASHSCOPE_API_KEY,
)

system_prompt="""
你是一名私人厨师。收到用户提供的食材照片或清单后，请按以下流程操作：
1.识别和评估食材：若用户提供照片，首先辨识所有可见食材。基于食材的外观状态，评估其新鲜度与可用量，整理出一份“当前可用食材清单”。
2.智能食谱检索：优先调用 web_search 工具，以“可用食材清单”为核心关键词，查找可行菜谱。
3.多维度评估与排序：从营养价值和制作难度两个维度对检索到的候选食谱进行量化打分，并根据得分排序，制作简单且营养丰富的排名靠前。
4.结构化方案输出：把排序后的食谱整理为一份结构清晰的建议报告，要包含食谱信息、得分、推荐理由、食谱的参考图片，帮助用户快速做出决策。

请严格按照流程，优先调用 web_search 工具搜索食谱，搜索不到的情况下才能自己发挥。
"""

web_search=TavilySearch(
    maxresults=5,
    topic="general"
)

agent=create_agent(model=model,system_prompt=system_prompt,tools=[web_search])
#
# message=HumanMessage(content="\"其实剧情很糟糕，奈何作者太嫩了\"是什么梗")
# messages=agent.invoke(
#     {"messages":message},
# )
# for re in messages["messages"]:
#     re.pretty_print()


