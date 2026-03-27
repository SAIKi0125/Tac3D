# Tac3D + TACTO 项目说明

这是基于 `tacto` 的个人开发仓库，主要用于 Tac3D 触觉传感器在 PyBullet 下的渲染、调试和机器人集成测试。

## 项目内容

- 原始 `tacto` 渲染与传感器接口
- `Tac3D/` 独立资产与 demo（已并入本仓库）
- RG2 / UR5 + Tac3D 组合测试脚本
- 自定义资产目录：`custom_assets/`

## 目录结构

- `tacto/`：TACTO Python 包源码
- `examples/`：原始示例
- `Tac3D/`：Tac3D 相关配置、资产和演示脚本
- `scripts/`：本项目诊断与验证脚本
- `custom_assets/`：自定义 URDF / mesh 资源

## 环境安装

要求 Python 版本：`3.7.12`。

```bash
conda env create -f environment.yml
conda activate tacto

pip install -e .
pip install -r requirements/examples.txt
```

## 常用运行命令

在仓库根目录执行：

```bash
# Tac3D 主演示
python Tac3D/demos/demo_pybullet_tac3d.py

# Tac3D 调试演示
python Tac3D/demos/demo_pybullet_tac3d_test.py

# UR5 + RG2 + Tac3D 联合测试
python Tac3D/demos/demo_pybullet_ur5_rg2_tac3d_control_tacto_test.py
```

## 开发约定

- Tac3D 主入口：`Tac3D/demos/demo_pybullet_tac3d.py`
- 调试与试验优先放在 `*test*.py` 或独立 demo
- 修改资产前先确认是否会影响现有 demo

## Git 远程说明

- `origin`：个人仓库（GitHub）
- `upstream`：原始 `facebookresearch/tacto`
