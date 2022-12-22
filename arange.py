import maya.cmds as cmds
import math
import pymel.core

selection = cmds.ls(orderedSelection=True)

# Thanks Toke Jepsen for this part, it unfreezes transform of objects so we can calculate in world space coordinate. https://gist.github.com/tokejepsen
for node in pymel.core.ls(selection=True):
    grp1 = pymel.core.group(empty=True)
    grp2 = pymel.core.group(empty=True)
    
    pymel.core.delete(pymel.core.parentConstraint(node, grp1))
    pymel.core.delete(pymel.core.parentConstraint(node, grp2))
    
    pymel.core.parent(node, grp1)
    grp1.tx.set(0)
    grp1.ty.set(0)
    grp1.tz.set(0)
    grp1.rx.set(0)
    grp1.ry.set(0)
    grp1.rz.set(0)
    
    pymel.core.parent(node, w=True)
    pymel.core.makeIdentity(node, apply=True, t=1, r=1, s=1, n=0)
    
    pymel.core.delete(pymel.core.parentConstraint(grp2, node))
    pymel.core.delete([grp1, grp2])    
    
    

# Get the start and end points

if len(selection) >= 2:
    start_point = cmds.xform(selection[0], t =True, q =True, ws =True)
    end_point = cmds.xform(selection[1], t =True, q =True, ws =True)
else:
    print("Error: At least two objects must be selected")
    

# Calculate the distance between the start and end points
dx = end_point[0] - start_point[0]
dy = end_point[1] - start_point[1]
dz = end_point[2] - start_point[2]
distance = math.sqrt(dx**2 + dy**2 + dz**2)

if distance == 0:
    print("Error: The start and end points cannot be at the same position")
else:
        
    # Calculate the number of objects to arrange
    num_objects = len(selection) - 2

    # Calculate the spacing between the objects
    spacing = distance / (num_objects + 1)

    # Calculate the positions of the objects
    positions = []
    for i in range(num_objects):
        pos = [
            start_point[0] + (i + 1) * spacing * dx / distance,
            start_point[1] + (i + 1) * spacing * dy / distance,
            start_point[2] + (i + 1) * spacing * dz / distance
        ]
        positions.append(pos)

    # Move the objects to their positions
    for i, object_name in enumerate(selection[2:]):
        cmds.move(positions[i][0], positions[i][1], positions[i][2], object_name, absolute=True, ws=True)
