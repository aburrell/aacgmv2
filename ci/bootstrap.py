#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os
import sys

if __name__ == "__main__":
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print("Project path: {0}".format(base_path))
    env_path = os.path.join(base_path, ".tox", "bootstrap")
    if sys.platform == "win32":
        bin_path = os.path.join(env_path, "Scripts")
    else:
        bin_path = os.path.join(env_path, "bin")
    if not os.path.exists(env_path):
        import subprocess
        print("Making bootstrap env in: {0} ...".format(env_path))
        try:
            subprocess.check_call(["virtualenv", env_path])
        except Exception:
            subprocess.check_call([sys.executable, "-m", "virtualenv",
                                   env_path])
        print("Installing `jinja2` and `matrix` into bootstrap environment ...")
        subprocess.check_call([os.path.join(bin_path, "pip"), "install",
                               "jinja2", "matrix"])
    activate = os.path.join(bin_path, "activate_this.py")
    exec(compile(open(activate, "rb").read(), activate, "exec"),
         dict(__file__=activate))

    import jinja2
    import matrix

    jinja = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.join(base_path, "ci",
                                                    "templates")),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True
    )
    tox_envs = {}
    for (alias, conf) in matrix.from_file(os.path.join(base_path,
                                                       "setup.cfg")).items():
        python = conf["python_versions"]
        #deps = conf["dependencies"]
        if "coverage_flags" in conf:
            cover = {"false": False,
                     "true": True}[conf["coverage_flags"].lower()]
        if "environment_variables" in conf:
            env_vars = conf["environment_variables"]

        tox_envs[alias] = {
            "python": "python" + python if "py" not in python else python,
            #"deps": deps.split(),
        }
        if "coverage_flags" in conf:
            tox_envs[alias].update(cover=cover)
        if "environment_variables" in conf:
            tox_envs[alias].update(env_vars=env_vars.split())

    for name in os.listdir(os.path.join("ci", "templates")):
        with open(os.path.join(base_path, name), "w") as fh:
            fh.write(jinja.get_template(name).render(tox_environments=tox_envs))
        print("Wrote {}".format(name))
    print("DONE.")
