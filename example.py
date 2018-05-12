from mushroomcloud import SecurityGroup

x = SecurityGroup("myName", VpcId="a", Description="b")

class TwoSecurityGroups:
    def __init__(self, name, a, b):
        self.sg1 = SecurityGroup("SG1", VpcId = a)
        self.sg2 = SecurityGroup("SG2", VpcId = b)

class TwoWrapper:
    def __init__(self, name):
        self.two = TwoSecurityGroups("Two", 1, 2)

y = TwoWrapper("Wrapper")

## How do things execute at the end?
# push function that plans on global thing
# for each element,
#    compare with statefile
#    write to global thing
        # if no ID (does not exist)
            # - create function
            # - update state
        # - update function
        # - destroy/create function
        # - destroy function (hard)
# execute function that plans on global thing
