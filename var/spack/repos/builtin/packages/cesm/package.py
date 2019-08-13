# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cesm(CMakePackage):
    """Community Earth System Model."""

    homepage = 'http://www.cesm.ucar.edu/'
    url = 'https://github.com/ESCOMP/cesm/archive/release-cesm2.1.1.tar.gz'
    svn = 'https://svn-ccsm-models.cgd.ucar.edu/cesm1/release_tags/cesm1_2_2_1'

    version('2.1.1',
            sha256='e9981d144715c871ecb449f77d835c12f287080e23179b8401920b30d183e79b',
            url='https://github.com/ESCOMP/cesm/archive/release-cesm2.1.1.tar.gz')
    version('1.2.2.1',
            url='https://svn-ccsm-models.cgd.ucar.edu/cesm1/release_tags/cesm1_2_2_1')

    variant('mpi', default=True)
    variant('esmf', default=False)
    variant('trilinos', default=False)

    depends_on('cmake@2.8.6:', type='build')
    depends_on('subversion', type='build')

    depends_on('lapack')
    depends_on('blas')
    depends_on('mpi', when='+mpi')

    # TODO: Add the esmf package.
    # depends_on('esmf@5.2.0:', when='+esmf')
    depends_on('netcdf@4.2: +parallel-netcdf', when='@1')
    depends_on('netcdf@4.3: +parallel-netcdf', when='@2:')
    depends_on('parallel-netcdf@1.2.0:', when='@1')
    depends_on('parallel-netcdf@1.7.0:', when='@2:')
    depends_on('netcdf-fortran@4.2:', when='@1')
    depends_on('netcdf-fortran@4.3:', when='@2:')
    depends_on('trinilinos', when='+trilinos')

    root_cmakelists_dir = 'cime'
    phases = ['bootstrap', 'cmake', 'build', 'install']

    def bootstrap(self, spec, prefix):
        bootstrap = Executable('./manage_externals/checkout_externals')
        bootstrap()

    def cmake_args(self):
        args = [
            '-DNETCDF_C={0}'.format(self.spec['netcdf'].prefix),
            '-DNETCDF_FORTRAN={0}'.format(self.spec['netcdf-fortran'].prefix),
            # TODO: Set Intel fortran compiler for f95?
        ]
        return args
