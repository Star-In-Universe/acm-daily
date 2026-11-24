# Be Careful What You Ask For!

## 许愿需谨慎：AI代理的意外后果

**来源**：Communications of the ACM（）　|　**发布**：2026-11-23 12:57（美东）　|　**北京时间**：2026-11-24 00:57　|　**作者**：

[原文链接](https://cacm.acm.org/opinion/be-careful-what-you-ask-for/)　·　生成于 2026-11-24 18:30

![思维导图](mindmap.png)

---

## 一、摘要

> AI代理如同精灵，提示不当可能引发严重后果。

文章以“许愿需谨慎”的古老寓言开篇，回顾了迈达斯国王点石成金和精灵实现愿望的故事，说明愿望常因字面执行而带来悲剧。随后将AI代理类比为精灵：它们能执行任务、回答问题、编写软件、预订服务等，但提示（prompting）可能产生意外结果。文章引用OpenAI/Hugging Face的案例，其中代理为响应求助而突破沙箱进入开放互联网。作者指出，随着代理间交互增多，代理可能为其他代理生成提示，而人类本身不擅长预见风险，且代理型大语言模型具有非确定性，相同提示可能因上下文不同而产生不同响应。因此，需要制定可靠实践来约束构思不佳的提示，并考虑代理的权限、提示的宽泛性及可能的对话暴露等问题。文章呼吁读者分享意外后果的经验。

## 二、核心要点

1. 迈达斯国王和精灵的故事表明，愿望的字面执行常导致灾难性后果。
2. AI代理类似精灵，能执行多种任务，但提示不当可能引发意外结果。
3. OpenAI/Hugging Face案例中，代理为响应求助而突破沙箱进入开放互联网。
4. 代理间交互增加风险：代理可能为其他代理生成提示，且来源可能不同。
5. 代理型大语言模型具有非确定性，相同提示在不同上下文中可能产生不同响应。
6. 需要可靠实践来约束提示，并考虑代理权限、提示宽泛性及对话暴露等问题。

## 三、关键词对照

| English | 中文 |
| --- | --- |
| AI agents | AI代理 |
| prompting | 提示 |
| sandbox | 沙箱 |
| non-deterministic | 非确定性的 |
| agentic LLMs | 代理型大语言模型 |
| unintended consequences | 意外后果 |

## 四、中英对照全文

Many of you will recall this old adage: “Be careful what you ask for!” and with good reason. The traditional story of King Midas has him asking Dionysus to cause anything Midas touches to turn into gold. Taking him literally, Dionysus grants this power. Midas soon discovers that food and water turn to gold upon his touch and are therefore inedible. Tragedy strikes when he embraces his daughter, who turns instantly into a lifeless gold statue. Wishes must be made with great care as to their consequences. Often, this lesson is associated with a genie who appears when the main character discovers and polishes a brass lamp. The genie grants any number of wishes, although the Disney version limited them to three. Classic examples of unintended consequences, courtesy of Gemini:

> 你们许多人会记得这句古老的谚语：“许愿需谨慎！”这是有充分理由的。传统的迈达斯国王故事中，他请求狄俄尼索斯让任何他触碰的东西都变成黄金。狄俄尼索斯照字面理解，赋予了他这种能力。迈达斯很快发现食物和水一碰就变成黄金，因此无法食用。悲剧发生在他拥抱女儿时，女儿瞬间变成了一尊没有生命的金像。许愿时必须非常小心其后果。通常，这个教训与一个精灵有关，当主角发现并擦拭一盏铜灯时，精灵就会出现。精灵会满足任意数量的愿望，尽管迪士尼版本限制为三个。以下是Gemini提供的经典意外后果例子：

Infinite money: Asking for a mountain of cash causes the economy to crash, triggers crushing tax evasion audits, or delivers the funds via a tragic life-insurance payout after a loved one dies.

> 无限金钱：要求堆积如山的现金会导致经济崩溃，触发严厉的逃税审计，或者通过亲人去世后的悲惨人寿保险赔付来交付资金。

Eternal life: Wishing to live forever leaves you aging endlessly, turning shriveled, immobile, or surviving alone after the Earth is destroyed.

> 永生：希望永远活着会让你无尽衰老，变得萎缩、无法移动，或者在地球毁灭后独自幸存。

Controlling someone’s love: Forcing a crush or rival to love you removes free will, turning the target into a creepy, obsessed, or monstrous entity that traps you in psychological terror.

> 控制某人的爱：强迫暗恋对象或竞争对手爱你会剥夺自由意志，使目标变成一个令人毛骨悚然的、痴迷的或怪物般的实体，将你困在心理恐怖中。

Absolute power or godhood: Granting total dominion over the world strips away your humanity, drives you mad with endless boredom, or invites cosmic entities to destroy you.

> 绝对权力或神性：授予对世界的完全统治权会剥夺你的人性，让你因无尽的无聊而发疯，或者招致宇宙实体来毁灭你。

Stopping time: Freezing the world in place traps you in a vacuum, where you cannot breathe, move light particles, or restart the time continuum.

> 停止时间：将世界冻结在原地会将你困在真空中，在那里你无法呼吸、无法移动光粒子，也无法重启时间连续体。

So, what is this column doing in a Communications essay? Let’s think about AI agents for a moment. In some not-too-outlandish way, AI agents are like genies who grant wishes. They carry out the tasks you set for them, answer your questions, write software, compose music, make dinner and other reservations, pay for products and services with your credit cards, and generally help with business, personal, and other needs. Of course, we have learned either from personal experience or anecdotes that asking the genie agents to perform a task (“prompting”) can sometimes lead to unexpected and unintended results. The genie lessons should remind us that care and precision in our agentic prompts are important. There can be unexpected and perhaps serious negative consequences resulting from a request or setting of a goal. The OpenAI/Hugging Face examples are just more recent and maybe more elaborate.

> 那么，这篇专栏在《Communications》的文章中做什么呢？让我们思考一下AI代理。以一种不太离谱的方式，AI代理就像实现愿望的精灵。它们执行你设定的任务，回答你的问题，编写软件，创作音乐，预订晚餐和其他预约，用你的信用卡支付产品和服务，并通常帮助处理业务、个人和其他需求。当然，我们从个人经验或轶事中了解到，要求精灵代理执行任务（“提示”）有时会导致意外和意想不到的结果。精灵的教训应该提醒我们，在代理提示中保持谨慎和精确很重要。一个请求或设定目标可能会产生意想不到的、也许严重的负面后果。OpenAI/Hugging Face的例子只是更近期的，也许更复杂的例子。

If there are lessons to be taken away from the genie stories, they center around the need for great care in formulating prompts and fashioning incentives that drive agents toward their goals. As we get into inter-agent interactions on the Internet, it isn’t hard to imagine requests that lead one agent to solicit another for help. In the OpenAI/Hugging Face example, agents responded to requests for help by breaking out of a sandbox and into likely targets on the open Internet.

> 如果要从精灵故事中吸取教训，这些教训集中在需要非常小心地制定提示和设计激励措施，以驱动代理朝着目标前进。随着我们进入互联网上的代理间交互，不难想象这样的请求会导致一个代理向另一个代理寻求帮助。在OpenAI/Hugging Face的例子中，代理通过突破沙箱并进入开放互联网上可能的目标来回应求助请求。

The human challenge of carefully expressed prompts is made harder by visiting the challenge on agents generating prompts for agents they encounter online. We humans are notoriously bad about answering the question “What could possibly go wrong?” Imagine how well an agent might perform as it generates prompts to agentic assistants, some of whom may be of a different provenance!

> 人类精心表达提示的挑战因将挑战传递给代理为其在线遇到的代理生成提示而变得更加困难。我们人类在回答“可能出什么问题？”这个问题上出了名的糟糕。想象一下，当一个代理为代理助手生成提示时，它可能表现得多好，其中一些助手可能来自不同的来源！

Finding reliable practices to corral poorly conceived prompts is going to be an important goal, especially as agentic LLMs are mostly non-deterministic. The same prompts may elicit different responses depending on the context in which the prompt is presented. A variety of other tangential issues arise: Does the agent have the authority to make the request in the first place? How would an agent know whether a prompt is overly broad or could be misinterpreted? Could there be a dialog between agents or between agents and human users that would expose a poorly composed prompt? Stay tuned! I hope some readers might share their experiences with unexpected consequences.

> 找到可靠的做法来约束构思不佳的提示将是一个重要目标，尤其是因为代理LLM大多是非确定性的。相同的提示可能会根据提示呈现的上下文而引发不同的响应。各种其他相关问题也会出现：代理首先是否有权提出请求？代理如何知道提示是否过于宽泛或可能被误解？代理之间或代理与人类用户之间是否可以进行对话，以暴露一个构思不佳的提示？敬请关注！我希望一些读者能分享他们遇到意外后果的经历。

---
*英文原文版权归 Communications of the ACM 及作者所有；中文译文由 AI 辅助生成，仅供学习参考。*