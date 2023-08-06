# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libnova', 'libnova.log', 'libnova.pwn', 'libnova.struct', 'libnova.typ']

package_data = \
{'': ['*']}

install_requires = \
['coloredlogs>=15.0.1,<16.0.0', 'pwntools>=4.7.0,<5.0.0']

setup_kwargs = {
    'name': 'libnova',
    'version': '0.1.14',
    'description': 'Personal python batteries libary -- mostly binary analysis, exploitation.',
    'long_description': '# libnova\nThe novafacing standard library but this time it\'s on PyPi\n\n## What is this for?\n\nMostly pwntools and angr wrapper stuff so I can avoid retyping things constantly.\nI also now only write strongly typed Python and I don\'t use strings for paths,\nwhich doesn\'t sound like a huge change but things don\'t play nice! So here\'s my\ncompatibility.\n\n## Example?\n\n```python\nfrom logging import getLogger\nfrom pathlib import Path\nfrom libnova import PW, PWMode\n\nl = getLogger(__name__).info\n\n\nb = Path("../src/target/debug/src")\n\nx = PW(binary=b, mode=PWMode.DEBUG)\n\nl(f"Loaded with {len(x.elf.symbols)} symbols")\n\nx.sendline(b":q")\nx.precvall()\n```\n\nThe nice part is we get some really nice output from *everything* (you can\'t see the colors but they are there!):\n\n```\n...\nINFO     | /home/novafa...a/pwn/pwn.py:0237 | Checksec info for library: ld-2.31.so\nINFO     | /home/novafa...a/pwn/pwn.py:0239 | RELRO:    Partial RELRO\nINFO     | /home/novafa...a/pwn/pwn.py:0239 | Stack:    No canary found\nINFO     | /home/novafa...a/pwn/pwn.py:0239 | NX:       NX enabled\nINFO     | /home/novafa...a/pwn/pwn.py:0239 | PIE:      PIE enabled\nINFO     | /home/novafa...a/pwn/pwn.py:0241 | Checksec info for main object: src\nINFO     | /home/novafa...a/pwn/pwn.py:0243 | RELRO:    Full RELRO\nINFO     | /home/novafa...a/pwn/pwn.py:0243 | Stack:    No canary found\nINFO     | /home/novafa...a/pwn/pwn.py:0243 | NX:       NX enabled\nINFO     | /home/novafa...a/pwn/pwn.py:0243 | PIE:      PIE enabled\nINFO     |                    __main__:0012 | Loaded with 1260 symbols\nINFO     | pwnlib.tubes...365646789552:0298 | Receiving all data\nINFO     | pwnlib.tubes...365646789552:0298 | Receiving all data: 0B\nINFO     | pwnlib.tubes...365646789552:0298 | Receiving all data: 108B\nINFO     | pwnlib.tubes...365646789552:0298 | Receiving all data: 136B\nINFO     | pwnlib.tubes...365646789552:0298 | Process \'/usr/local/bin/gdbserver\' stopped with exit code 0 (pid 419479)\nINFO     | pwnlib.tubes...365646789552:0298 | Receiving all data: Done (136B)\nb\'Welcome to the embedded programming simulator!\\nOf course, you can only code using vim if you are 133...\\nex: \\nChild exited with status 0\\n\'\n```\n',
    'author': 'novafacing',
    'author_email': 'rowanbhart@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/novafacing/libnova.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.8.10',
}


setup(**setup_kwargs)
