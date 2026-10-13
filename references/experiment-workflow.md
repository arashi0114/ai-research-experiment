# M3 实验实现与验收

按已确认的实验契约实现数据读取、Dataset/DataLoader、转换和必要采样；数据划分须有版本或可复现生成规则，检查与任务相关的泄漏。预训练冻结模块同时处理 requires_grad_(False) 与 eval()，正确放置设备并记录权重版本；是否使用 no_grad()/inference_mode() 由算法是否需要穿过该模块的输入梯度决定。缓存特征时记录数据、预处理和编码器版本。

PyTorch 项目把训练/验证循环放在 trainer.py；Lightning 项目使用其原生机制，避免另写平行 Trainer。实现模型 forward、损失、优化器、验证、配置驱动入口、checkpoint 保存/恢复和日志。Evaluator 只实现契约中确认的 metrics，明确 batch 统计与全数据集聚合、边界条件、优化方向。验证集用于选择模型，测试集只用于最终评估。

每次正式运行创建唯一 run_id，在 runs/<run_id> 保存实际生效 config.yaml、metadata.json、checkpoint 和训练/验证/最终测试指标。metadata 至少包含运行状态、种子、可获取的代码版本、主要依赖版本、数据与划分版本、预训练权重标识；按需要补设备与精度。失败运行也保留状态和原因。优先 JSON/JSONL/CSV/YAML，不引入实验数据库。results/raw 保存关联 run_id、配置和指标名的结构化评估记录；summarize.py 只从真实记录计算分组、跨种子均值/标准差及可比 baseline 的结果，并按需导出 CSV/绘图。

验证顺序按适用性覆盖：导入、数据读取、shape、forward、loss、backward、最小训练步、验证、checkpoint 保存恢复、metric 单元检查、结果文件和端到端 smoke test。合成数据只用于工程验证并明确标记。只有数据到模型、配置训练与验证、checkpoint、约定 metrics、结构化结果以及最小端到端检查均通过，才能报告 Smoke Test Passed；真实实验和科研结论仍需分别验证。
