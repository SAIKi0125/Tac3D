# Repository Guidelines

## Project Structure & Module Organization
`tacto/` contains the installable Python package, including the renderer, sensor API, and bundled sensor configs such as `config_digit.yml`. `tests/` holds `pytest` coverage for core utilities and rendering behavior. `examples/` contains runnable demos and Hydra-style YAML configs under `examples/conf/`. `experiments/` stores research scripts and task-specific assets, while `meshes/` and `website/` contain sensor geometry and documentation media.

## Build, Test, and Development Commands
Install the package in editable mode with `pip install -e .`. Add demo dependencies with `pip install -r requirements/examples.txt`. Run the test suite with `pytest` or `nox -s tests`; the nox session installs `pytest` and exercises the editable package. Use `pre-commit run --all-files` before opening a PR to apply formatting and lint checks. For a local smoke test, run an example such as `python examples/demo_render.py` or `python examples/demo_pybullet_digit.py`.

## Coding Style & Naming Conventions
Target Python 3.6+ compatibility and follow the existing 4-space indentation style. Formatting is handled by Black with a 119-character line length; linting uses Flake8 with the same limit. Module filenames are lowercase with underscores, and tests follow the `test_*.py` pattern. Match the repository’s concise docstring and comment style, and preserve existing copyright headers where they already appear.

## Testing Guidelines
Write tests with `pytest` in `tests/`, keeping them focused and deterministic. Name test functions `test_<behavior>()` and place fixtures or test data next to the relevant test when practical. If you change rendering, sensor configuration, or timing helpers, add or update a regression test and run `pytest tests`. For example-specific changes, include the exact demo command you used for manual verification in the PR description.

## Commit & Pull Request Guidelines
Recent history favors short, imperative commit subjects such as `Update README.md` or `add shadow`; keep subjects brief and action-oriented. Pull requests should describe the behavior change, list validation steps, and link any relevant issue. Include screenshots or GIFs for rendering or demo changes, update `README.md` or example configs when APIs change, and ensure tests and lint checks pass before requesting review.

## Environment Notes
TACTO is primarily developed on Ubuntu. Headless rendering may require setting `PYOPENGL_PLATFORM=osmesa` or EGL support, so call out any environment-specific assumptions when changing rendering code.


## Tac3D Notes
Keep the standalone Tac3D work under `Tac3D/`. The main entrypoint is `Tac3D/demo_pybullet_tac3d.py`, which should use the original asset package at `Tac3D/assets/sensor/Tac3D/urdf/Tac3D.urdf`. The test entrypoint is `Tac3D/demo_pybullet_tac3d_test.py`; use it for visualization/debug-only experiments such as showing a non-URDF gel pad or alternate debug URDFs.

Do not modify the original Tac3D asset package in `Tac3D/assets/sensor/Tac3D/` unless explicitly requested. That package uses `package://Tac3D/...` mesh paths, so demo code must register `Tac3D/assets/sensor` as a PyBullet search root instead of rewriting the asset files.

For Tac3D tactile rendering, `tacto.config_path` must be set explicitly because `tacto.Sensor` defaults to the DIGIT config. The Tac3D sensor config currently lives at `Tac3D/conf/sensor/config_tac3d_local.yml`.

Treat Tac3D `camera.position`, `gel.origin`, and `lights.origin` in the sensor config as coordinates relative to the sensor `baseLink`, not world coordinates. Likewise, URDF `visual/collision origin` values are relative to the link frame. If a pad or debug plate appears displaced while `base_position` is unchanged, the offset is coming from the local origin in the URDF or sensor config, not from the world pose.

## 1. Repository constraints
- Read and followed the local `AGENTS.md` instructions.
- Main Tac3D entrypoint: `Tac3D/demo_pybullet_tac3d.py`.
- Debug and visualization work should go into `Tac3D/demo_pybullet_tac3d_test.py`.
- Avoid modifying original assets under `Tac3D/assets/sensor/Tac3D/` unless explicitly requested.

