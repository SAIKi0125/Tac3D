import os
import time

import pybullet as p
import pybullet_data

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROBOT_URDF = os.path.join(
    PROJECT_ROOT,
    "assets",
    "robot",
    "ur5_rg2_tac3d_description",
    "urdf",
    "ur5_rg2_tac3d.urdf",
)
SPHERE_URDF = os.path.join(PROJECT_ROOT, "assets", "object", "sphere_small.urdf")

ARM_HOME = [0.0, -1.57, 1.57, -1.57, -1.57, 0.0]
ACTIVE_GRIPPER_JOINTS = {
    "gripper_joint": 1.0,
    "l_finger_2_joint": -1.0,
    "l_finger_passive_joint": 1.0,
    "r_finger_1_joint": -1.0,
    "r_finger_2_joint": 1.0,
    "r_finger_passive_joint": -1.0,
}


def get_joint_map(body_id):
    joint_map = {}
    for joint_idx in range(p.getNumJoints(body_id)):
        info = p.getJointInfo(body_id, joint_idx)
        joint_map[info[1].decode("utf-8")] = joint_idx
    return joint_map




def find_link_id(body_id, link_name):
    for joint_idx in range(p.getNumJoints(body_id)):
        info = p.getJointInfo(body_id, joint_idx)
        child_link = info[12].decode("utf-8")
        if child_link == link_name:
            return joint_idx
    raise ValueError("Link not found: {}".format(link_name))


def get_midpoint_between_links(body_id, link_a, link_b):
    a_state = p.getLinkState(body_id, link_a, computeForwardKinematics=True)
    b_state = p.getLinkState(body_id, link_b, computeForwardKinematics=True)
    a_pos = a_state[0]
    b_pos = b_state[0]
    return [0.5 * (a + b) for a, b in zip(a_pos, b_pos)]

def print_joint_summary(body_id):
    print("Loaded joints:")
    for joint_idx in range(p.getNumJoints(body_id)):
        info = p.getJointInfo(body_id, joint_idx)
        joint_name = info[1].decode("utf-8")
        link_name = info[12].decode("utf-8")
        joint_type = info[2]
        print(
            "  idx={:2d} type={} joint={} child_link={}".format(
                joint_idx, joint_type, joint_name, link_name
            )
        )


def reset_arm_pose(body_id, joint_map):
    arm_joint_names = [
        "shoulder_pan_joint",
        "shoulder_lift_joint",
        "elbow_joint",
        "wrist_1_joint",
        "wrist_2_joint",
        "wrist_3_joint",
    ]
    for joint_name, target in zip(arm_joint_names, ARM_HOME):
        joint_idx = joint_map[joint_name]
        p.resetJointState(body_id, joint_idx, target)
        p.setJointMotorControl2(
            bodyUniqueId=body_id,
            jointIndex=joint_idx,
            controlMode=p.POSITION_CONTROL,
            targetPosition=target,
            force=200.0,
        )


def set_gripper_opening(body_id, joint_map, opening, force=80.0):
    for joint_name, multiplier in ACTIVE_GRIPPER_JOINTS.items():
        joint_idx = joint_map[joint_name]
        p.setJointMotorControl2(
            bodyUniqueId=body_id,
            jointIndex=joint_idx,
            controlMode=p.POSITION_CONTROL,
            targetPosition=multiplier * opening,
            force=force,
        )


def main():
    client = p.connect(p.GUI)
    if client < 0:
        raise RuntimeError("Failed to connect to PyBullet GUI")

    p.configureDebugVisualizer(p.COV_ENABLE_GUI, 1)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.81)
    p.loadURDF("plane.urdf")

    p.resetDebugVisualizerCamera(
        cameraDistance=1.4,
        cameraYaw=45.0,
        cameraPitch=-30.0,
        cameraTargetPosition=[0.0, 0.0, 0.35],
    )

    robot_id = p.loadURDF(
        ROBOT_URDF,
        basePosition=[0.0, 0.0, 0.0],
        baseOrientation=[0.0, 0.0, 0.0, 1.0],
        useFixedBase=True,
        flags=p.URDF_USE_INERTIA_FROM_FILE,
    )

    joint_map = get_joint_map(robot_id)
    print_joint_summary(robot_id)
    reset_arm_pose(robot_id, joint_map)
    set_gripper_opening(robot_id, joint_map, 0.35)

    left_link = find_link_id(robot_id, "tac3d_dl1_sensor_left")
    right_link = find_link_id(robot_id, "tac3d_dl1_sensor_right")
    sphere_position = get_midpoint_between_links(robot_id, left_link, right_link)
    sphere_position[0] += 0.002
    sphere_position[2] += 0.002
    p.loadURDF(
        SPHERE_URDF,
        basePosition=sphere_position,
        baseOrientation=[0.0, 0.0, 0.0, 1.0],
        globalScaling=0.18,
        useFixedBase=True,
    )

    gripper_slider = p.addUserDebugParameter("gripper_opening", -0.45, 1.0, 0.35)
    gripper_force_slider = p.addUserDebugParameter("gripper_force", 1.0, 200.0, 80.0)
    reset_button = p.addUserDebugParameter("reset_arm", 1, 0, 0)

    last_reset_value = p.readUserDebugParameter(reset_button)

    try:
        while p.isConnected():
            opening = p.readUserDebugParameter(gripper_slider)
            force = p.readUserDebugParameter(gripper_force_slider)
            reset_value = p.readUserDebugParameter(reset_button)

            if reset_value != last_reset_value:
                reset_arm_pose(robot_id, joint_map)
                last_reset_value = reset_value

            set_gripper_opening(robot_id, joint_map, opening, force=force)
            p.stepSimulation()
            time.sleep(1.0 / 240.0)
    finally:
        p.disconnect()


if __name__ == "__main__":
    main()
