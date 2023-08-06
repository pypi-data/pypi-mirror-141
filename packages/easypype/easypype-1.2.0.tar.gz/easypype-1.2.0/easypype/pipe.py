import abc
import easypype.command as c
import easypype.sink as s
from multiprocessing.pool import ThreadPool


class Pipe(c.Command):
    """A Command implementation that executes a list of commands.
    
    ...
    Attributes:
    - commands : List[Command]
        The commands to be executed.
    ...
    Methods:
    - do(sink : Sink)
        Executes each command listed, saving results to the sink."""

    def __init__(self):
        self.pool = ThreadPool()
        self.commands = list()

    def parallelize(self, sink: s.Sink, command: c.Command):
        arguments = [(sink, )]
        sink.collect(self.pool.starmap(command.do, arguments)[0])

    def do(self, sink: s.Sink):
        """Executes each command listed."""
        for command in self.commands:
            self.parallelize(sink, command)


class PipeBuilder(abc.ABC):

    @abc.abstractproperty
    def build(self) -> Pipe:
        pass

    @abc.abstractmethod
    def command(self, command: c.Command):
        pass


class PipeBuilderConcrete(PipeBuilder):
    """A PipeBuilder implementation.
    
    ...
    Attributes:
    - pipe : Pipe
        The Pipe object to be built.
    ...
    Methods:
    - build()
        Returns the built Pipe.
    - command(command : Command)
        Appends the command to Pipe list of commands.
    - __init__()
        Begins the building."""

    def __init__(self):
        """Initializes an empty Pipe to be built."""
        self.pipe = Pipe()

    def build(self) -> Pipe:
        """Returns Pipe instance."""
        return self.pipe

    def command(self, command: c.Command):
        """Appends command to Pipe."""
        self.pipe.commands.append(command)
        return self
