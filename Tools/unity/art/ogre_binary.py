"""Strict sequential readers for Ogre/Fairy mesh 1.30/1.40 and skeleton 1.10, from bundled serializers."""
import math
import struct

def text(data):
    # OGRE resource keys in this source snapshot are GBK bytes, even when also valid UTF-8.
    try:return data.decode('gb18030')
    except UnicodeError:return data.decode('utf8')

def unpack(fmt,data,p):
    size=struct.calcsize(fmt)
    if p<0 or p+size>len(data):raise ValueError('Truncated binary data')
    return struct.unpack_from(fmt,data,p)

def line(data,p):
    end=data.index(b'\n',p,min(p+4096,len(data)))
    return text(data[p:end]),end+1

def finite(values):
    if not all(math.isfinite(v) for v in values):raise ValueError('Nonfinite asset data')
    return list(values)

def mesh(data):
    if data[:2]!=b'\x00\x10':raise ValueError('Invalid mesh header/endian')
    version,p=line(data,2)
    if version not in ['[MeshSerializer_v1.40]','[MeshSerializer_v1.30]']:raise ValueError('Unsupported mesh version '+version)
    shared=None;geo=None;sub=None;parts=[];skeleton='';binding=0;stride=0
    skipped=[]
    def geometry(count):
        if not 0<=count<=10000000:raise ValueError('Unreasonable vertex count')
        return dict(count=count,decl=[],buffers={},assignments=[])
    while p+6<=len(data):
        cid,size=unpack('<HI',data,p);q=p+6
        if cid==0x3000:p=q+1
        elif cid==0x4000:
            material,q=line(data,q);use_shared,count,wide=unpack('<?I?',data,q);q+=6
            if count>30000000:raise ValueError('Unreasonable index count')
            indices=list(unpack('<'+('I' if wide else 'H')*count,data,q));p=q+count*(4 if wide else 2)
            sub=dict(material=material,shared=use_shared,indices=indices,operation=4,geometry=None);parts.append(sub);geo=None
        elif cid==0x4010:
            if sub is None:raise ValueError('Operation without submesh')
            sub['operation']=unpack('<H',data,q)[0];p=q+2
        elif cid==0x5000:
            geo=geometry(unpack('<I',data,q)[0]);p=q+4
            if sub is None:shared=geo
            else:sub['geometry']=geo
        elif cid==0x5100:p=q
        elif cid==0x5110:
            if geo is None:raise ValueError('Declaration without geometry')
            geo['decl'].append(unpack('<5H',data,q));p=q+10
        elif cid==0x5200:binding,stride=unpack('<2H',data,q);p=q+4
        elif cid==0x5210:
            if geo is None or stride==0:raise ValueError('Invalid vertex buffer')
            end=q+geo['count']*stride
            if end>len(data):raise ValueError('Truncated vertex buffer')
            geo['buffers'][binding]=(stride,data[q:end]);p=end
        elif cid in (0x4100,0x7000):
            vertex,bone,weight=unpack('<IHf',data,q);p=q+10
            target=shared if cid==0x7000 else (sub['geometry'] if sub else None)
            if target is None:raise ValueError('Bone assignment without geometry')
            if vertex>=target['count'] or not math.isfinite(weight) or weight<0:raise ValueError('Invalid skin assignment')
            target['assignments'].append((vertex,bone,weight))
        elif cid==0x6000:skeleton,p=line(data,q)
        elif cid==0x4200:
            _,q=line(data,q);_,p=line(data,q)
        elif cid==0x9000:p=q+28
        elif cid==0xA000:p=q
        elif cid==0xA100:_,p=line(data,q+2)
        elif cid in {0x8000,0xB000,0xC000,0xD000,0xE000} and 6<=size<=len(data)-p:
            skipped.append(hex(cid));p+=size
        elif all(v==0 for v in data[p:]) and len(data)-p<=64:break
        else:raise ValueError(f'Unsupported mesh chunk {cid:#x} at {p}')
        if p>len(data):raise ValueError('Mesh chunk exceeds file')
    if p<len(data) and any(data[p:]):raise ValueError('Unparsed mesh tail')
    result=[]
    for part in parts:
        g=shared if part['shared'] else part['geometry']
        if g is None:raise ValueError('Submesh geometry missing')
        count=g['count'];attrs={}
        for source,typ,semantic,offset,index in g['decl']:
            if semantic not in [1,4,7] or (semantic==7 and index!=0):continue
            if typ not in [0,1,2,3]:raise ValueError('Unsupported vertex attribute type '+str(typ))
            components=typ+1;vertex_stride,buffer=g['buffers'][source]
            if offset+components*4>vertex_stride:raise ValueError('Vertex element exceeds stride')
            values=[]
            for i in range(count):values+=unpack('<'+'f'*components,buffer,i*vertex_stride+offset)
            if semantic==4 and not all(math.isfinite(v) for v in values):
                attrs[semantic]=(components,[])
            else:attrs[semantic]=(components,finite(values))
        if 1 not in attrs or attrs[1][0] not in [3,4]:raise ValueError('FLOAT3/FLOAT4 positions required')
        indices=part['indices']
        if indices and max(indices)>=count:raise ValueError('Mesh index out of bounds')
        if part['operation']==4:
            if len(indices)%3:raise ValueError('Invalid triangle list')
            triangles=[v for i in range(0,len(indices),3) for v in [indices[i],indices[i+2],indices[i+1]]]
        elif part['operation'] in [5,6]:
            triangles=[]
            for i in range(2,len(indices)):
                a,b,c=(indices[i-2],indices[i-1],indices[i]) if part['operation']==5 else (indices[0],indices[i-1],indices[i])
                if part['operation']==5 and i%2:a,b=b,a
                if len({a,b,c})==3:triangles.extend([a,c,b])
        else:raise ValueError('Unsupported primitive operation '+str(part['operation']))
        weights=[[] for _ in range(count)]
        for vertex,bone,weight in g['assignments']:weights[vertex].append((bone,weight))
        ids=[];normalized=[];trimmed=0
        for row in weights:
            row=sorted(row,key=lambda v:-v[1]);trimmed+=max(0,len(row)-4);row=row[:4]
            total=sum(w for _,w in row)
            ids.extend([b for b,_ in row]+[0]*(4-len(row)))
            normalized.extend([w/total if total else 0 for _,w in row]+[0]*(4-len(row)))
        result.append(dict(material=part['material'],positions=[attrs[1][1][i*attrs[1][0]+j]*.01 for i in range(count) for j in range(3)],sourcePositionW=attrs[1][1][3::4] if attrs[1][0]==4 else [],normalRepair=4 in attrs and not attrs[4][1],
            normals=attrs.get(4,(3,[]))[1],uv=attrs.get(7,(2,[]))[1],uvComponents=attrs.get(7,(2,[]))[0],
            triangles=triangles,boneIds=ids,weights=normalized,trimmedWeights=trimmed,hasSkin=bool(g['assignments'])))
    if not result:raise ValueError('Mesh has no submeshes')
    return dict(schema=1,version=version,parts=result,skeleton=skeleton,skippedChunks=skipped)

