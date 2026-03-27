import os
import time

import pybullet as p
import pybullet_data

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
URDF_PATH = os.path.join(ROOT, 'meshes', 'Tac3D.urdf')


def add_debug_frame(position, axis_len=0.02, line_width=2):
    x, y, z = position
    p.addUserDebugLine([x, y, z], [x + axis_len, y, z], [1, 0, 0], lineWidth=line_width)
    p.addUserDebugLine([x, y, z], [x, y + axis_len, z], [0, 1, 0], lineWidth=line_width)
    p.addUserDebugLine([x, y, z], [x, y, z + axis_len], [0, 0, 1], lineWidth=line_width)


def main():
    cid = p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.81)
    p.resetDebugVisualizerCamera(
        cameraDistance=0.18,
        cameraYaw=45,
        cameraPitch=-30,
        cameraTargetPosition=[0.02, 0.0, 0.02],
    )

    p.loadURDF('plane.urdf')

    tac3d_id = p.loadURDF(
        URDF_PATH,
        basePosition=[0.0, 0.0, 0.02],
        baseOrientation=p.getQuaternionFromEuler([0.0, 0.0, 0.0]),
        useFixedBase=True,
    )

    print('Tac3D loaded:', tac3d_id)
    print('URDF path:', URDF_PATH)
    print('num_joints:', p.getNumJoints(tac3d_id))
    print('base pose:', p.getBasePositionAndOrientation(tac3d_id))

    add_debug_frame([0.0, 0.0, 0.02])

    while p.isConnected(cid):
        p.stepSimulation()
        time.sleep(1.0 / 240.0)


if __name__ == '__main__':
    main()
