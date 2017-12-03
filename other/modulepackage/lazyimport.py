#!/usr/bin/env python
# @Author  : pengyun

import types

class _Module(types.ModuleType):
    pass

class _LazyModule(_Module):
    def __init__(self, spec):
        super().__init__(spec.name)
        self.__file__ = spec.origin
        self.__package__ = spec.parent
        self.__loader__ = spec.loader
        self.__path__ = spec.submodule_search_locations
        self.__spec__ = spec

    def __getattr__(self, name):
        self.__class__ = _Module
        self.__spec__.loader.exec_module(self)
        assert sys.modules[self.__name__] == self
        return getattr(self, name)

import importlib.util, sys
def lazy_import(name):
 # If already loaded, return the module
    if name in sys.modules:
        return sys.modules[name]
    # Not loaded. Find the spec
    spec = importlib.util.find_spec(name)
    if not spec:
        raise ImportError('No module %r' % name)
     # Check for compatibility
    if not hasattr(spec.loader, 'exec_module'):
        raise ImportError('Not supported')
    module = sys.modules[name] = _LazyModule(spec)
    return module
