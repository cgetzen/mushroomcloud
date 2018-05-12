import atexit
import yaml
import boto3

class AwsType:

    state_plan = []

    @property
    def valid_args(self):
        if "_valid_args" in self.__dict__:
            return self._valid_args
        try:
            client = boto3.client(self.client, region_name="us-west-2")
            getattr(client, self.create_method)(WRONG="wrong", DryRun=True)
            # This should fail, and give an argument error
        except Exception as e:
            self._valid_args = str(e).split(": ")[-1].split(", ")
        return self._valid_args

    def validate_args(self, kwargs):
        if len(kwargs.keys() - self.valid_args) > 0:
            raise AttributeError(f"{kwargs.keys() - self.valid_args} not found in {self.valid_args}")

    def __getattr__(self, key):
        if key in self.args:
            return self.args[key]
        return super().__getattribute__(key)

    def __setattr__(self, key, val):
        if "args" in self.__dict__ and key in self.__dict__["args"]:
            self.__dict__["args"][key] = val
        else:
            super().__setattr__(key, val)

    @property
    def state(self):
        if "_state" in self.__dict__:
            return self._state
        # FUTURE: don't hardcode state.yaml :(
        state = yaml.load(open("state.yaml", 'rb').read())
        if self.name not in state:
            # raise LookupError(f"state not found for \"{self.name}\"")
            self._state = {key: "None" for key in self.valid_args}
        else:
            self._state = state[self.name]
        return self._state

    @classmethod
    def add_state_plan(cls, function):
        cls.state_plan.append(function)
        if atexit._ncallbacks() <= 1:
            def f(l):
                print("atexit command:")
                for element in l:
                    print(element.action())
                command = input()
                print("registered" + command)
            atexit.register(f, cls.state_plan)
