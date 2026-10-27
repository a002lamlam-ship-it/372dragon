"""Blender headless validation of an original skinned asset/rest and attack pose; not a Unity screenshot."""
import bpy
import json
from pathlib import Path
import sys
from mathutils import Matrix,Quaternion,Vector
args=sys.argv[sys.argv.index('--')+1:]
file=Path(args[0]);out=Path(args[1]);out.mkdir(parents=True,exist_ok=True)
asset=json.loads(file.read_text());bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
rig_data=bpy.data.armatures.new('OriginalRig');rig=bpy.data.objects.new('OriginalRig',rig_data);bpy.context.collection.objects.link(rig);bpy.context.view_layer.objects.active=rig;rig.select_set(True)
bpy.ops.object.mode_set(mode='EDIT')
bones={b['id']:b for b in asset['rig']['bones']};global_matrices={}
def rest(handle):
 if handle in global_matrices:return global_matrices[handle]
 b=bones[handle];q=b['rotation'];local=Matrix.LocRotScale(Vector(b['position']),Quaternion((q[3],q[0],q[1],q[2])),Vector(b['scale']))
 matrix=rest(b['parent'])@local if b['parent']>=0 else local;global_matrices[handle]=matrix;return matrix
for handle,b in bones.items():
 edit=rig_data.edit_bones.new('Bone_'+str(handle));matrix=rest(handle);edit.head=matrix.translation;edit.tail=edit.head+matrix.to_3x3()@Vector((0,.08,0));edit.matrix=matrix;edit.length=.08
for handle,b in bones.items():
 if b['parent']>=0:rig_data.edit_bones['Bone_'+str(handle)].parent=rig_data.edit_bones['Bone_'+str(b['parent'])]
bpy.ops.object.mode_set(mode='OBJECT')
objects=[]
for index,part in enumerate(asset['parts']):
 points=[part['positions'][i:i+3] for i in range(0,len(part['positions']),3)]
 # The converter reverses winding for Unity; reverse back for Blender's right-handed renderer.
 faces=[(part['triangles'][i],part['triangles'][i+2],part['triangles'][i+1]) for i in range(0,len(part['triangles']),3)]
 mesh=bpy.data.meshes.new('OriginalMesh');mesh.from_pydata(points,[],faces);mesh.update()
 obj=bpy.data.objects.new('OriginalMesh_'+str(index),mesh);bpy.context.collection.objects.link(obj);objects.append(obj)
 if part['uv']:
  layer=mesh.uv_layers.new();stride=part['uvComponents']
  for polygon in mesh.polygons:
   for loop_index in polygon.loop_indices:
    v=mesh.loops[loop_index].vertex_index;layer.data[loop_index].uv=part['uv'][v*stride:v*stride+2]
 for handle in bones:obj.vertex_groups.new(name='Bone_'+str(handle))
 if part['hasSkin']:
  for vertex in range(len(points)):
   for k in range(4):
    weight=part['weights'][vertex*4+k]
    if weight>0:obj.vertex_groups['Bone_'+str(part['boneIds'][vertex*4+k])].add([vertex],weight,'REPLACE')
  modifier=obj.modifiers.new('OriginalSkin','ARMATURE');modifier.object=rig
 mat=bpy.data.materials.new(part['material']);mat.use_nodes=True;bsdf=mat.node_tree.nodes.get('Principled BSDF')
 texture=asset['materials'][index]['textureFile']
 if texture:
  node=mat.node_tree.nodes.new('ShaderNodeTexImage');node.image=bpy.data.images.load(str(file.parent/texture));mat.node_tree.links.new(node.outputs['Color'],bsdf.inputs['Base Color'])
 bsdf.inputs['Roughness'].default_value=.75;mesh.materials.append(mat)
# Ogre/Unity use Y up; Blender uses Z up. Rotate the whole source scene for the preview.
from math import radians
rig.rotation_euler.x=radians(90)
for obj in objects:obj.rotation_euler.x=radians(90)
bpy.context.view_layer.update()
points=[obj.matrix_world@Vector(corner) for obj in objects for corner in obj.bound_box];center=sum(points,Vector())/len(points);span=max((p-center).length for p in points)
world=bpy.context.scene.world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.12,.12,.12,1)
bpy.ops.object.camera_add(location=center+Vector((span*2.3,-span*3,span*1.2)));camera=bpy.context.object;camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler();bpy.context.scene.camera=camera
for location,power,size in [(center+Vector((3,-4,6)),700,5),(center+Vector((-4,0,3)),400,4)]:
 bpy.ops.object.light_add(type='AREA',location=location);light=bpy.context.object;light.data.energy=power;light.data.shape='DISK';light.data.size=size;light.rotation_euler=(center-light.location).to_track_quat('-Z','Y').to_euler()
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.use_denoising=False;scene.cycles.samples=16;scene.render.resolution_x=512;scene.render.resolution_y=512;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.filepath=str(out/'rest.png');bpy.ops.render.render(write_still=True)
clip=next(a for a in asset['rig']['animations'] if a['name']=='攻击')
for track in clip['tracks']:
 keys=track['keys'];key=min(keys,key=lambda k:abs(k['time']-.5));q=key['rotation'];bone=bones[track['boneId']];rest_q=bone['rotation'];pose=rig.pose.bones['Bone_'+str(track['boneId'])];pose.rotation_mode='QUATERNION';pose.rotation_quaternion=Quaternion((q[3],q[0],q[1],q[2]));pose.location=Quaternion((rest_q[3],rest_q[0],rest_q[1],rest_q[2])).inverted()@Vector(key['position']);pose.scale=Vector(key['scale'])
bpy.context.view_layer.update();scene.render.filepath=str(out/'attack.png');bpy.ops.render.render(write_still=True)
print('ORIGINAL_ART_RENDER_OK',len(bones),len(clip['tracks']),clip['duration'])
