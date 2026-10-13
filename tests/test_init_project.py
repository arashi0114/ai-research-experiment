"""M1、M2 增量和现有项目保护的确定性测试。"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
INITIALIZER = SKILL_ROOT / "scripts" / "init_project.py"


def initialize(project: Path, name: str = "research-demo") -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(INITIALIZER), "--project-name", name, "--path", str(project)],
        text=True,
        capture_output=True,
    )


class InitProjectTests(unittest.TestCase):
    def test_a_blank_scaffold_and_repeat(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "research-demo"
            first = initialize(project)
            self.assertEqual(first.returncode, 0, first.stderr)

            required = [
                "configs/base.yaml", "pyproject.toml", "README.md", ".gitignore",
                "data/raw/.gitkeep", "data/interim/.gitkeep", "data/processed/.gitkeep",
                "data/manifests/.gitkeep", "weights/pretrained/.gitkeep",
                "runs/.gitkeep", "logs/.gitkeep", "results/raw/.gitkeep",
                "results/tables/.gitkeep", "results/figures/.gitkeep",
                "docs/.gitkeep", "tests/.gitkeep",
                "src/research_demo/__init__.py", "src/research_demo/data/dataset.py",
                "src/research_demo/data/loader.py", "src/research_demo/models/model.py",
                "src/research_demo/trainer.py", "src/research_demo/evaluator.py",
                "src/research_demo/checkpoint.py", "scripts/preprocess.py",
                "scripts/extract_features.py", "scripts/train.py", "scripts/evaluate.py",
                "scripts/summarize.py",
            ]
            for name in required:
                self.assertTrue((project / name).is_file(), name)

            for source in project.rglob("*.py"):
                content = source.read_text(encoding="utf-8")
                compile(content, str(source), "exec")
                self.assertIn("# TODO：", content)
                self.assertNotIn("class ", content)
                self.assertNotIn("def ", content)

            self.assertIn('name = "research-demo"', (project / "pyproject.toml").read_text())
            self.assertIn('name: "research-demo"', (project / "configs/base.yaml").read_text())
            self.assertIn("weights/pretrained/*", (project / ".gitignore").read_text())
            second = initialize(project)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertIn("已创建 0 个文件", second.stdout)

    def test_b_multimodal_extension_stays_small(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "multimodal"
            self.assertEqual(initialize(project, "multimodal").returncode, 0)
            model_dir = project / "src" / "multimodal" / "models"
            for name in ("text_encoder.py", "image_encoder.py", "recommender.py"):
                (model_dir / name).write_text("# 功能：根据已确认架构实现。\n# TODO：确认接口后编码。\n", encoding="utf-8")
            plan = project / "docs" / "architecture_plan.md"
            plan.write_text("文本/图像输入 -> 编码器 -> 推荐模型；融合方式待确认。\n", encoding="utf-8")
            self.assertEqual(initialize(project, "multimodal").returncode, 0)
            self.assertEqual(
                {path.name for path in model_dir.glob("*.py")},
                {"__init__.py", "model.py", "text_encoder.py", "image_encoder.py", "recommender.py"},
            )
            self.assertIn("融合方式待确认", plan.read_text(encoding="utf-8"))

    def test_e_conflict_fails_before_any_write(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "existing"
            self.assertEqual(initialize(project, "existing").returncode, 0)
            trainer = project / "src" / "existing" / "trainer.py"
            trainer.write_text("# 用户代码\n", encoding="utf-8")
            missing = project / "scripts" / "summarize.py"
            missing.unlink()
            result = initialize(project, "existing")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("未覆盖", result.stderr)
            self.assertEqual(trainer.read_text(encoding="utf-8"), "# 用户代码\n")
            self.assertFalse(missing.exists())

    def test_invalid_package_name_fails_fast(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "invalid"
            result = initialize(project, "123")
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(project.exists())


if __name__ == "__main__":
    unittest.main()
