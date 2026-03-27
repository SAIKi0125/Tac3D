import os
import pybullet as p
import pybullet_data

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
URDF = os.path.join(ROOT, 'custom_assets', 'ur5_rg2_tacto', 'ur5_rg2_tacto.urdf')


def main():
    cid = p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.81)
    p.loadURDF('plane.urdf')
    robot = p.loadURDF(URDF, useFixedBase=True)

    print('robot_id =', robot)
    print('num_joints =', p.getNumJoints(robot))
    for joint_idx in range(p.getNumJoints(robot)):
        info = p.getJointInfo(robot, joint_idx)
        joint_name = info[1].decode('utf-8')
        child_link = info[12].decode('utf-8')
        if child_link in {'rg2_leftfinger', 'rg2_rightfinger', 'tacto_left_mount', 'tacto_right_mount', 'tool0'}:
            print(f'joint {joint_idx}: joint_name={joint_name}, child_link={child_link}')

    while p.isConnected(cid):
        p.stepSimulation()


if __name__ == '__main__':
    main()
