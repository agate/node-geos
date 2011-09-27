import Options, Utils
from os import unlink, symlink, popen
from os.path import exists

srcdir = '.'
blddir = 'build'
VERSION = '0.0.1'

def set_options(opt):
  opt.tool_options('compiler_cxx')

def configure(conf):
  conf.check_tool('compiler_cxx')
  conf.check_tool('node_addon')

  geos_config = conf.find_program('geos-config', var='GEOS_CONFIG', mandatory=True)
  geos_ldflags = popen("%s --ldflags" % geos_config).readline().strip()[2:]
  conf.env.append_value("LIBPATH_GEOS", geos_ldflags)
  conf.env.append_value("LIB_GEOS", "geos_c")
  geos_cflags = popen("%s --cflags" % geos_config).readline().strip()
  conf.env.append_value("CPPPATH_GEOS", geos_cflags)

  conf.env.append_value("LIBPATH_PROJ", "/usr/lib")
  conf.env.append_value("LIBPATH_PROJ", "/usr/local/lib")
  conf.env.append_value("LIBPATH_PROJ", "/opt/local/lib")
  conf.env.append_value("LIB_PROJ", "proj")
  conf.env.append_value("CPPPATH_PROJ", "/usr/include")
  conf.env.append_value("CPPPATH_PROJ", "/usr/local/include")
  conf.env.append_value("CPPPATH_PROJ", "/opt/local/include")

def build(bld):
  obj = bld.new_task_gen('cxx', 'shlib', 'node_addon')
  obj.cxxflags = ["-g", "-D_LARGEFILE_SOURCE", "-Wall"]
  obj.target = 'geos'
  obj.source = "src/binding.cpp src/geometry.cpp src/projection.cpp src/strTree.cpp"
  obj.uselib = "GEOS PROJ"