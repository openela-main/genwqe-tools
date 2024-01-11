# Copyright 2015, International Business Machines
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# zlib-devel 1.2.8 is better, but 1.2.7 should work too
#
# The following switch tries to take care that the distros libz.so is been taken:
#    CONFIG_ZLIB_PATH=%%{_libdir}/libz.so
# No special libz build should be needed anymore, since we added the right
# dependency to the spec file. We want to have a zlib-devel installed.
# 

Summary: GenWQE userspace tools
Name: genwqe-tools
Version: 4.0.20
Release: 5%{?dist}
License: ASL 2.0
URL: https://github.com/ibm-genwqe/genwqe-user/
BuildRequires: zlib-devel >= 1.2.7
BuildRequires: help2man
%ifarch %{power64}
BuildRequires: libcxl-devel
%endif
Source0: https://github.com/ibm-genwqe/genwqe-user/archive/v%{version}.tar.gz#/genwqe-user-%{version}.tar.gz
Patch0: genwqe-user-4.0.18-install-gzFile_test.patch
Requires: genwqe-zlib = %{version}-%{release}

%description
Provide a suite of utilities to manage and configure the IBM GenWQE card.

%package -n genwqe-zlib
Summary: GenWQE hardware accelerated libz
%description -n genwqe-zlib
GenWQE hardware accelerated libz and test-utilities.

%package -n genwqe-vpd
Summary: GenWQE adapter VPD tools
%description -n genwqe-vpd
The genwqe-vpd package contains GenWQE adapter VPD tools.

%package -n genwqe-zlib-devel
Summary: Development files for %{name}
Requires: genwqe-zlib%{?_isa} = %{version}-%{release}

%description -n genwqe-zlib-devel
The genwqe-zlib-devel package contains libraries and header files for
developing applications that use %{name}.

%package -n genwqe-zlib-static
Summary: Static library files for %{name}
Requires: genwqe-zlib-devel%{?_isa} = %{version}-%{release}

%description -n genwqe-zlib-static
The genwqe-zlib-static package contains static libraries for
developing applications that use %{name}.

%prep
%autosetup -p1 -n genwqe-user-%{version}

%build
LDFLAGS="%{__global_ldflags}" CFLAGS="%{optflags}" make %{?_smp_mflags} tools lib \
 VERSION=%{version} CONFIG_ZLIB_PATH=%{_libdir}/libz.so V=2

%install
make %{?_smp_mflags} install DESTDIR=%{buildroot}/%{_prefix} \
    SYSTEMD_UNIT_DIR=%{buildroot}/%{_unitdir} \
    LIB_INSTALL_PATH=%{buildroot}/%{_libdir}/genwqe \
    INCLUDE_INSTALL_PATH=%{buildroot}/%{_includedir}/genwqe

# move genwqe_vpd.csv to expected location.
mkdir -p %{buildroot}/%{_sysconfdir}/
install -m 0644 tools/genwqe_vpd.csv %{buildroot}/etc/

