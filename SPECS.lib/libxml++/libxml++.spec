%global 	api_ver 2.6
# first two digits of version
%define release_version %(echo %{version} | awk -F. '{print $1"."$2}')

Name:           libxml++
Version:	2.91.2
Release: 2%{?dist}
Summary:        C++ wrapper for the libxml2 XML parser library
Summary(zh_CN.UTF-8): libxml2 XML 解析库的 C++ 接口

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
URL:            http://libxmlplusplus.sourceforge.net/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/libxml++/%{release_version}/libxml++-%{version}.tar.xz

BuildRequires:  libxml2-devel >= 2.6.1
BuildRequires:  glibmm24-devel >= 2.4.0

%description
libxml++ is a C++ wrapper for the libxml2 XML parser library. It's original
author is Ari Johnson and it is currently maintained by Christophe de Vienne
and Murray Cumming.

%description -l zh_CN.UTF-8
libxml2 XML 解析库的 C++ 接口。

%package devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       libxml2-devel
Requires:       glibmm24-devel

%description devel
This package contains the headers and libraries for libxml++ development.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package        doc
Summary:        Documentation for %{name}, includes full API docs
Summary(zh_CN.UTF-8): %{name} 的文档
Group:          Documentation
Group(zh_CN.UTF-8): 文档
BuildArch:      noarch
BuildRequires:  doxygen, graphviz
Requires:       %{name} = %{version}-%{release}
Requires:       glibmm24-doc

%description    doc
This package contains the full API documentation for %{name}.

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%prep
%setup -q
sed -i s'#\r##' examples/dom_parser/example_with_namespace.xml

%build
# examples are now enabled by default
%configure --disable-static --enable-examples=yes
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name "*.la" -o -name '*.a' | xargs rm -f
# fix wrong base path in devhelp index file
sed -i "s#$RPM_BUILD_ROOT##g" \
    $RPM_BUILD_ROOT%{_datadir}/devhelp/books/%{name}-%{api_ver}/%{name}-%{api_ver}.devhelp2
magic_rpm_clean.sh

%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%doc AUTHORS COPYING NEWS README ChangeLog
%{_libdir}/*.so.*


%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_libdir}/%{name}-%{api_ver}


%files doc
%doc %{_datadir}/devhelp/books/%{name}-%{api_ver}
%doc %{_docdir}/%{name}-%{api_ver}


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 2.91.2-2
- 更新到 2.91.2

* Fri Aug 08 2014 Liu Di <liudidi@gmail.com> - 2.37.1-1
- 更新到 2.37.1

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 2.34.2-3
- 为 Magic 3.0 重建

* Thu Jan 12 2012 Liu Di <liudidi@gmail.com> - 2.34.2-2
- 为 Magic 3.0 重建

* Wed Sep 07 2011 Kalev Lember <kalevlember@gmail.com> - 2.34.2-1
- Update to 2.34.2

* Tue Jun 14 2011 Kalev Lember <kalev@smartlink.ee> - 2.34.1-1
- Update to 2.34.1
- Dropped upstreamed patches
- Require base package from -doc subpackage
- Clean up the spec file for modern rpmbuild

* Fri Jun 10 2011 Karsten Hopp <karsten@redhat.com> 2.33.2-2
- buildrequire mm-common for doc-install.pl
- fix configure and aclocal to check for mm-common-util before trying glibmm-2.4

* Tue Feb 22 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 2.33.2-1
- Update to upstream 2.33.2
- split doc into sub-package

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.33.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 22 2010 Haïkel Guémar <hguemar@fedoraproject.org> - 2.33.1-1
- Update to upstream 2.33.1

* Fri Nov 05 2010 Haïkel Guémar <hguemar@fedoraproject.org> - 2.32.0-1
- Update to upstream 2.32.0

* Thu Sep 30 2010 Haïkel Guémar <hguemar@fedoraproject.org> - 2.30.1-1
- Update to upstream 2.30.1

* Fri Apr 09 2010 Haïkel Guémar <hguemar@fedoraproject.org> - 2.30.0-1
- Update to upstream 2.30.0

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 12 2009 Denis Leroy <denis@poolshark.org> - 2.26.0-1
- Update to upstream 2.26.0 (to match Gnome release)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 15 2009 Denis Leroy <denis@poolshark.org> - 2.24.2-1
- Update to 2.24.2 (memleak fixes)
- Fixed Gnome FTP URL

* Fri Aug 29 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 2.23.2-2
- Include unowned directories

* Tue Aug  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.23.2-1
- update to 2.23.2

* Tue May 13 2008 Denis Leroy <denis@poolshark.org>
- Removed unneeded example binaries from devel package

* Thu Mar 13 2008 Denis Leroy <denis@poolshark.org> - 2.22.0-1
- Update to upstream 2.22.0
- GCC 4.3 patch upstreamed

* Sun Feb 17 2008 Denis Leroy <denis@poolshark.org> - 2.20.0-2
- Added patch for gcc 4.3 rebuild

* Thu Sep 20 2007 Denis Leroy <denis@poolshark.org> - 2.20.0-1
- Update to new 2.20 stable branch

* Thu Aug 16 2007 Denis Leroy <denis@poolshark.org> - 2.18.2-2
- Update to upstream 2.18.2 (mem leak fix)
- Fixed License tag

* Wed Jul 25 2007 Jesse Keating <jkeating@redhat.com> - 2.18.1-2
- Rebuild for RH #249435

* Tue Jul 24 2007 Denis Leroy <denis@poolshark.org> - 2.18.1-1
- Update to version 2.18.1

* Sun Sep 03 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 2.14.0-1.1
- FC6 rebuild

* Tue May 02 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 2.14.0-1
- Version 2.14.0

* Mon Feb 13 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 2.12.0-2.1
- FC5 Rebuild

* Thu Jan 26 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 2.12.0-2
- Rebuilt to address RH #178592

* Thu Sep 08 2005 Konstantin Ryabitsev <icon@linux.duke.edu> - 2.12.0-1
- Version 2.12.0
- Use --disable-static for configure.

* Thu Jul 21 2005 Konstantin Ryabitsev <icon@linux.duke.edu> - 2.10.0-1
- Version 2.10.0
- Rearrange and conform to new FE standards
- Buildrequire glibmm24-devel
- Add devel requires to -devel

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 0.26.0-5
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Tue Nov 04 2003 Panu Matilainen <pmatilai@welho.com> - 0:0:26.0-0.fdr.3
- remove empty .libs directories

* Mon Nov  3 2003 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.26.0-0.fdr.2
- buildrequires graphviz
- devel package requires main package and pkgconfig
- own %%_includedir/libxml++-1.0
- clean up examples tree

* Tue Oct 21 2003 Panu Matilainen <pmatilai@welho.com>
- Initial Fedora packaging

