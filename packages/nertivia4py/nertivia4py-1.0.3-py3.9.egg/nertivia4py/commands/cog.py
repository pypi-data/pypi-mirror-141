class Cog:
    def __init__(self, name, commands_class, lib_path, commands):
        self.name = name
        self.commands_class = commands_class
        self.lib_path = lib_path
        self.commands = commands

    def get_commands(self):
        return self.commands