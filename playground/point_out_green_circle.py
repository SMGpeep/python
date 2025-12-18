# !/usr/bin/env python3
import pyniryo

# Roboter-Adresse festlegen
my_robot_ip = None
# Name Ihres Vision Workspace
workspace_name = None
# Name Ihrer Observierungspose
observation_pose_name = None

assert my_robot_ip is not None, \
    "Sie müssen die IP-Adresse Ihres Roboters definieren!"
assert workspace_name is not None, \
    "Sie müssen den Namen Ihres Workspaces definieren!"
assert observation_pose_name is not None, \
    "Sie müssen den Namen Ihrer Beobachtungspose definieren!"

# Verbindung herstellen
robot = pyniryo.NiryoRobot(my_robot_ip)
try:
    robot.calibrate_auto()           # Autokalibration durchführen
    robot.update_tool()              # Werkzeug erkennen
    robot.enable_tcp()               # Tool-TCP aktivieren

    assert robot.tool == pyniryo.ToolID.GRIPPER_1, \
        "Sie müssen den Greifer wieder anschließen!"

    # Observierungspose abrufen
    observation_pose = robot.get_pose_saved(observation_pose_name)

    while True:
        # In Observierungspose fahren
        robot.move(observation_pose)

        # Objekt mit Kreisform und grüner Farbe detektieren
        (object_found,
            object_pose,
            object_shape,
            object_color) = robot.detect_object(
                workspace_name=workspace_name,
                shape=pyniryo.ObjectShape.CIRCLE,
                color=pyniryo.ObjectColor.GREEN)
        if object_found:
            # Objekt wurde gesehen,
            # object_pose enthält Pose relativ zum Workspace
            x_rel, y_rel, yaw_rel = object_pose

            # Wir bestimmen die Pose im globalen Koordinatensystem,
            # 3cm über dem Objekt (height_offset=0.03)
            target_pose = robot.get_target_pose_from_rel(
                workspace_name=workspace_name,
                height_offset=0.03,
                x_rel=x_rel,
                y_rel=y_rel,
                yaw_rel=yaw_rel)
            # Auf Objekt zeigen
            robot.move(target_pose)
        # 1s warten
        robot.wait(1)
finally:
    robot.close_connection()        # Verbindung zum Roboter schließen
