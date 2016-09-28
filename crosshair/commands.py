import argparse
import shlex
from crosshair import plugins


class BadArgumentsException(Exception):
    pass


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise BadArgumentsException(message)


class Command(object):
    def __init__(self, command_name):
        self.args = None
        self.parser = ArgumentParser(
            prog=command_name, add_help=False)
        self.setup_parser()

    def parse_args(self, arg_string):
        try:
            self.args = self.parser.parse_args(shlex.split(arg_string))
            return True
        except BadArgumentsException:
            return False

    def setup_parser(self):
        pass

    def execute(self, channel):
        pass

    def help(self, channel):
        return channel.send(self.parser.format_usage())


class HelpCommand(Command):
    def setup_parser(self):
        self.parser.add_argument('command')

    def execute(self, channel):
        if self.args.command == 'help':
            channel.send('This is getting needlessly meta.\n')
        command = plugins.get_command_handler(self.args.command)
        if command is None:
            channel.send(
                'Could not find help for command: %s\n' % self.args.command)
        else:
            command.help(channel)


class ListCommands(Command):
    def execute(self, channel):
        available = list(plugins.command_handlers.keys())
        available.sort()
        channel.send('\n'.join(available) + '\n')


class ReloadPluginsCommand(Command):
    def execute(self, channel):
        plugins.reload()
        channel.send('Plugins reloaded.\n')


plugins.register_command_handler(
    'help', HelpCommand)
plugins.register_command_handler(
    'list-commands', ListCommands)
plugins.register_command_handler(
    'reload-plugins', ReloadPluginsCommand)
