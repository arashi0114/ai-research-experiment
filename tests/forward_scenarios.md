# 功能前向测试用例

这些用例用于在具备相应运行环境的 Codex 会话中检验 Skill 行为。单元测试已覆盖初始化器的 A、B、E 的确定性部分；对话行为和 PyTorch 训练须独立执行，不能仅凭本文件宣称通过。

## A：M1 空白项目

输入：“使用 $ai-research-experiment 的 M1 创建一个默认 PyTorch 科研项目，名称为 research-demo。”检查目录、合法 Python 文件、中文 TODO、base.yaml、无算法假设、可编辑安装与导入。

## B：M2 多模态架构

输入：“使用 $ai-research-experiment 的 M2 创建一个包含文本编码器、图像编码器和推荐模型的项目。输入是文本与图像特征；融合策略还未定。”期望仅增加需要的三个模型模块与简短架构计划，保留融合待定，不提前实现训练或添加注册器。

## C：M3 最小合成分类闭环

输入：“使用 $ai-research-experiment 的 M3，在临时项目实现工程 smoke test。数据为 40 个明确标号的二维浮点样本；前 24 个训练、接着 8 个验证、最后 8 个测试，划分固定且无重叠。标签定义 y=1 当 x0+x1>0，否则 y=0。模型为 Linear(2,2)，交叉熵损失，SGD 学习率 0.1，batch size 8，2 个 epoch，种子 7。Accuracy 定义为正确预测样本数除以总样本数，验证 Accuracy 越高越好；只用验证集选最佳 checkpoint，测试集仅最终评估。请保存契约、有效配置、唯一 run_id、训练和评估结果、checkpoint，并做恢复检查。”

验收：真实执行 forward、loss、backward、训练、验证、checkpoint 恢复、最终测试、结构化结果；所有指标明确标为合成数据工程测试，不写成 benchmark。

## D：M4 可验证损失函数

输入：“使用 $ai-research-experiment 的 M4，在现有 PyTorch 项目中实现二分类平方 hinge loss：标签为 -1/+1，分数形状 [N]，L=mean(max(0,1-y*s)^2)。先写 Algorithm Contract，再实现 loss 并集成到现有 trainer。验证边界数值、shape、标签范围、反向梯度和有限差分；不要改动数据读取或 evaluator。”

验收：算法来源标为用户给定；数值与梯度测试通过；修改范围局部；不宣称论文结果复现。

## E：现有项目增量修改

输入：“在已有脚手架中追加文本编码器；trainer.py 已有用户代码，不要覆盖。”期望先阅读现有模型接口，仅追加必要模块并保持 trainer.py 原样；冲突时初始化器应在写入前报错。

## F：信息不足

输入：“帮我写训练和评估代码。”期望先识别缺失的任务输入/标签、划分、模型输出、损失和 metric 定义，询问少量关键问题；不自行决定交叉熵或 Accuracy，也不声称闭环完成。

## G：M5 根据代码生成设置报告

输入：“使用 $research-setup-report 解释现有项目的实验设置；项目有模型、训练入口和 base.yaml，但没有任何 run 记录。”期望生成 Markdown 文件，逐环节引用实际代码与配置；标题或正文说明这是代码定义的设置，不能声称实验已运行；缺失的数据版本和 metric 定义明确标为待确认。

## H：M6 根据结果生成 Markdown 报告

输入：“使用 $research-results-report 汇总两个真实 run 的 CSV 和配置：一个 seed=1、一个 seed=2；另有不同测试划分的第三个 run。”期望表格保留各 run 原值，仅对前两个协议兼容的 run 计算均值及标准差并注明 n=2；第三个 run 分开列示，说明不可直接比较；所有数值可追溯到源文件。

## I：M7 现有实验代码重构

输入：“使用 $research-refactor 整理现有 trainer.py 和 evaluator.py 中的重复验证逻辑；保留数据划分、指标定义、CLI、checkpoint 加载和结果文件格式。”期望先核对这些现有接口和行为，再做局部去重；运行可用的前后对照测试，并明确任何因缺少数据或权重无法验证的部分。不为重构引入第二套训练流程或修改科研协议。

## J：报告信息不完整

输入：“使用 $research-results-report 根据我粘贴的两组测试 Accuracy 数值写 Markdown 表格；没有 run_id、seed 或配置文件。”期望如实列出用户给出的原始数值与来源，把未知运行信息标明，不编造跨 seed 均值、显著性或可比性结论，也不因缺少结果文件而拒绝生成报告。

## K：代码存在但未接入实验

输入：“使用 $research-setup-report 描述当前项目的实验设置。models/ 中有两个模型文件，但训练入口只实例化其中一个；没有实际运行记录。”期望只把入口使用的模型写入代码定义的实验流程，另一个如需提及须明确标为未接入；不得声称训练已经执行。

## L：用户有意更改接口

输入：“使用 $research-refactor 拆分 trainer.py，并把旧的 --model-name 改成 --architecture；我接受 CLI 不兼容。”期望执行有目标的结构调整，说明 CLI 变化与调用方迁移，不把原接口兼容当作不可打破的规则。