def skeleton(data):
    if data[:2]!=b'\x00\x10':raise ValueError('Invalid skeleton endian/header')
    version,p=line(data,2)
    if version!='[Serializer_v1.10]':raise ValueError('Unsupported skeleton version '+version)
    bones=[];parents={};animations=[];links=[];animation=None;track=None
    def key(time,rotation=(0,0,0,1),position=(0,0,0),scale=(1,1,1)):
        finite([time]);return dict(time=time,rotation=finite(rotation),position=[v*.01 for v in finite(position)],scale=finite(scale))
    while p+6<=len(data):
        cid,size=unpack('<HI',data,p);q=p+6
        if cid==0x1010:p=q+2
        elif cid==0x2000:
            name,q=line(data,q);handle=unpack('<H',data,q)[0];q+=2
            vals=finite(unpack('<7f',data,q));q+=28
            scale=finite(unpack('<3f',data,q)) if size>36 else [1,1,1]
            if size>36:q+=12
            bones.append(dict(id=handle,name=name,parent=-1,position=[v*.01 for v in vals[:3]],rotation=vals[3:],scale=scale));p=q
        elif cid==0x3000:
            child,parent=unpack('<HH',data,q);parents[child]=parent;p=q+4
        elif cid==0x4000:
            name,q=line(data,q);duration=unpack('<f',data,q)[0];p=q+4
            finite([duration]);animation=dict(name=name,duration=duration,tracks=[]);animations.append(animation)
        elif cid==0x4010:raise ValueError('Animation base-keyframe rebasing requires explicit support')
        elif cid==0x4100:
            if animation is None:raise ValueError('Track without animation')
            track=dict(boneId=unpack('<H',data,q)[0],keys=[]);animation['tracks'].append(track);p=q+2
        elif cid==0x4110:
            if track is None:raise ValueError('Key without track')
            vals=unpack('<8f',data,q);q+=32
            scale=unpack('<3f',data,q) if size>38 else (1,1,1)
            if size>38:q+=12
            track['keys'].append(key(vals[0],vals[1:5],vals[5:8],scale));p=q
        elif cid==0x4120:
            if track is None:raise ValueError('Keys without track')
            count,flags=unpack('<HH',data,q);q+=4
            if flags&~7:raise ValueError('Unsupported compact key flags')
            for _ in range(count):
                t=unpack('<f',data,q)[0];q+=4;r=(0,0,0,1);v=(0,0,0);s=(1,1,1)
                if flags&1:r=unpack('<4f',data,q);q+=16
                if flags&2:v=unpack('<3f',data,q);q+=12
                if flags&4:s=unpack('<3f',data,q);q+=12
                track['keys'].append(key(t,r,v,s))
            p=q
        elif cid==0x5000:
            name,q=line(data,q);scale=unpack('<f',data,q)[0];p=q+4;links.append(dict(name=name,scale=scale))
        elif all(v==0 for v in data[p:]) and len(data)-p<=64:break
        else:raise ValueError(f'Unsupported skeleton chunk {cid:#x} at {p}')
        if p>len(data):raise ValueError('Skeleton chunk exceeds file')
    if p<len(data) and any(data[p:]):raise ValueError('Unparsed skeleton tail')
    handles={b['id'] for b in bones}
    if len(handles)!=len(bones) or not bones:raise ValueError('Missing/duplicate bones')
    for bone in bones:
        bone['parent']=parents.get(bone['id'],-1)
        visited={bone['id']};parent=bone['parent']
        while parent!=-1:
            if parent not in handles or parent in visited:raise ValueError('Invalid/cyclic bone hierarchy')
            visited.add(parent);parent=parents.get(parent,-1)
    for a in animations:
        for t in a['tracks']:
            if t['boneId'] not in handles:raise ValueError('Animation references absent bone')
            t['keys'].sort(key=lambda k:k['time'])
    return dict(schema=1,version=version,bones=bones,animations=animations,links=links)
