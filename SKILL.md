---
name: ai-research-experiment
description: 为 AI 科研项目创建脚手架、规划、实现或重构实验代码，并依据现有代码与真实结果撰写报告。适用于研究实验工程，不用于普通应用开发。
---

# AI Research Experiment

以科研协议正确为先，保持实现简单，并从设计阶段保证结果可追溯。默认 PyTorch；用户要求 Lightning，或它确实明显简化当前流程时才采用 Lightning。一个项目只保留一套训练流程。代码使用明确的英文标识符，注释和文档默认中文。不要为未知研究决定编造模型、数据、损失或指标；不要引入无需求的工厂、注册器、管理层或实验平台。

## 选择工作模式

- M1 空白项目：用户要求初始化、默认脚手架。读取 [项目结构](references/project-structure.md)，有 Python 3 时优先运行 scripts/init_project.py；没有时按模板手工创建等价项目，并检查占位符、语法和文件冲突。只生成可安装的结构和中文 TODO，不实现训练。
- M2 架构规划：用户给出具体研究任务并希望规划或扩展项目。读取 [规划流程](references/planning-workflow.md) 与 [项目结构](references/project-structure.md)。先给出最小模块增量和数据流，再创建需要的文件；未确定的模块保留 TODO。
- M3 实验闭环：用户要求数据、训练、评估、checkpoint、结果管理。先读取 [实验契约](references/experiment-contract.md)，形成具体契约；再读取 [实验实现流程](references/experiment-workflow.md) 与 [可复现性](references/reproducibility.md) 并实现和验证。
- M4 核心算法：用户要求实现论文方法、模型模块或损失。读取 [算法实现](references/algorithm-implementation.md)，先形成算法契约，再实现可检查的参考版本并集成。
- M5 实验设置报告：用户要求根据现有代码说明实验各环节。读取 [实验设置报告](references/setup-report.md)，追踪实际入口与配置，写出可从代码或运行记录确认的流程；不把未调用代码或计划写成已执行事实。
- M6 实验结果报告：用户提供实验数值、结果文件或日志并要求 Markdown 表格报告。读取 [实验结果报告](references/results-report.md)，先列出可追溯的真实结果；只对协议足够明确且可比的记录做统计或结论性比较。
- M7 现有代码重构：用户要求整理、拆分或简化已有实验代码。读取 [实验代码重构](references/refactoring.md) 与 [代码规范](references/coding-standards.md)，按请求范围识别需要保持的实验行为和接口，再重构及验证。

六个独立入口 Skill 与本 Skill 同包分发：`research-scaffold` 对应 M1，`research-outline` 对应 M2，`research-training` 对应以提问逐步完成 M3，`research-setup-report` 对应 M5，`research-results-report` 对应 M6，`research-refactor` 对应 M7。用户直接调用本 Skill 时，也按需求选择相同模式。

跨模式修改代码时读取 [代码规范](references/coding-standards.md)。多个模式并用时按实际依赖推进，复用已完成内容，不机械重做。用户指定模式时遵从其范围。现有项目先检查相关代码、配置和数据接口，再局部编辑；不要用模板盲目替换已有文件。未经用户要求，不删除或改写数据、权重、日志及原始结果。

## 对话与决策

先阅读用户提供的资料和现有项目，整理已确定信息、普通工程默认值、影响科研结论的待决协议以及暂不实现项。每轮只询问少量真正阻碍当前阶段的问题；能独立完成的部分继续推进。需要新决定或改变数据划分、比较协议、指标含义、算法等科研选择时，请用户确认，不用推测填空；只描述已有代码或结果时，标明证据与不确定性即可。开始前用简短计划说明目标、必要文件及验收条件；完成后报告实际验证及限制。可用 Plan Mode 时用于交互规划，否则正常对话即可。

## 验收状态

对代码任务，只报告有证据支持的最高状态：Scaffold Ready（结构可安装）；Implementation Ready（代码已实现）；Smoke Test Passed（适用的最小工程测试通过）；Experiment Executed（真实数据与正式配置已运行）；Research Result Validated（协议、指标和必要对比已核查）。合成数据测试只能支持工程验证，不能当作正式科研结果。报告任务不套用代码成熟度标签，而应说明证据范围；M3 缺少真实数据、权重或环境时，明确列出未验证部分。

维护本 Skill 或做行为前向测试时，使用 [功能场景](tests/forward_scenarios.md)；不要把场景说明视为已执行结果。