## 2. Tac3D URDF path changes
- Updated the main Tac3D demo to load `Tac3D_DL1_URDF.urdf` instead of `Tac3D.urdf`.
- Later restored the main demo to the simpler version without extra debug logic, while keeping the explicit Tac3D URDF selection in code.

## 3. Environment and import issue
- User hit `ModuleNotFoundError: No module named 'tacto'` when running the demo.
- Suggested installing the repo in editable mode with `pip install -e .` and verifying the active Python environment.

## 4. Encoder / motion question
- Checked whether any code applied encoder bias or active rotation.
- Conclusion: no explicit encoder bias or motor actuation in the Tac3D demo path.
- The loaded Tac3D sensor URDF had no joints, so no internal encoder-driven motion existed there.

## 5. Gel visualization work in test
- Added multiple debugging variants in `demo_pybullet_tac3d_test.py` during the session:
  - semi-transparent gel box visualization
  - gel-only visualization
  - gel surface sampling / curve visualization
  - sensor-axis visualization
  - test version aligned with main demo plus one gel visual
- Final user preference was to keep the main demo untouched and use `test` for extra visualization only.

## 6. Plane / orientation debugging
- Investigated why the ball imprint appeared on the wrong plane.
- Found that sensor base orientation and camera orientation heavily affected whether the gel appeared aligned with `xoy` or `yoz`.
- Also found a broken config state where camera position and orientation values had been accidentally swapped.

## 7. RGB / depth display behavior
- Clarified that TACTO GUI stacks RGB on top of depth when `show_depth=True`.
- Explained that the lower black region was the depth panel, not a missing render region.
- Noted that depth values vanish quickly at the gel boundary because the depth map is deformation relative to a reference gel surface, not a standard camera depth image.
- Explained the meaning of `zrange` and where to tune it in YAML.

## 8. Making Tac3D behave like DIGIT demos
- Aligned the Tac3D demo flow with the DIGIT demo structure where possible.
- Kept Tac3D-specific resource handling such as asset search paths and Tac3D config usage.
- Discussed that remaining differences were mostly due to geometry/config, not the Python loop structure.

## 9. Gel geometry explanation
- Explained the meaning of:
  - `gel.origin`
  - `gel.width`
  - `gel.height`
  - `curvature`
  - `curvatureMax`
  - `R`
  - `countW`
- Clarified that `curvature=False` gives a flat gel, while `curvature=True` gives a curved sampled surface.

## 10. Rolling demo request
- Added a Tac3D-specific rolling demo modeled after `examples/demo_pybullet_rolling.py`:
  - `Tac3D/demo_pybullet_tac3d_rolling.py`
  - `Tac3D/conf/tac3d_rolling.yaml`

## 11. RG2 gripper with Tac3D sensors
- User requested loading the RG2 gripper asset under:
  - `Tac3D/assets/robot/rg2_tac3d_description`
- Initially there was confusion between `.urdf.xacro` and plain `.urdf`.
- Switched to using the provided plain URDF:
  - `Tac3D/assets/robot/rg2_tac3d_description/urdf/rg2_tac3d_dual.urdf`
- Created a dedicated test loader:
  - `Tac3D/demo_pybullet_rg2_tac3d_test.py`
- The test loader:
  - rewrites URDF mesh paths for PyBullet
  - loads the RG2 gripper with dual Tac3D sensors
  - finds `tac3d_dl1_sensor_right` and `tac3d_dl1_sensor_left`
  - attaches both sensor links to TACTO
  - spawns a small sphere for contact testing

## 12. RG2 joint stabilization
- The RG2 test initially had unstable / problematic joints.
- Added logic to lock all movable joints in the test loader.
- Tried a wider open pose version, then reverted it at user request.
- Current state after rollback: joints are fixed at zero-position control targets.


