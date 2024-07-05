import importlib as importlib
from Plugin import Plugin as Plugin

class Test2:
    def factory(self, pluginName: str):
        pluginDir = importlib.import_module(f'plugins.{pluginName}.{pluginName}')
        pluginClass = getattr(pluginDir, pluginName)
        plugin = Plugin()
        pluginClass(plugin)
        return plugin