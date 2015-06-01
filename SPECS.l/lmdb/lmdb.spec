Name:           lmdb
Version:        0.9.14
Release:        2%{?dist}
Summary:        Memory-mapped key-value database
Summary(zh_CN.UTF-8): 内存映射的键-值数据库

License:        OpenLDAP
URL:            http://symas.com/mdb/
# Source built from git. To get the tarball, execute following commands:
# $ export VERSION=%%{version}
# $ git clone git://gitorious.org/mdb/mdb.git lmdb && pushd lmdb
# $ git checkout tags/LMDB_$VERSION && popd
# $ tar cvzf lmdb-$VERSION.tar.gz -C lmdb/libraries/ liblmdb
Source:        %{name}-%{version}.tar.gz
# Patch description in the corresponding file
Patch0: lmdb-make.patch
Patch1: lmdb-s390-check.patch

BuildRequires: doxygen

%description
LMDB is an ultra-fast, ultra-compact key-value embedded data
store developed by for the OpenLDAP Project. By using memory-mapped files,
it provides the read performance of a pure in-memory database while still 
offering the persistence of standard disk-based databases, and is only limited
to the size of the virtual address space.

%description -l zh_CN.UTF-8
内存映射的键-值数据库。

%package        libs
Summary:        Shared libraries for %{name}
Summary(zh_CN.UTF-8): %{name} 的运行库

%description    libs
The %{name}-libs package contains shared libraries necessary for running
applications that use %{name}.

%description libs -l zh_CN.UTF-8
%{name} 的运行库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package        doc
Summary:        Documentation files for %{name}
Summary(zh_CN.UTF-8): %{name} 的文档
BuildArch:      noarch
Group:          Documentation

%description    doc
The %{name}-doc package contains automatically generated documentation for %{name}.

%description doc -l zh_CN.UTF-8
%{name} 的文档。
%prep
%setup -q -n lib%{name}
%patch0 -p1 -b .make
%patch1 -p1 -b .s390-check


%build
make XCFLAGS="%{optflags}" %{?_smp_mflags}
# Build doxygen documentation
doxygen
# remove unpackaged files
rm -f Doxyfile
rm -rf man # Doxygen generated manpages

%install
# make install expects existing directory tree
mkdir -m 0755 -p %{buildroot}%{_prefix}{/bin,/include}
mkdir -m 0755 -p %{buildroot}{%{_libdir},%{_mandir}/man1}
make DESTDIR=%{buildroot} prefix=%{_prefix} libprefix=%{_libdir} manprefix=%{_mandir} install
magic_rpm_clean.sh

%check
rm -rf testdb
LD_LIBRARY_PATH=$PWD make test

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%{_bindir}/*
%{_mandir}/man1/*

%files libs
%doc COPYRIGHT CHANGES LICENSE
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/*.so

%files doc
%doc html COPYRIGHT CHANGES LICENSE


%changelog
* Thu Apr 16 2015 Liu Di <liudidi@gmail.com> - 0.9.14-2
- 为 Magic 3.0 重建

* Thu Dec 11 2014 Jan Staněk <jstanek@redhat.com> - 0.9.14-1
- Updated to 0.9.14

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Jan Stanek <jstanek@redhat.com> - 0.9.13-1
- Updated to 0.9.13

* Mon Jul 14 2014 Jan Stanek <jstanek@redhat.com> - 0.9.11-4
- Changed install instruction to be compatible with older coreutils (#1119084)

* Thu Jun 26 2014 Jan Stanek <jstanek@redhat.com> - 0.9.11-3
- Added delay in testing which was needed on s390* arches (#1104232)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Jan Stanek <jstanek@redhat.com> - 0.9.11-1
- Initial Package
