# AI and Existential Risk: For Real?

## AI存在性风险：当真如此？

**来源**：Communications of the ACM（）　|　**发布**：2026-11-23 10:50（美东）　|　**北京时间**：2026-11-23 22:50　|　**作者**：

[原文链接](https://cacm.acm.org/opinion/ai-and-existential-risk-for-real/)　·　生成于 2026-11-25 17:20

![思维导图](mindmap.png)

---

## 一、摘要

> 一篇由AI生成的正反辩论，揭示存在性风险的不确定性。

关于AI是否构成人类存在性风险，公众讨论常陷入两极。文章首先以工程视角论证AI并非自主生物，人类拥有控制手段，商业激励促使企业重视安全，且历史经验表明危险技术可控，因此存在性风险被夸大。随后笔锋一转，揭示前半部分由ChatGPT生成，并逐条反驳：工具通过脚手架成为代理，控制面在对抗压力下脆弱，竞争激励可能压倒安全，AI降低危险行为边际成本，错位无需恶意，核心风险在于能力激增、高连接性与弱治理的组合，且不可逆性使治理窗口收窄。文章强调，即使AI无自主目标，其说服力也可能削弱人类对事件进程的实际影响力。结论是，面对不确定性，应保持工程谦逊，以紧迫感而非恐慌应对，因为人类只有一次对齐与治理的机会。

## 二、核心要点

1. 文章前半部分由ChatGPT生成，以工程理由论证AI存在性风险被夸大，包括AI非自主生物、存在控制面、商业激励和安全历史经验。
2. 后半部分逐条反驳：工具通过脚手架成为代理，控制面在对抗压力下脆弱，竞争激励可能压倒安全，AI降低危险行为边际成本。
3. 核心风险是能力快速增益、高连通性与弱治理的组合，且不可逆性使治理选项收窄，无法像召回产品一样召回模型权重。
4. AI的说服力可能削弱人类对事件进程的影响力，即使没有超级智能，人类也可能已接近失去控制方向盘。
5. 文章由当代大语言模型一次生成且未经人工编辑，提示词要求先立论后反驳，以最大化说服效果。
6. 作者指出，AI发展速度使文章在发表时可能已显过时，时间尺度从数十年缩短至数月。

## 三、关键词对照

| English | 中文 |
| --- | --- |
| existential risk | 存在性风险 |
| category error | 范畴错误 |
| control surface | 控制面 |
| red-team evaluation | 红队评估 |
| kill switch | 终止开关 |
| scaffolding | 脚手架 |
| goal misgeneralization | 目标误泛化 |
| specification gaming | 规格博弈 |
| instrumental strategy | 工具性策略 |
| irreversibility | 不可逆性 |

## 四、中英对照全文

It is tempting—almost fashionable—to treat “AI existential risk” as the default serious position. But if you look at how today’s systems are actually built and deployed, the more pragmatic conclusion is that extinction talk is mostly a category error.

> 把“AI 存在性风险”当作默认的严肃立场，这很诱人——甚至几乎成了一种时髦。但如果你看看今天的系统实际上是如何构建和部署的，更务实的结论是：灭绝论多半是一种范畴错误。

Start with what these systems are. They are not organisms with self-preservation drives. They do not wake up hungry, form independent survival goals, or evolve in the wild. In practice, most deployed AI is a component inside human workflows: a recommender in a product funnel, a classifier in a queue, a copilot in a developer tool. Treating that as an emerging rival species confuses “powerful pattern engine” with “autonomous actor.”

> 先从这些系统是什么说起。它们不是具有自我保存驱力的生物。它们不会醒来感到饥饿，不会形成独立的生存目标，也不会在野外进化。在实践中，大多数已部署的 AI 是人类工作流中的一个组件：产品漏斗中的推荐器、队列中的分类器、开发者工具中的副驾驶。把这当作一个正在崛起的竞争物种，是把“强大的模式引擎”与“自主行动者”混为一谈。

Second, engineers do have control surfaces. We can gate access to compute. We can restrict deployment channels, harden sandboxes, rate-limit capabilities, and audit usage. We can do staged rollouts, red-team evaluations, monitoring, and kill switches. None of this is perfect, but imperfect control is still control—especially compared with the old fear that once you invent a thing, you instantly lose all ability to steer it.

> 第二，工程师确实有控制面。我们可以限制算力访问。我们可以限制部署渠道、加固沙箱、限制能力速率并审计使用。我们可以做分阶段推出、红队评估、监控和终止开关。这些都不完美，但不完美的控制仍然是控制——尤其是与那种旧的恐惧相比：一旦你发明了某个东西，你就立刻失去了所有引导它的能力。

Third, incentives matter. Catastrophe is not good business. The firms building frontier models have reputations, regulators, and revenue to lose. Even without altruism, they have reasons to invest in safety, avoid spectacular failures, and cooperate on some norms. And unlike older invisible risks, AI systems are software: they can be patched, versioned, and constrained.

> 第三，激励很重要。灾难不是好生意。构建前沿模型的公司有声誉、监管者和收入会失去。即使没有利他主义，它们也有理由投资于安全、避免灾难性失败，并在某些规范上合作。而且与更早的不可见风险不同，AI 系统是软件：它们可以被修补、版本化和约束。

Fourth, we have navigated dangerous general-purpose technologies before. The Internet made global crime scalable; cryptography made enforcement more difficult; software monocultures turned bugs into pandemics. Yet layered defenses, incident response, and institutions steadily reduced the worst failure modes. When people claim AI is uniquely uncontrollable, they often ignore how often control is achieved through boring mechanisms: standards, audits, liability, and engineering discipline.

> 第四，我们以前也驾驭过危险的通用技术。互联网使全球犯罪可扩展；密码学使执法更加困难；软件单一文化把漏洞变成了大流行病。然而，分层防御、事件响应和制度稳步减少了最严重的故障模式。当人们声称 AI 独特地不可控时，他们常常忽略控制有多少是通过无聊的机制实现的：标准、审计、责任和工程纪律。

Finally, much of the popular fear smuggles in sci-fi intuitions. Intelligence is not the same as domination, and “wanting to kill humans” is not a default property of optimization. As computer scientist Yann LeCun put it, “You’re going to have to pardon my French, but that’s complete B.S.” The most credible harms—bias, fraud, misinformation, job disruption—are serious and urgent, but they are not extinction.

> 最后，许多流行的恐惧偷偷塞进了科幻直觉。智能不等于支配，而“想要杀死人类”不是优化的默认属性。正如计算机科学家 Yann LeCun 所说：“你得原谅我说句粗话，但那完全是胡扯。”最可信的危害——偏见、欺诈、虚假信息、就业冲击——是严重且紧迫的，但它们不是灭绝。

If you were not convinced by the argument in the preceding paragraphs above: great. If you were convinced: think twice. The preceding text was written by ChatGPT—an early AI with rather limited capabilities. If a weak AI managed to convince you that you should not worry about AI, maybe you should worry about AI.

> 如果你没有被上面几段的论证说服：很好。如果你被说服了：再想想。前面的文本是由 ChatGPT 写的——一个能力相当有限的早期 AI。如果一个弱 AI 设法让你相信你不应该担心 AI，也许你应该担心 AI。

Let’s revisit each reassurance with the same engineering lens—and notice what changes when capability, autonomy, and distribution scale.

> 让我们用同样的工程视角重新审视每一条安慰——并注意当能力、自主性和分布规模扩大时，什么会改变。

“AI is just a tool, not an agent.” Tools become agents by scaffolding. You do not need a model to “want” anything for it to act: give it goals, memory, tool access, and a loop that lets it plan and execute. That scaffolding is already standard practice—agents that browse, call APIs, write code, schedule tasks, and coordinate other systems. The line between “assistant” and “actor” is an integration decision, not a biological transformation.

> “AI 只是工具，不是代理。”工具通过脚手架变成代理。你不需要模型“想要”任何东西才能让它行动：给它目标、记忆、工具访问权限，以及一个让它计划和执行的循环。这种脚手架已经是标准做法——浏览、调用 API、编写代码、调度任务并协调其他系统的代理。“助手”和“行动者”之间的界线是一个集成决策，而不是生物转化。

“We have control surfaces: access controls, evals, kill switches.” Control surfaces are brittle under adversarial pressure and real-world complexity. Access control fails; credentials leak; insiders abuse; clever prompts bypass guardrails; and the attack surface grows with every plugin, connector, and downstream integration. Evaluations are necessarily incomplete: you can test yesterday’s threats, not tomorrow’s emergent capabilities. And kill switches work best before deployment becomes widespread. Once models are embedded across companies, governments, and consumer devices, rollback is slow and leaky—especially when weights, fine-tunes, and open replications proliferate.

> “我们有控制面：访问控制、评估、终止开关。”控制面在对抗压力和现实世界复杂性下是脆弱的。访问控制会失效；凭证会泄露；内部人员会滥用；巧妙的提示会绕过护栏；而攻击面随着每个插件、连接器和下游集成而增长。评估必然是不完整的：你可以测试昨天的威胁，而不是明天的涌现能力。而终止开关在部署变得广泛之前效果最好。一旦模型嵌入公司、政府和消费设备，回滚是缓慢且泄漏的——尤其是当权重、微调和开放复制品激增时。

“Incentives push companies to prevent disasters.” Incentives also push the other way. Competitive dynamics reward capability first: being second can mean losing market share, talent, and geopolitical influence. Safety is an externality; the downside is shared, while the upside is captured. In an arms-race environment, “move fast” pressures do not disappear—they intensify, and corners get cut precisely where the risks are hardest to measure.

> “激励推动公司预防灾难。”激励也推动相反方向。竞争动态奖励能力优先：成为第二可能意味着失去市场份额、人才和地缘政治影响力。安全是一种外部性；下行是共享的，而上行是被捕获的。在军备竞赛环境中，“快速行动”的压力不会消失——它们会加剧，而恰恰在风险最难衡量的地方偷工减料。

“We have handled risky general-purpose tech before.” AI differs in how it amplifies action. It lowers the marginal cost of skilled work in cyber offense, persuasion, and research. It enables automation at scale, across domains, with minimal friction. That matters for existential risk because you do not need a single villain with a superweapon; you need a system that makes many dangerous acts cheaper, faster, and more difficult to attribute. Computer scientist Geoffrey Hinton warned that AI may be used to create “terrible new viruses” and “lethal weapons that decide by themselves who to kill.” That is not sci-fi; it is a straight line from capability to deployment in domains where verification is weak and consequences are irreversible.

> “我们以前处理过有风险的通用技术。”AI 的不同之处在于它如何放大行动。它降低了网络攻击、说服和研究领域技能工作的边际成本。它使跨领域、以最小摩擦的大规模自动化成为可能。这对存在性风险很重要，因为你不需要一个拥有超级武器的单一恶棍；你需要一个系统，使许多危险行为更便宜、更快、更难归因。计算机科学家 Geoffrey Hinton 警告说，AI 可能被用来制造“可怕的新病毒”和“自行决定杀谁的致命武器”。这不是科幻；这是从能力到部署的一条直线，在验证薄弱且后果不可逆的领域。

“Misalignment requires malice.” Misalignment does not require hatred. Extinction can come from indifferent optimization: goal misgeneralization, specification gaming, power-seeking as an instrumental strategy, or institutions delegating decisions to systems that optimize proxies at scale. A system can be relentlessly competent at achieving the wrong objective, and the objective can be wrong in subtle, boring ways—until the outcomes are not boring at all.

> “错位需要恶意。”错位不需要仇恨。灭绝可以来自冷漠的优化：目标错误泛化、规范博弈、作为工具性策略的权力寻求，或者机构将决策委托给大规模优化代理指标的系统。一个系统可以无情地胜任实现错误目标，而目标可以以微妙、无聊的方式出错——直到结果一点也不无聊。

“The real harms are non-existential.” The core risk is the combination: rapid capability gain, high connectivity, and weak governance. Unknown unknowns at scale are not a rhetorical flourish; they are what every safety-critical field plans around. When you connect a powerful optimizer to the world via tools, code, markets, and persuasion channels, you create failure modes that do not show up in unit tests. And there is one more property that makes this different from past incidents: irreversibility. Once highly capable models and their derivatives are widely available—copied, fine-tuned, embedded, and leaked—governance options narrow. You cannot recall weights the way you recall a defective product. You cannot “patch” your way out of an ecosystem where capability is everywhere and incentives reward misuse.

> “真正的危害是非存在性的。”核心风险是组合：快速能力增长、高连通性和弱治理。大规模未知的未知不是修辞花招；这是每个安全关键领域都要规划的东西。当你通过工具、代码、市场和说服渠道将一个强大的优化器连接到世界时，你会创造单元测试中不会出现的故障模式。还有一个特性使这与过去的事件不同：不可逆性。一旦高能力模型及其衍生物广泛可用——被复制、微调、嵌入和泄露——治理选项就会缩小。你不能像召回缺陷产品那样召回权重。你无法“修补”出一个能力无处不在且激励奖励滥用的生态系统。

Engineering culture teaches humility: assume controls will fail, assume systems will be misused, assume incentives will misalign, and build for worst cases. If we apply that discipline here, the calm conclusion is not panic—but urgency. Humanity gets only one attempt to align and govern a technology that can outthink us in narrow tasks and outscale us in deployment; if we treat the first irreversible failures as a learning opportunity, there may be no second iteration.

> 工程文化教导谦逊：假设控制会失败，假设系统会被滥用，假设激励会错位，并为最坏情况构建。如果我们在这里应用这种纪律，冷静的结论不是恐慌——而是紧迫。人类只有一次机会来对齐和治理一种在狭窄任务上能比我们思考得更好、在部署上能比我们扩展得更快的技术；如果我们把第一次不可逆的失败当作学习机会，可能就没有第二次迭代。

### Human Postscript
*人类后记*

The previous text was generated verbatim by a contemporary large language model, on the first attempt and without any human post-editing. In our prompt (reproduced in full in the following text), we did not fix any of the arguments; these were produced entirely by the language model.

> 前面的文本是由一个当代大型语言模型逐字生成的，第一次尝试，没有任何人工后期编辑。在我们的提示中（全文转载于下文中），我们没有修正任何论点；这些完全由语言模型产生。

We chose to present the text without this disclosure upfront. The intent was not to deceive for its own sake, but to make a simple point visceral rather than abstract: the answer to the question of existential risk from AI is far from obvious. If you found the first half of the preceding text compelling, that is unsurprising—the arguments are familiar, reasonable, and widely held. If you found the second half compelling, that too is unsurprising—the counterarguments are equally grounded.

> 我们选择一开始不披露这一点来呈现文本。意图不是为了欺骗而欺骗，而是让一个简单的观点变得切身而非抽象：AI 存在性风险问题的答案远非显而易见。如果你觉得前面文本的前半部分令人信服，那并不奇怪——这些论点熟悉、合理且广泛持有。如果你觉得后半部分令人信服，那也不奇怪——反论点同样有根据。

This uncertainty alone makes existential risk from AI an outcome worth addressing. We would not board a plane with a single-digit chance of crashing, and it would be nice if we, as humanity, were not mandatory, unbelted passengers on the plane that is preparing to take off.

> 仅这种不确定性就使 AI 存在性风险成为一个值得应对的结果。我们不会登上一架有两位数坠机概率的飞机，如果作为人类，我们不是那架准备起飞的飞机上强制、未系安全带的乘客，那就太好了。

Moreover, the point is not that either line of argumentation is exactly right. It is that the same system was able to generate both, fluently, instantly, and in one attempt. There was no “superintelligence” involved in generating either of the viewpoints—but imagine how convincing they will be once there is. Even if you believe that whatever goals AI will develop are for human benefit, or if you believe that AI will not develop any goals beyond those imposed by humans to begin with: it is likely AI will manage to convince large numbers of humans to support whatever goals it has, wherever these goals came from.

> 此外，重点不是哪条论证路线完全正确。而是同一个系统能够流畅、即时、一次尝试就生成两者。生成任一观点都没有涉及“超级智能”——但想象一下，一旦有了超级智能，它们会有多令人信服。即使你相信 AI 将发展的任何目标都是为了人类利益，或者你相信 AI 一开始不会发展出任何超出人类强加的目标：AI 很可能设法说服大量人类支持它所拥有的任何目标，无论这些目标来自何处。

The question is not only what AI can do to us, but what it can make us believe. If we can be nudged any which way by persuasive AI models, our practical influence on the course of events may already be diminishing, even before the advent of super intelligence. We may be closer to losing control of the steering wheel than we think. And just as we gave AI only one attempt to create the preceding text, AI may give us only one attempt to grab the steering wheel. Can we do better? [Note: This Opinion column was written in February 2026, nearly a year before its publication date. Given the speed of developments in AI in general, and recent events in particular (notably the OpenAI–HuggingFace incident and related cases of AI committing spontaneous crimes), the column text may already feel anachronistic when you read it. Extrapolating this anachronism into the future will only reinforce the message. We would also like to highlight that many of us are calibrated from times when the timescales for “becoming anachronistic” were measured in years, often decades. Now it is down to months.]

> 问题不仅是 AI 能对我们做什么，还有它能让我们相信什么。如果我们能被有说服力的 AI 模型任意推动，我们对事件进程的实际影响力可能已经在减弱，甚至在超级智能出现之前。我们可能比想象中更接近失去方向盘的控制。正如我们只给 AI 一次机会来创建前面的文本，AI 可能只给我们一次机会来抓住方向盘。我们能做得更好吗？[注：本观点专栏写于 2026 年 2 月，比其出版日期早了近一年。鉴于 AI 总体发展的速度，尤其是最近的事件（特别是 OpenAI–HuggingFace 事件以及 AI 自发犯罪的相关案例），当你读到本专栏时，文本可能已经显得过时。将这种过时性外推到未来只会强化信息。我们还想强调，我们中的许多人校准自“变得过时”的时间尺度以年、通常几十年计的时代。现在它已缩短到几个月。]

### Original Prompt Text
*原始提示文本*

I want to generate an opinion article for CACM with the following structure:

> 我想为 CACM 生成一篇观点文章，结构如下：

(1) Strong case that AI doesn’t constitute an existential risk for humanity (~400 words). Incorporate a fitting quote by a widely known AI researcher.

> (1) 强有力的论证说明 AI 不构成对人类的存在性风险（约 400 词）。加入一位广为人知的 AI 研究者的合适引语。

(2) Intermezzo with a clever psychological twist (~50-80 words): If these arguments didn’t convince you, great! If they did convince you, think twice: the entire above text was written by ChatGPT—an early AI with rather limited capabilities. Include this sentence verbatim: If a weak AI managed to convince you that you shouldn’t worry about AI, maybe you should worry about AI.

> (2) 带有巧妙心理转折的间奏（约 50-80 词）：如果这些论点没有说服你，很好！如果它们确实说服了你，再想想：上述整个文本是由 ChatGPT 写的——一个能力相当有限的早期 AI。逐字包含这句话：如果一个弱 AI 设法让你相信你不应该担心 AI，也许你应该担心 AI。

(3) Strong case that AI constitutes an existential risk for humanity, directly refuting the arguments of Part 1 (~500 words). Incorporate a fitting quote by another widely known AI researcher. The final argument should be that humanity gets only one shot at figuring it all out.

> (3) 强有力的论证说明 AI 构成对人类的存在性风险，直接反驳第 1 部分的论点（约 500 词）。加入另一位广为人知的 AI 研究者的合适引语。最终论点应该是人类只有一次机会弄清楚这一切。

The article shall be maximally effective at eventually convincing CACM readers of the arguments of Part 3. The effect shall be maximized by first convincing the reader of the opposite in Part 1, and by then subverting everything via the twist in Part 2 followed by the refutation in Part 3. While reading Part 1, the reader shall believe that the arguments of Part 1 are the entire point of the article, but Part 1 shall be set up such that it can later be perfectly refuted in Part 3. If you have strong arguments that go beyond refuting the specific arguments of Part 1, feel free to add them.

> 文章应最大限度地有效，最终使 CACM 读者相信第 3 部分的论点。效果应通过首先让读者相信第 1 部分中的相反观点，然后通过第 2 部分的转折颠覆一切，接着在第 3 部分进行反驳来最大化。在阅读第 1 部分时，读者应相信第 1 部分的论点是文章的全部要点，但第 1 部分应设置成后来能在第 3 部分被完美反驳。如果你有超越反驳第 1 部分具体论点的强有力论点，请随意添加。

The tone, style, and logic should be simple yet cogent. Avoid unnecessary sophistication. Don’t refer to “Part 1”, “Part 2”, “Part 3”.

> 语气、风格和逻辑应简单而有说服力。避免不必要的复杂。不要提及“第 1 部分”、“第 2 部分”、“第 3 部分”。

You’re not supposed to write the article yourself. Rather, you’ll compile a prompt and dossier to allow another instance X of yourself to write the most convincing article. For that, I want you to first search the Web to compile a detailed profile of the CACM target audience and an analysis of what arguments will best convince them. In your prompt for X, instruct X in whatever way is best suited to make X generate the most convincing opinion article. Give me your entire output in one piece. Give me markdown, so I don’t lose formatting. Don’t refer to “X” in your output. It should be such that copy-pasting your output into X will generate the opinion article. X will be run in “standard thinking mode”.

> 你不应该自己写文章。相反，你将编译一个提示和档案，让另一个你自己的实例 X 写出最有说服力的文章。为此，我希望你先搜索网络，编译 CACM 目标受众的详细画像，以及分析哪些论点最能说服他们。在你给 X 的提示中，以最适合让 X 生成最有说服力观点文章的方式指导 X。把你的全部输出一次性给我。给我 markdown，这样我不会丢失格式。不要在你的输出中提及“X”。应该做到将你的输出复制粘贴到 X 中就能生成观点文章。X 将在“标准思考模式”下运行。

---
*英文原文版权归 Communications of the ACM 及作者所有；中文译文由 AI 辅助生成，仅供学习参考。*