# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from glob import glob

from spack import *


class NcbiToolkit(AutotoolsPackage):
    """NCBI C++ Toolkit"""

    homepage = "https://www.ncbi.nlm.nih.gov/IEB/ToolBox/CPP_DOC/"
    url      = "ftp://ftp.ncbi.nih.gov/toolbox/ncbi_tools++/CURRENT/ncbi_cxx--22_0_0.tar.gz"

    version('22.0.0', 'e352d25b24c3a2d087c2cf3cedf6ea95')
    version('21.0.0', '14e021e08b1a78ac9cde98d0cab92098')
    variant('debug', default=False,
            description='Build debug versions of libs and apps')

    depends_on('boost@1.35.0:')
    depends_on('bzip2')
    depends_on('jpeg')
    depends_on('libpng')
    depends_on('libtiff')
    depends_on('libxml2')
    depends_on('libxslt@1.1.14:')
    depends_on('lzo')
    depends_on('pcre')
    depends_on('giflib')
    depends_on('sqlite@3.6.6:')
    depends_on('zlib')
    depends_on('samtools')
    depends_on('bamtools')

    def url_for_version(self, version):
        version_date = {
            Version('22.0.0'): 'Mar_28_2019',
            Version('21.0.0'): 'Apr_2_2018',
        }
        ftp = 'ftp://ftp.ncbi.nih.gov/toolbox/ncbi_tools++/'
        if version in version_date.keys():
            date = version_date[version]
            year = date[-4:]
            return ftp + ('ARCHIVE/{0}/{1}/ncbi_cxx--{2}.tar.gz'
                          .format(year, date, version.underscored))
        else:
            # Assume the unknown version is the current release.
            return ftp + ('CURRENT/ncbi_cxx--{0}.tar.gz'
                          .format(version.underscored))

    def configure_args(self):
        args = ['--without-sybase', '--without-fastcgi']
        if '+debug' not in self.spec:
            args += ['--without-debug']
        return args

    def patch(self):
        with working_dir(join_path('src', 'util', 'image')):
            filter_file(r'jpeg_start_compress(&cinfo, true)',
                        'jpeg_start_compress(&cinfo, TRUE)',
                        'image_io_jpeg.cpp', string=True)
        # TODO: Convert these substitutions into BOOST_VERSION preprocessor
        # patches to send upstream.
        if self.spec.satisfies('^boost@1.69:'):
            with working_dir(join_path('include', 'corelib')):
                filter_file(r'(boost::unit_test::decorator::collector)',
                            r'\1_t', 'test_boost.hpp')
        if self.spec.satisfies('^boost@1.70:'):
            with working_dir(join_path('include', 'corelib')):
                filter_file(('unit_test::ut_detail::'
                             'ignore_unused_variable_warning'),
                            'ignore_unused', 'test_boost.hpp', string=True)
            with working_dir(join_path('src', 'corelib')):
                for file_ in ['test_boost.cpp', 'teamcity_boost.cpp']:
                    filter_file(
                        r'(void log_build_info\s*\(.*ostream&[^)]*)\);',
                        r'\1, bool log_build_info = true);', file_)
                    filter_file(r'(::log_build_info\(.*ostream.*&[^)]+)\)',
                                r'\1, bool log_build_info)', file_)
                    filter_file(r'(log_build_info\(ostr)\)', r'\1, true)',
                                file_)

    def build(self, spec, prefix):
        with working_dir(join_path(glob(
                '*MT64')[0], 'build')):
            make('all_r')
