%define soversion 1
%define soname libdwarf.so.%{soversion}
%define sofullname libdwarf.so.%{soversion}.%{version}.0

Name:          libdwarf
Version: 20150915
Release:       3%{?dist}
Summary:       Library to access the DWARF Debugging file format 
Summary(zh_CN.UTF-8): 访问 DWARF 调试文件格式的库
Group:         Development/Libraries
Group(zh_CN.UTF-8): 开发/库

License:       LGPLv2
URL:           http://www.prevanders.net/dwarf.html
Source0:       http://www.prevanders.net/%{name}-%{version}.tar.gz
Patch0:        libdwarf-shlib.patch

BuildRequires: binutils-devel elfutils-libelf-devel

%package devel
Summary:       Library and header files of libdwarf
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:         Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:       LGPLv2
Requires:      %{name} = %{version}-%{release}

%package static
Summary:       Static libdwarf library
Summary(zh_CN.UTF-8): %{name} 的静态库
Group:         Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:       LGPLv2
Requires:      %{name}-devel = %{version}-%{release}

%package tools
Summary:       Tools for accessing DWARF debugging information
Summary(zh_CN.UTF-8): 访问 DWARF 调试信息的工具
Group:         Development/Tools
Group(zh_CN.UTF-8): 开发/工具
License:       GPLv2
Requires:      %{name} = %{version}-%{release}

%description
Library to access the DWARF debugging file format which supports
source level debugging of a number of procedural languages, such as C, C++,
and Fortran.  Please see http://www.dwarfstd.org for DWARF specification.

%description -l zh_CN.UTF-8
访问 DWARF 调试文件格式的库，支持一些语言的源代码级调试，比如 C, C++, Fortran。

%description static
Static libdwarf library.

%description static -l zh_CN.UTF-8
%{name} 的静态库。

%description devel
Development package containing library and header files of libdwarf.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%description tools
C++ version of dwarfdump (dwarfdump2) command-line utilities 
to access DWARF debug information.

%description tools -l zh_CN.UTF-8
C++ 版本的命令行工具 dwarfdump，用来访问 DWARF 调试信息。

%prep
%setup -q -n dwarf-%{version}
%patch0 -p1 -b .soname

%build
CFLAGS="$RPM_OPT_FLAGS" %configure --enable-shared
LD_LIBRARY_PATH="../libdwarf" make %{?_smp_mflags} SONAME="%{soname}"

%install
install -pDm 0644 libdwarf/dwarf.h         %{buildroot}%{_includedir}/libdwarf/dwarf.h
install -pDm 0644 libdwarf/libdwarf.a      %{buildroot}%{_libdir}/libdwarf.a

install -pDm 0644 libdwarf/libdwarf.h      %{buildroot}%{_includedir}/libdwarf/libdwarf.h
install -pDm 0755 libdwarf/libdwarf.so     %{buildroot}%{_libdir}/%{sofullname}
ln      -s        %{sofullname}            %{buildroot}%{_libdir}/%{soname}
ln      -s        %{sofullname}            %{buildroot}%{_libdir}/libdwarf.so
install -pDm 0755 dwarfdump2/dwarfdump     %{buildroot}%{_bindir}/dwarfdump
magic_rpm_clean.sh

%post -n libdwarf -p /sbin/ldconfig

%postun -n libdwarf -p /sbin/ldconfig

%files
%doc libdwarf/ChangeLog libdwarf/README libdwarf/COPYING libdwarf/LIBDWARFCOPYRIGHT libdwarf/LGPL.txt
%{_libdir}/libdwarf.so.*

%files static
%{_libdir}/libdwarf.a

%files devel
%doc libdwarf/*.pdf
%{_includedir}/libdwarf
%{_libdir}/libdwarf.so

%files tools
%doc dwarfdump2/README dwarfdump2/ChangeLog dwarfdump2/COPYING dwarfdump2/DWARFDUMPCOPYRIGHT dwarfdump2/GPL.txt
%{_bindir}/dwarfdump

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 20150915-3
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 20150915-2
- 更新到 20150915

* Tue Jul 15 2014 Liu Di <liudidi@gmail.com> - 20140519-1
- 更新到 20140519

* Fri Feb  8 2013 Tom Hughes <tom@compton.nu> - 20130207-1
- Update to 20130207 release

* Sun Jan 27 2013 Tom Hughes <tom@compton.nu> - 20130126-1
- Update to 20130126 release
- Revert soname to libdwarf.so.0

* Sat Jan 26 2013 Tom Hughes <tom@compton.nu> - 20130125-1
- Update to 20130125 release
- Bump soname to libdwarf.so.1

* Mon Dec  3 2012 Tom Hughes <tom@compton.nu> - 20121130-1
- Update to 20121130 release

* Thu Nov 29 2012 Tom Hughes <tom@compton.nu> - 20121127-1
- Update to 20121127 release

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120410-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 13 2012 Tom Hughes <tom@compton.nu> - 20120410-1
- Update to 20120410 release
- Drop the 0. from the version - the dates are the upstream versions
- Remove explicit dependencies on elfutils-libelf

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110612-3
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110612-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 13 2011 Parag Nemade <paragn AT fedoraproject DOT org> - 0.20110612-1
- Update to 20110612 release

* Wed Mar 09 2011 Parag Nemade <paragn AT fedoraproject DOT org> - 0.20110113-1
- Update to 20110113 release

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20100629-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 06 2010 Parag Nemade <paragn AT fedoraproject.org> - 0.20100629-1
- Update to 20100629 release
- Add -static subpackage as request in rh#586807

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20090324-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 31 2009 - Suravee Suthikulpanit <suravee.suthikulpanit@amd.com>
- 0.20090324-4
- Adding _smp_mflags for libdwarf build
- Move CFLAGS override from configure to make
 
* Mon Mar 30 2009 - Suravee Suthikulpanit <suravee.suthikulpanit@amd.com>
- 0.20090324-3
- Remove AutoreqProv no

* Thu Mar 26 2009 - Suravee Suthikulpanit <suravee.suthikulpanit@amd.com>
- 0.20090324-2
- Drop the C implementation of dwarfdump. (dwarfdump1)
- Since the doc package is small, we combined the contents into the devel package.
- Fix the version string.
- Drop the static library.
- Add release number to "Requires".
- Fix licensing (v2 instead of v2+)
- Change linking for libdwarf.so and libdwarf.so.0

* Wed Mar 25 2009 - Suravee Suthikulpanit <suravee.suthikulpanit@amd.com>
- 20090324-1
- Initial Revision
