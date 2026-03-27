# Tac3D 项目说明

本目录是 Tac3D 的独立开发仓库，主要用于 Tac3D 传感器在 PyBullet + TACTO 下的调试、可视化与验证。

## 目录结构

- `assets/`：Tac3D 传感器与机器人相关资产（URDF/mesh 等）
- `conf/`：传感器与 demo 配置文件
- `demos/`：主要演示与测试入口脚本

## 运行环境

建议使用已有的 `parkour` 或 Tac3D 对应 conda 环境，并确保以下依赖可用：

- `pybullet`
- `tacto`
- `opencv-python`
- `numpy`

## 常用脚本

在 `Tac3D/` 根目录执行：

```bash
python demos/demo_pybullet_tac3d.py
```

调试/可视化测试：

```bash
python demos/demo_pybullet_tac3d_test.py
```

## 开发约定（来自 AGENTS）

- 主入口优先使用 `demos/demo_pybullet_tac3d.py`
- 调试实验优先放在 `demos/*test*.py`
- 除非明确要求，不直接修改原始资产包
- Tac3D 独立仓库以 `Tac3D/.gitignore` 为准

## Git 远程说明

- `origin`：个人 GitHub 仓库
- 如需同步上游，再额外添加 `upstream`
