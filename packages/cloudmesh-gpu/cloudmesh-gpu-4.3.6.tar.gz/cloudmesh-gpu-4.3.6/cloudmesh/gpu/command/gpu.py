import json

from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.gpu.gpu import Gpu
from pprint import pprint
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.console import Console
from cloudmesh.shell.command import map_parameters
import xmltodict
import yaml


class GpuCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_gpu(self, args, arguments):
        """
        ::

          Usage:
                gpu --json [--pretty]
                gpu --xml
                gpu --yaml
                gpu processes
                gpu system
                gpu status
                gpu

          This command returns some information about NVIDIA GPUs if your 
          system has them.

          Options:
              --json   returns the information in json
              --xml    returns the information in xml
              --yaml   returns the information in xml


        """

        map_parameters(arguments,
                       "json",
                       "xml",
                       "yaml",
                       "pretty")

        try:
            gpu = Gpu()

            if arguments.xml:
                try:
                    result = gpu.smi(output="xml")
                except:
                    Console.error("nvidia-smi must be installed on the system")
                    return ""

            elif arguments.json and arguments.pertty:
                result = gpu.smi(output="json")

            elif arguments.json:
                result = gpu.smi(output="json")

            elif arguments.yaml:
                result = gpu.smi(output="yaml")

            elif arguments.processes:
                arguments.pretty = True
                result = gpu.processes()

            elif arguments.system:
                arguments.pretty = True
                result = gpu.system()

            elif arguments.status:
                arguments.pretty = True
                result = gpu.status()

            else:
                result = gpu.smi()


            try:
                if arguments.pretty:
                    result = json.dumps(result, indent=2)
            except:
                result = None
        except:
            result = None
        print(result)

        return ""
