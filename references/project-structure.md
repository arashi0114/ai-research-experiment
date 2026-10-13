# 项目结构与 M1

默认项目采用标准 src-layout。只在用户任务确实需要时增添模块，不把模板当作现有项目的强制目标。初始化命令：

    python3 scripts/init_project.py --project-name my-research --path /absolute/path/my-research

名称应给出合法的 ASCII Python 包名；脚本可从英文项目名推导，也可用 --package-name 显式指定。--path 指项目根目录。已有同内容文件会跳过；任何同名文件内容不一致时，脚本先报错且不写入。目标机没有 Python 3 时，Codex 可依 `assets/project-template/` 手工生成同等文件：先列出将创建的路径并检查冲突，复制模板、替换项目名与包名占位符，再检查未替换标记和目录结构；不覆盖内容不同的已有文件。已有项目的增量修改应由 Codex 阅读后逐个创建必要文件，不运行模板覆盖。

模板包含 configs/base.yaml、data/{raw,interim,processed,manifests}、weights/pretrained、src/<package>/{data,models}、trainer.py、evaluator.py、checkpoint.py、五个 scripts 入口、runs、logs、results/{raw,tables,figures}、docs、tests、pyproject.toml、README.md 和 .gitignore。Python 文件只有中文功能说明与 TODO，语法合法。M1 的配置仅记录项目名和待填写领域；绝不假设具体数据、算法超参数或 metrics。M1 不要求训练可运行。

目录职责：raw 保存只读原始数据；interim 保存中间产物；processed 保存可供模型使用的数据；manifests 保存来源、版本、许可、引用、校验、处理规则、划分协议、种子、生成代码及产物关联，且只记录已知事实。weights/pretrained 保存外部权重及其来源和校验，与 runs 下的训练 checkpoint 分开。src 只放可复用实现，scripts 只放薄入口。runs/<run_id> 保存正式运行配置、元数据、checkpoint 和指标；logs 保存非 run 专属日志；results/raw 保存结构化逐次结果，tables 与 figures 保存汇总产物。未取得真实结果时不生成统计数字。

验收 M1：默认目录与文件存在；没有未经确认的模型、指标和无效依赖；二次初始化不破坏文件。有 Python 环境时验证 Python 文件可编译、`pip install -e .` 后包可导入；没有时明确将这两项标为未验证，不因此声称训练可运行。
