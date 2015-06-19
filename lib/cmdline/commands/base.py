# Copyright 2015 Curtis Sand
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class CommandMixin(object):
    """Command Mixin: Used to add commands to an interpreter.

    Subclasses of the CommandMixin should use mangled class attributes to avoid
    collisions when the interpreter object is put together.

    Example::

        class Example(CommandMixin):
            '''Example command help documentation.'''
            def __count(self, opts):
                pass  # some code goes here

            def __setup_parser(self):
                parser = ArgumentParser(prog='example',
                                        description=Example.__doc__)
                self._add_argument(parser, '-c', '--count', const=self.__count)
                return parser, self.__count

            def do_example(self, line):
                return super(Test2, self)._do(line, self.__setup_parser)

            def help_example(self):
                print(Example.__doc__)
    """

    def __init__(self, engine):
        self.engine = engine

    def _do(self, line, setup_parser):
        """
        The parser object will set arg.action to a method which will perform
        the action for this command. If opts.action is None, the method
        returned from "__setup_parser" will be called instead.
        """
        try:
            parser, default_action = setup_parser()
            (opts, args) = parser.parse_known_args(line.split(' '))
            setattr(opts, 'args', args)
            if opts.action is None:
                default_action(opts)
            else:
                opts.action(opts)
        except SystemExit:
            pass
        return False

    def _add_argument(self, parser, *args, **kwargs):
        """Help set the "action" and "dest" attrs for the argument"""
        action = 'action'
        dest = 'dest'
        if action not in kwargs:
            kwargs[action] = 'store_const'
        if dest not in kwargs:
            kwargs[dest] = action
        parser.add_argument(*args, **kwargs)
