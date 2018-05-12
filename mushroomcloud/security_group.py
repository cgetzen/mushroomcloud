from .helper import cname
from .base import AwsType

class SecurityGroup(AwsType):
    def __init__(self, name, **kwargs):
        self.name = cname()
        self.validate_args(kwargs)
        self.args = {key: "None" for key in self.valid_args}
        self.args.update(kwargs)
        self.add_state_plan(self)

    @property
    def client(self):
        return "ec2"
    @property
    def create_method(self):
        return "create_security_group"

    @property
    def action_type(self):
        if "_action_type" in self.__dict__:
            return self._action_type
        if "id" not in self.state:
            self._action_type = "+"
            return "+"
        for key, val in self.args.items():
            if self.state[key] != val:
                self._action_type = "~"
                return "~"
                break

    def yaml(self):
        string = f"{self.name}:\n"
        string += "\n".join([f"  {key}: {val}" for key, val in self.args.items()])
        return string
        #
    def action(self):
        output = []

        output = [f"{self.action_type} {self.name}"]

        if "id" not in self.state:
            ## Create resource:
            for key, val in self.args.items():
                output.append(f"\t{key}: {val}")
            return "\n".join(output)
        for key, val in self.args.items():
            if self.state[key] != val:
                output.append(f"\tchange {key} from {self.state[key]} to {val}")
        return "\n".join(output)
