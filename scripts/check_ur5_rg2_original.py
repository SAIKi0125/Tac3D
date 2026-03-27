import os
import time

import pybullet as p
import pybullet_data

ASSET_ROOT = '/home/saiki/isaacsim_assets/Assets/Isaac/5.1/Isaac/Robots/ur5_rg2_ign'
URDF_PATH = os.path.join(ASSET_ROOT, 'urdf', 'ur5_rg2.isaac_fixed.urdf')


def main():
    cid = p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setAdditionalSearchPath(os.path.dirname(ASSET_ROOT))
    p.setGravity(0, 0, -9.81)
    p.resetDebugVisualizerCamera(
        cameraDistance=1.3,
        cameraYaw=45,
        cameraPitch=-30,
        cameraTargetPosition=[0.0, 0.2, 0.4],
    )

    p.loadURDF('plane.urdf')
    robot = p.loadURDF(URDF_PATH, basePosition=[0, 0, 0], useFixedBase=True)

    print('robot_id =', robot)
    print('urdf =', URDF_PATH)
    print('num_joints =', p.getNumJoints(robot))
    for joint_idx in range(p.getNumJoints(robot)):
        info = p.getJointInfo(robot, joint_idx)
        print(joint_idx, info[1].decode('utf-8'), info[12].decode('utf-8'))

    while p.isConnected(cid):
        p.stepSimulation()
        time.sleep(1.0 / 240.0)


if __name__ == '__main__':
    main()