# remove libz stuff
rm %{buildroot}%{_libdir}/genwqe/libz.*
mv %{buildroot}%{_libdir}/genwqe/* %{buildroot}%{_libdir}/
rmdir %{buildroot}%{_libdir}/genwqe/

%post -n genwqe-zlib -p /sbin/ldconfig
%postun -n genwqe-zlib -p /sbin/ldconfig

%files -n genwqe-tools
%license LICENSE
%{_bindir}/genwqe_echo
%{_bindir}/genwqe_ffdc
%{_bindir}/genwqe_cksum
%{_bindir}/genwqe_memcopy
%{_bindir}/genwqe_peek
%{_bindir}/genwqe_poke
%{_bindir}/genwqe_update

%{_bindir}/genwqe_gunzip
%{_bindir}/genwqe_gzip
%{_bindir}/genwqe_test_gz
%{_bindir}/genwqe_mt_perf
%{_bindir}/zlib_mt_perf
%{_bindir}/gzFile_test

%{_mandir}/man1/genwqe_echo.1*
%{_mandir}/man1/genwqe_ffdc.1*
%{_mandir}/man1/genwqe_gunzip.1*
%{_mandir}/man1/genwqe_gzip.1*
%{_mandir}/man1/genwqe_cksum.1*
%{_mandir}/man1/genwqe_memcopy.1*
%{_mandir}/man1/genwqe_peek.1*
%{_mandir}/man1/genwqe_poke.1*
%{_mandir}/man1/genwqe_update.1*
%{_mandir}/man1/zlib_mt_perf.1*
%{_mandir}/man1/genwqe_test_gz.1*
%{_mandir}/man1/genwqe_mt_perf.1*
%{_mandir}/man1/gzFile_test.1*

%ifarch %{power64}
%{_bindir}/genwqe_maint
%{_bindir}/genwqe_loadtree
/%{_unitdir}/genwqe_maint.service
%{_mandir}/man1/genwqe_maint.1*
%{_mandir}/man1/genwqe_loadtree.1*
%endif

%files -n genwqe-zlib
%license LICENSE
%{_libdir}/*.so.*

%files -n genwqe-vpd
%license LICENSE
%config(noreplace) %{_sysconfdir}/genwqe_vpd.csv
%{_bindir}/genwqe_csv2vpd
%{_bindir}/genwqe_vpdconv
%{_bindir}/genwqe_vpdupdate
%{_mandir}/man1/genwqe_csv2vpd.1*
%{_mandir}/man1/genwqe_vpdconv.1*
%{_mandir}/man1/genwqe_vpdupdate.1*

%files -n genwqe-zlib-devel
%dir %{_includedir}/genwqe
%{_includedir}/genwqe/*
%{_libdir}/*.so

%files -n genwqe-zlib-static
%{_libdir}/*.a

%changelog
* Wed May 23 2018 Than Ngo <than@redhat.com> - 4.0.20-5
- add explicit package version requirement
- fix multilib regression in man pages

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Than Ngo <than@redhat.com> - - 4.0.20-3
- use the Fedora linker flags

* Thu Feb  1 2018 Florian Weimer <fweimer@redhat.com> - 4.0.20-2
- Build with linker flags from redhat-rpm-config

* Mon Jan 15 2018 Dan Horák <dan[at]danny.cz> - 4.0.20-1
- update to 4.0.20 (#1533296)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 13 2017 Than Ngo <than@redhat.com> - 4.0.18-2
- backport upstream to fix compilation on 32-bits arch

* Mon Feb 13 2017 Than Ngo <than@redhat.com> - 4.0.18-1
- update to 4.0.18 prerelease

* Tue Feb 07 2017 Than Ngo <than@redhat.com> - 4.0.17-2
- fix build with RPM_OPT_FLAGS

* Mon Feb 06 2017 Than Ngo <than@redhat.com> - 4.0.17-1
- fixed to build system libcxl on power64
- clean up spec files

* Wed Apr 06 2016 Gabriel Krisman Bertazi <krisman@linux.vnet.ibm.com> - 4.0.16
- dlopen uses SONAME when opening libz.
- Support CAPI version.
- Bulid fixes.
- Include genwqe_maint daemon (CAPI version).

* Mon Apr 04 2016 Frank Haverkamp <haverkam@de.ibm.com>
- Renamed some scripts again

* Thu Feb 04 2016 Frank Haverkamp <haverkam@de.ibm.com>
- Fix s390 and Intel build. Remove debug stuff from zlib rpm.

* Fri Dec 11 2015 Frank Haverkamp <haverkam@de.ibm.com>
- Changing some install directories again.

* Tue Dec 08 2015 Gabriel Krisman Bertazi <krisman@linux.vnet.ibm.com> - 4.0.7-1
- Create Fedora package.
- Make genwqe-vpd and genwqe-libz subpackages of genwqe-tools.

* Wed Apr 22 2015 Frank Haverkamp <haverkam@de.ibm.com>
- Initial release.
