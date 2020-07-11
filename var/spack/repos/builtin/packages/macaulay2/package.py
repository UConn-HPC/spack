# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class Macaulay2(AutotoolsPackage):
    """A system for computing in commutative algebra, algebraic geometry and
    related fields."""

    homepage = "http://macaulay2.com/"
    git      = "https://github.com/Macaulay2/M2.git"

    maintainers = ['omsai']

    version('master', branch='master')
    # version('1.15', branch='version-1.15')

    depends_on('autoconf', type='build')
    # depends_on('automake', type='build')
    # depends_on('libtool',  type='build')
    # depends_on('m4',       type='build')

    depends_on('eigen')
    depends_on('boost')

    @property
    def configure_directory(self):
        return os.path.join(self.stage.source_path, 'M2')

    def autoreconf(self, spec, prefix):
        with working_dir(self.configure_directory):
            autoreconf('--install', '--verbose', '--force')

    def configure_args(self):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
