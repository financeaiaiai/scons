#!/usr/bin/env python
#
# __COPYRIGHT__
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__revision__ = "__FILE__ __REVISION__ __DATE__ __DEVELOPER__"

import TestSCons
import sys

"""
Verify site_scons/site_init.py file can define a tool, and it shows up
automatically in the SCons.Script namespace.
"""

test = TestSCons.TestSCons()

test.subdir('site_scons')

if sys.platform == 'win32':
    cat_cmd='type'
else:
    cat_cmd='cat'

test.write(['site_scons', 'site_init.py'], """
def TOOL_FOO(env):
      env['FOO'] = '%s'
      bld = Builder(action = '$FOO ${SOURCE} > ${TARGET}',
				      suffix = '.tgt')
      env.Append(BUILDERS = {'Foo' : bld})

"""%cat_cmd)

test.write('SConstruct', """
e=Environment(tools=['default', TOOL_FOO])
e.Foo(target='foo.out', source='SConstruct')
""")

test.run(arguments = '-Q .',
         stdout = """%s SConstruct > foo.out\n"""%cat_cmd)


"""
Test errors in site_scons/site_init.py.
"""

test = TestSCons.TestSCons()

test.subdir('site_scons')

test.write(['site_scons', 'site_init.py'], """
raise Exception("Huh?")
""")

test.write('SConstruct', """
e=Environment(tools=['default', TOOL_FOO])
e.Foo(target='foo.out', source='SConstruct')
""")

test.run(arguments = '-Q .',
         stdout = "",
         stderr = """.*Error loading site_init file.*Huh\?.*""",
         status=2,
         match=TestSCons.match_re_dotall)



test.pass_test()

# end of file

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
