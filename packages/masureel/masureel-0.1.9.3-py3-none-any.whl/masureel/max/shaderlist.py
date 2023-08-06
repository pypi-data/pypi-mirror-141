import pymxs, json

# open up a matlib and parse the material names into a list

matpath = "X:/1082_MSR_BHP/Materials/Matlib_full.mat"


rt = pymxs.runtime
rt.loadMaterialLibrary(matpath)
matlib = rt.currentMaterialLibrary

shaders = {}

print(dir(matlib[0]))

print(type(matlib[0]))

for m in matlib:
    try:
        print(m.name, m.texmap_diffuse)
        if m.texmap_diffuse is not None:
            shaders[m.name] = True
        else:
            shaders[m.name] = False
    except:
        
        print(m.name, m.baseMtl)
        if m.baseMtl is not None:
            shaders[m.name] = True
        else:
            shaders[m.name] = False

print(json.dumps(shaders))

with open('shaders_full.json', 'w') as fp:
    json.dump(shaders, fp, indent=2)