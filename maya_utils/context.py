from maya import cmds
class SuspendRefresh(): 

    def __enter__(self): 
        cmds.refresh(su=1)
      
    def __exit__(self, exc_type, exc_value, exc_traceback): 
        cmds.refresh(su=0)
