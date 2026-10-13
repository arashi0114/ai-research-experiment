# {{PROJECT_NAME}}

本项目是空白科研实验脚手架。Python 模块中的 TODO 待实验协议确定后实现；当前不能执行训练或评估。

## 安装

    pip install -e .

## 目录

- configs：正式实验配置；base.yaml 目前只含项目标识。
- data/raw：原始数据，默认只读；data/interim 与 data/processed：派生数据；data/manifests：真实数据来源、版本和划分记录。
- weights/pretrained：外部预训练权重，与 runs 中训练 checkpoint 分离。
- src/{{PACKAGE_NAME}}：可复用的数据、模型、训练、评估和 checkpoint 代码。
- scripts：预处理、特征提取、训练、评估和汇总的薄入口。
- runs：每次实验的配置、元数据、指标和 checkpoint；logs：非运行专属调试日志。
- results/raw、results/tables、results/figures：逐次结果、汇总表格和图。
- docs：实验契约与架构说明；tests：算法正确性与工程检查。

请先确定实验契约，再实现具体任务。不要把合成数据测试写作正式科研结果。
