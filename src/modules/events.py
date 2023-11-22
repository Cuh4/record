# // ---------------------------------------------------------------------
# // ------- [Record] Events Module
# // ---------------------------------------------------------------------

# // ---- Imports
import inspect

# // ---- Variables
events: dict[str, "event"] = {}

# // ---- Functions
def isCoroutine(func: "function"):
    return inspect.iscoroutinefunction(func)

def getSavedEvent(name: str):
    return events.get(name, None)

# // ---- Classes
# // Event
# contains functions. when an event is called, all of its functions (callbacks) are called
class event:
    def __init__(self, name: str = ""):
        self.name = name
        self.callbacks: list["callback"] = []
        self.callbackID = 0
        
    def save(self):
        events[self.name] = self
        return self
        
    def unsave(self):
        events.pop(self.name, None)
        return self
        
    def fire(self, *args, **kwargs):
        returnValue = None
        
        # go through all regular functions and call them
        for callback in self.callbacks:
            if callback.isAsync:
                continue
            
            returnValue = callback.call(*args, **kwargs)
            
        # returns the most recent return value
        return returnValue
    
    async def asyncFire(self, *args, **kwargs):
        returnValue = None
        
        # go through all callbacks that are coroutines and call them
        for callback in self.callbacks:
            if not callback.isAsync:
                continue
            
            returnValue = await callback.asyncCall(*args, **kwargs)
            
        # returns the most recent return value
        return returnValue
    
    def attach(self, func: "function"):
        # increase callback id
        self.callbackID += 1

        # create callback for the provided function
        currentCallback = callback(
            func = func,
            id = self.callbackID
        )
        
        # attach it to this event
        currentCallback.attach(self)

        # return the callback
        return currentCallback
    
    def detach(self, callback: "callback"):
        callback.detach()
        return self

# // Callback   
# function with extra steps
class callback:
    def __init__(self, func: "function", id: int):
        # // attributes
        self.func = func
        self.id = id
        self.parent: "event" = None
        self.isAsync = isCoroutine(func)
        
    def attach(self, event: "event"):
        # set parent attribute
        self.parent = event
        
        # attach to parent's callbacks
        self.parent.callbacks.append(self)
        
        # return
        return self
        
    def detach(self):
        # no parent, so can't detach from anything
        if self.parent is None:
            return self
        
        # remove from parent's callbacks
        self.parent.callbacks.remove(self)
        
        # remove parent attribute
        self.parent = None
        
        # return
        return self
        
    def call(self, *args, **kwargs):
        # check if this is an async callback. if so, return here to prevent calling a coroutine like a regular function
        if self.isAsync:
            return
        
        # call function
        return self.func(*args, **kwargs)
    
    async def asyncCall(self, *args, **kwargs):
        # check if this is a normal function. if so, return here to prevent calling a function like a coroutine
        if not self.isAsync:
            return
        
        # call coroutine
        return await self.func(*args, **kwargs)