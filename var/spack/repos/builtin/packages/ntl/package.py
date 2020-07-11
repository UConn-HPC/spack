# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import inspect
import os

from spack import *


class Ntl(AutotoolsPackage):
    """A library for doing numbery theory."""

    homepage = "https://www.shoup.net/ntl/"
    url      = "https://www.shoup.net/ntl/ntl-11.4.3.tar.gz"

    maintainers = ['omsai']

    version('11.4.3', sha256='b7c1ccdc64840e6a24351eb4a1e68887d29974f03073a1941c906562c0b83ad2')

    depends_on('perl', type='build')
    depends_on('gmp')
    depends_on('gf2x')

    build_directory = 'src'

    @property
    def configure_directory(self):
        return os.path.join(self.stage.source_path, 'src')

    def configure(self, spec, prefix):
        options = getattr(self, 'configure_flag_args', [])
        options += ['PREFIX={0}'.format(prefix)]
        with working_dir(self.build_directory, create=True):
            inspect.getmodule(self).configure(*options)
