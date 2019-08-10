# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dynemol(MakefilePackage):
    """Tools for studying Dynamics of Electrons in Molecules."""

    homepage = 'https://github.com/lgcrego/Dynemol'
    url = 'https://www.github.com/lgcrego/Dynemol/tarball/18d7aa2fcc5b9af174af1a5e313644ac3c77bf6b'

    version('18d7aa2fcc5b9af174af1a5e313644ac3c77bf6b',
            sha256='b60b92a5121225f24f08253a3491446e66f5b56ae3c464c31eb4f9450b426758')

    variant('cuda', default=False,
            description='Enable GPU compute capability')

    # The code uses MPI_Ibcast which was introduced in MPI-3.
    depends_on('mpi@3:')
    depends_on('blas')
    depends_on('lapack')
    depends_on('mkl')

    parallel = False

    def patch(self):
        # Replace obsolete -qopenmp directive wth -fopenmp, otherwise OpenMP
        # compilation is ignored.
        filter_file('-qopenmp', '-fopenmp', 'makefile')

        # Fix upstream issue #6: OpenMP functions cannot be pure.
        filter_file(r'pure (function DP_Moment_component)', r'\1', 'DP_main.f')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('a', prefix.bin.dynemol)
        mkdirp(prefix.share.doc)
        install('manual.pdf', prefix.share.doc)