## Session Notes
- Tac3D main entrypoint remains `Tac3D/demo_pybullet_tac3d.py`; prefer putting visualization and debug experiments into `Tac3D/demo_pybullet_tac3d_test.py` or separate test/demo files.
- The Tac3D demo was switched to use `Tac3D/assets/sensor/Tac3D/urdf/Tac3D_DL1_URDF.urdf` explicitly in code.
- For Tac3D rendering, `tacto` depth output is displayed through `show_depth` and `zrange`; `zrange` is a display normalization range, not a physical gel thickness parameter.
- If the tactile image seems mirrored or appears on the wrong plane, first check `digit.base_orientation`, `sensor.camera.orientation`, and `gel.origin` before changing rendering code.
- A common failure encountered in this session was accidentally swapping camera position and orientation values in `Tac3D/conf/sensor/config_tac3d_local.yml`; keep `camera.position` as a metric translation and `camera.orientation` as Euler angles.
- The Tac3D test file has been used for multiple gel visualizations: semi-transparent gel box, gel-only view, gel surface sampling, and a main-demo-matching version with one extra gel overlay.
- A Tac3D rolling demo modeled after `examples/demo_pybullet_rolling.py` was added as `Tac3D/demo_pybullet_tac3d_rolling.py` with config `Tac3D/conf/tac3d_rolling.yaml`.
- An RG2+Tac3D validation test was added as `Tac3D/demo_pybullet_rg2_tac3d_test.py`; it loads `Tac3D/assets/robot/rg2_tac3d_description/urdf/rg2_tac3d_dual.urdf`, rewrites mesh paths for PyBullet, finds the `tac3d_dl1_sensor_right` and `tac3d_dl1_sensor_left` links, and attaches both links to TACTO.
- In the RG2 test, the current behavior after rollback is to lock all movable joints at zero-position control targets for stability during sensor validation.
- Current working preference from the user: do not casually modify the main Tac3D demo; prefer isolated test files for experiments and debugging.
- `Tac3D/` was initialized as its own Git repository during this session. Treat `Tac3D/.gitignore` as the local source of truth for ignoring `.hydra/`, `__pycache__/`, `*.pyc`, `*.pyo`, and `*.log` inside that standalone workspace.
- The top-level Tac3D demo scripts were reorganized under `Tac3D/demos/`. When running or editing Tac3D demos, prefer the paths under `Tac3D/demos/` rather than the old top-level `Tac3D/demo_*.py` locations.
- Because the demos now live under `Tac3D/demos/`, Hydra demos must resolve `config_path`, `digit/object urdf_path`, and similar asset paths relative to `Tac3D/` project root, not relative to the `demos/` folder. Preserve this root-relative path handling when adding new demos.
- The UR5+RG2+Tac3D PyBullet assets now live under `Tac3D/assets/robot/ur5_rg2_tac3d_description/`. The main merged URDF is `Tac3D/assets/robot/ur5_rg2_tac3d_description/urdf/ur5_rg2_tac3d.urdf`.
- The standalone UR5 gripper-control test lives at `Tac3D/demos/demo_pybullet_ur5_rg2_tac3d_gripper_test.py`. It is a PyBullet-only validation script for UR5 arm pose plus RG2 mimic-joint control.
- The combined UR5+RG2+Tac3D control test lives at `Tac3D/demos/demo_pybullet_ur5_rg2_tac3d_control_tacto_test.py`. It currently loads `Tac3D/conf/tac3d_demo.yaml`, resolves the detailed Tac3D sensor config from there, prints left/right contact forces, and uses a fixed small sphere between the dual Tac3D sensors for contact testing.
- For the combined UR5+RG2+Tac3D control test, if the tactile depth view appears missing or weak, first inspect the contact object placement and actual contact-force printouts before changing the Tac3D YAML. In this setup, object pose and contact geometry were a more common cause than the YAML itself.
- User preference: after code changes are made, create a Git commit in the relevant repository by default unless the user explicitly asks not to commit for that turn.
