import os
import time

import pybullet as p
import pybullet_data

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
URDF = os.path.join(ROOT, 'custom_assets', 'ur5_rg2_tacto', 'ur5_rg2_tacto.urdf')


def main():
    cid = p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.81)
    p.resetDebugVisualizerCamera(
        cameraDistance=1.3,
        cameraYaw=45,
        cameraPitch=-30,
        cameraTargetPosition=[0.0, 0.2, 0.4],
    )

    p.loadURDF('plane.urdf')
    robot = p.loadURDF(URDF, basePosition=[0, 0, 0], useFixedBase=True)

    print('robot_id =', robot)
    print('num_joints =', p.getNumJoints(robot))
    for joint_idx in range(p.getNumJoints(robot)):
        info = p.getJointInfo(robot, joint_idx)
        child_link = info[12].decode('utf-8')
        if child_link in {'rg2_leftfinger', 'rg2_rightfinger', 'tacto_left_mount', 'tacto_right_mount', 'digit_left', 'digit_right'}:
            print(joint_idx, info[1].decode('utf-8'), child_link)

    while p.isConnected(cid):
        p.stepSimulation()
        time.sleep(1.0 / 240.0)


if __name__ == '__main__':
    main()
