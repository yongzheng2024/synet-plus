## <b>SyNet-Plus(NetComplete) Configure on Ubuntu 22.04 LTS</b>

### <b>Python Configure</b>

```sh
$ python2 --version
$ pip2 --version

# install python2, if command python2 not found
$ sudo apt-get install python2 -y
# install pip2, if command pip2 not found
# note: now pip2(python2) and pip3(python3) are not coexist
$ sudo apt-get install python-pip -y

# after install
$ python2 --version
python 2.7.18
$ pip2 --version
pip 20.3.4 from /usr/lib/python2.7/dist-packages/pip (python 2.7)

# NOTE: THE FOLLOWING OPERATIONS ARE OPTIONAL
# use update-alternatives to configure python and pip default commands
# update-alternatives - maintain symbolic links determining default commands

# configure python -> python2 or python3 (optional)
# locate command python2, python3
$ which python2
/usr/bin/python2
$ which python3
/usr/bin/python3
# use update-alternatives to configure command python
$ sudo update-alternatives --config python
update-alternatives: error: no alternatives for python
$ sudo update-alternatives --install /usr/bin/python python /usr/bin/python2 2
$ sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 1
$ sudo update-alternatives --config python
There are 2 choices for the alternative python (providing /usr/bin/python).
  Selection    Path              Priority   Status
------------------------------------------------------------
* 0            /usr/bin/python2   2         auto mode
  1            /usr/bin/python2   2         manual mode
  2            /usr/bin/python3   1         manual mode
Press <enter> to keep the current choice[*], or type selection number: 

# configure pip -> pip2 (optional)
# locate command pip2
$ which pip2
/usr/bin/pip2
# use update-alternatives to configure command pip
$ sudo update-alternatives --config pip
update-alternatives: error: no alternatives for pip
$ sudo update-alternatives --install /usr/bin/pip pip /usr/bin/pip2 2
$ sudo update-alternatives --config pip
There is only one alternative in link group pip (providing /usr/bin/pip): /usr/bin/pip2
Nothing to configure.

# undo update-alternatives python and pip configuration, if need be
$ sudo update-alternatives --remove-all python
$ sudo update-alternatives --remove-all pip

# after install and config
$ python --version
python 2.7.18
$ pip --version
pip 20.3.4 from /usr/lib/python2.7/dist-packages/pip (python 2.7)
```

### <b>Z3 Build and Make</b>

[https://github.com/Z3Prover/z3](https://github.com/Z3Prover/z3)

```sh
$ git clone https://github.com/Z3Prover/z3.git

$ cd z3
$ python3 scripts/mk_make.py  # note: use python3 or python2 (optional)
$ cd build 
$ make
omitting ...
Z3 was successfully built.
Z3Py scripts can already be executed in the 'build/python' directory.
Z3Py scripts stored in arbitrary directories can be executed if the 'build/python' 
directory is added to the PYTHONPATH environment variable and the 'build' directory 
is added to the LD_LIBRARY_PATH environment variable.
Use the following command to install Z3 at prefix /usr.
    sudo make install
$ sudo make install
```

### <b>Tekton Build and Make</b>

[https://github.com/nsg-ethz/tekton](https://github.com/nsg-ethz/tekton)

```sh
$ git clone https://github.com/grapefruit0/tekton.git

$ cd tekton
$ pip2 install -e .  # note: use pip2
```

### <b>SyNet-Plus(NetComplete) Python Dependencies Install</b>

[https://github.com/nsg-ethz/synet-plus](https://github.com/nsg-ethz/synet-plus)

```sh
$ git clone https://github.com/grapefruit0/synet-plus.git

$ cd synet-plus
$ pip2 install -r requirements.txt  # note: use pip2
$ pip2 list
Package             Version       Location
------------------- ------------- ------------------------------------------
boto                2.28.0
contextlib2         0.6.0.post1
decorator           4.4.2
enum34              1.1.10
future              1.0.0
importlib-resources 3.3.1
ipaddress           1.0.23
networkx            2.2
nose                1.3.7
nose-timer          1.0.1
pathlib2            2.3.7.post1
pip                 20.3.4
scandir             1.10.0
setuptools          44.1.1
singledispatch      3.7.0
six                 1.16.0
Tekton              0.1           /PATH-TO/tekton
typing              3.10.0.0
xmltodict           0.12.0
z3-solver           4.8.0.0.post1
zipp                1.2.0
```

### <b>Graphviz Install for Print NetGraph</b>

```sh
$ sudo apt-get install python2-dev  # for python2
$ sudo apt-get install python3-dev  # for python3

$ sudo apt-get install graphviz libgraphviz-dev pkg-config

$ pip2 install pygraphviz
$ pip2 install graphviz
```

### Environment Variable PYTHONPATH Configure

```sh
# use linux /etc/profile.d to configure globals variabls PYTHONPATH
$ cd /etc/profile.d
$ sudo vim pythonpath_synet.sh
$ cat pythonpath_synet.sh
#!/bin/bash

# add ~/codes/synet-plus/synet to $PYTHONPATH

SYNETPATH="${HOME}/.pythonpath-synet"

if [ -z "${PATHONPATH}" ]; then
    export PYTHONPATH="${SYNETPATH}"
fi

if [ -n "${PYTHONPATH##*${SYNETPATH}}" ] && [ -n "${PYTHONPATH##*${SYNETPATH}:*}" ]; then
    export PYTHONPATH="${PYTHONPATH}:${SYNETPATH}"
fi

# use symbolic link to link python directory to this
$ cd ~/.pythonpath-synet
$ ln -n -s /PATH-TO/synet-plus/synet .
$ ln -n -s /PATH-TO/synet-plus/synet/drivers .
$ ln -n -s /PATH-TO/synet-plus/synet/synthesis .
$ ln -n -s /PATH-TO/synet-plus/synet/utils .
```

### <b>Modified File Name and Path</b>

```txt
Python Dependencies Files:
+++ /PATH-TO/python2.7/site-packages/ipaddress.py  (version 1.0.23)

Tekton Files:
+++ /PATH-TO/tekton/tekton/cisco.py
+++ /PATH-TO/tekton/tekton/gns3.py

SyNet-Plus(NetComplete) Files:
+++ /PATH-TO/synet-plus/synet/examples/bgp_peers.py
+++ /PATH-TO/synet-plus/eval_scripts/run-ebgp.sh
```

### <b>Example and Test</b>

#### An Example use of NetComplete

The example at `synet/examples/bgp_peers.py` shows how to use NetComplete to synthesize 
Provider/Customer peering policies.

Running

```sh
$ cd /PATH-TO/synet-plus
$ python2 synet/examples/bgp_peers.py out-configs-simple
omitting ...
=========the example bgp_peers.py finish==========
```

#### Running NSDI Experiments

Running BGP experiments

```sh
$ cd /PATH-TO/synet-plus
# BGP
$ sh eval_scripts/run-ebgp-experiments.sh
waiting one hours ...
# OSPF
$ sh eval_scripts/run-ospf-experiments.sh
waiting one hours ...
```
