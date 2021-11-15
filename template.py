import os

Dirs = {
    os.path.join("data","raw"),
    os.path.join("data","preprocessed"),
    "src",
    "saved_models",
    "notebooks"
}

files = {
    "dvc.yaml",
    "params.yaml",
    ".gitignore",
    os.path.join("src","__init__.py")
}


for _dir in Dirs:
    os.makedirs(_dir,exist_ok=True)
    with open(os.path.join(_dir,".gitkeep"),"w") as f:
        pass


for _file in files:
    with open(_file,"w") as f:
        pass 

