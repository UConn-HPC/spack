# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gf2x(AutotoolsPackage):
    """gf2x is a C/C++ software package containing routines for fast
    arithmetic in GF(2)[x] (multiplication, squaring, GCD) and
    searching for irreducible/primitive trinomials.

    """

    homepage = "https://gforge.inria.fr/projects/gf2x/"
    url      = "https://gitlab.inria.fr/gf2x/gf2x/-/archive/gf2x-1.3.0/gf2x-gf2x-1.3.0.tar.bz2"

    maintainers = ['omsai']

    version('1.3.0', sha256='741694fac29d56edf58b42dc9827c85303090522ccdd1e89c311c6b22c290efa')

    depends_on('autoconf', type='build')

    def autoreconf(self, spec, prefix):
        autoreconf('--install', '--verbose', '--force')
