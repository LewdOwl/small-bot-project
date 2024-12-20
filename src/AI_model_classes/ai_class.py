from datetime import datetime

class ai:
    instance = 0
    iniTime = datetime.now()
    msgCount = 0
    lastMsgTime =datetime.now()

    def __init__(self) -> None:
        self.iniTime = datetime.now()
        self.lastMsgTime = datetime.now()

    # methods ============================
    def update_msgCount_and_time(self)->None:
        self.msgCount+=1
        self.lastMsgTime = datetime.now()
        return
    
    def resetCond(self, maxExistingTime, 
                    maxConverTime, 
                    maxMsg, 
                    condition
                    )->int:
        maxExistingTime = maxExistingTime.total_seconds()
        maxConverTime   = maxConverTime.total_seconds()
        if condition:                                                   # check for base condition
            self.msgCount = 0
            return 1
        if ((maxExistingTime <= (datetime.now() - self.iniTime).seconds) or       #check for how long the instanc lasted
            (maxConverTime <= (datetime.now()  - self.lastMsgTime).seconds) or    #check for how long the last message lasted
            (maxMsg <= self.msgCount)):                                 #check for maximum message
            self.msgCount = 0
            return 1                                                    # need reset
        
        
        return 0
    

