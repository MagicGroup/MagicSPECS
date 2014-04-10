%define git_commit	0a42888

%ifarch alpha ia64 x86_64 ppc64 sparc64 s390x aarch64
%define bits	64
%else
%define bits	32
%endif

Name: freetds
Summary: Implementation of the TDS (Tabular DataStream) protocol
Summary(zh_CN.UTF-8): TDS 协议的实现
Version: 0.91
Release: 11.git%{git_commit}%{?dist}
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License: LGPLv2+ and GPLv2+
URL: http://www.freetds.org/

#  download the latest git source for 0.91 branch from
#   http://gitorious.org/freetds/freetds/archive-tarball/Branch-0_91
#  then
#   mv freetds-freetds-Branch-0_91.tar.gz freetds-%{version}-%{git_commit}.tar.gz
Source0: freetds-%{version}-%{git_commit}.tar.gz

#Source0: ftp://ftp.freetds.org/pub/freetds/stable/freetds-%{version}.tar.bz2
Source1: freetds-tds_sysdep_public.h
Patch1: freetds-0.91-printf.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: unixODBC-devel, readline-devel, gnutls-devel, krb5-devel
BuildRequires: libgcrypt-devel
BuildRequires: libtool
BuildRequires: doxygen, docbook-style-dsssl


%description 
FreeTDS is a project to document and implement the TDS (Tabular
DataStream) protocol. TDS is used by Sybase(TM) and Microsoft(TM) for
client to database server communications. FreeTDS includes call
level interfaces for DB-Lib, CT-Lib, and ODBC.

%description -l zh_CN.UTF-8
TDS 是 Sybase 和微软用于客户端和数据库服务器通信的协议。这是 TDS 
的一个实现，它包含了 DB-Lib, CT-Lib 和 ODBC 的接口。

%package devel
Summary: Header files and development libraries for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files and development libraries
for %{name}. If you like to develop programs using %{name}, you will need
to install %{name}-devel.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package doc
Summary: Development documentation for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Documentation
Group(zh_CN.UTF-8): 文档
BuildArch: noarch

%description doc
This package contains the development documentation for %{name}.
If you like to develop programs using %{name}, you will need to install
%{name}-doc.

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%prep 
%setup -q -n freetds-freetds
#%setup -q
%patch1 -p1

#  correct perl path
sed -i '1 s,#!.*/perl,#!%{__perl},' samples/*.pl

chmod -x samples/*.sh samples/*.pl

find . -name .cvsignore -print | xargs rm -f
find . -name .gitignore -print | xargs rm -f


%build 

export LIBS=-lgcrypt

[ -f configure ] || NOCONFIGURE=yes ./autogen.sh

%configure \
	--disable-dependency-tracking \
	--disable-rpath \
	%{!?_with_static: --disable-static} \
	--with-tdsver="4.2" \
	--with-unixodbc="%{_prefix}" \
	--enable-msdblib \
	--enable-sybase-compat \
	--with-gnutls \
	--enable-krb5

make %{?_smp_mflags} DOCBOOK_DSL="`rpm -ql docbook-style-dsssl | fgrep html/docbook.dsl`"

 
%install 
rm -rf $RPM_BUILD_ROOT

make install DOCDIR=doc/%{name} DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

mv -f $RPM_BUILD_ROOT%{_includedir}/tds_sysdep_public.h \
	$RPM_BUILD_ROOT%{_includedir}/tds_sysdep_public_%{bits}.h
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_includedir}/tds_sysdep_public.h

rm -f samples/Makefile* samples/*.in samples/README

rm -f doc/doc/freetds-%{version}/reference/installdox

mv -f samples/unixodbc.freetds.driver.template \
	samples/unixodbc.freetds.driver.template-%{bits}
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%clean 
rm -rf $RPM_BUILD_ROOT
 

%files 
%defattr(-, root, root, -) 
%{_bindir}/*
%{_libdir}/*.so.*
%config(noreplace) %{_sysconfdir}/*.conf
%doc AUTHORS BUGS COPYING* NEWS README TODO doc/*.html
%doc doc/doc/freetds-%{version}/userguide doc/images
%{_mandir}/*/*

 
%files devel 
%defattr (-, root, root, -) 
%doc samples
%{?_with_static: %{_libdir}/*.a}
%{_libdir}/*.so
%{_includedir}/*


%files doc
%defattr (-, root, root, -) 
%doc doc/doc/freetds-%{version}/reference
%{_docdir}/freetds/* 

%changelog
* Tue Dec  3 2013 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.91-11.git0a42888
- update to the latest git source for 0_91 branch
- fix format-security issue (#1037071)

* Thu Aug 22 2013 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.91-10.git748aa26
- update to the latest git source for 0_91 branch
- fix #999696

* Wed Aug  7 2013 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.91-9.gitb760a89
- update to the latest git source for 0_91 branch
- fix #992295, #993762

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-8.gitf3ae29d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 13 2013 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.91-7.gitf3ae29d
- add aarch64 to the list of 64bit arches (#966129)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-6.gitf3ae29d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov  7 2012 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.91-5.gitf3ae29d
- update to the latest git source for 0_91 branch
- fix #870483

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 27 2012 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.91-3
- Enable Kerberos support (#797276)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 26 2011 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.91-1
- Upgrade to 0.91
- Drop shared-libtds support

* Wed Mar  9 2011 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.82.1-0.3.20110306dev
- update to the latest stable snapshot 0.82.1.dev.20110306
- make build with shared-libtds conditional
- disable shared-libtds patch by default (seems noone uses it for now)

* Mon Feb 14 2011 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.82.1-0.2.20100810dev
- fix again shared-libtds patch to provide increased library version

* Thu Feb 10 2011 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.82.1-0.1.20100810dev
- update to the latest stable snapshot 0.82.1.dev.20100810
- fix shared-libtds patch to provide properly library names

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.82-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.82-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Mar 26 2009 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.82-5
- add upstream patch cspublic.BLK_VERSION_150.patch (#492393)

* Tue Feb 24 2009 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.82-4
- fix autoconf data for libtool2 (patch by Tom Lane <tgl@redhat.com>)

* Fri Jan 30 2009 Karsten Hopp <karsten@redhat.com> 0.82-3
- add s390x to 64 bit archs

* Sun Jan 11 2009 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.82-3
- Use gnutls for SSL (#479148)

* Tue Jun 17 2008 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.82-2
- Continue to provide an internal libtds library as public
  (patch from Hans de Goede, #451021). This shared library is needed
  for some existing applications (libgda etc.), which still use it directly.

* Mon Jun  9 2008 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.82-1
- Upgrade to 0.82

* Tue Feb 26 2008 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-11
- fix "64 or 32 bit" test (#434975)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.64-10
- Autorebuild for GCC 4.3

* Mon Jan 28 2008 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-9
- drop "Obsoletes:" from -doc subpackage to avoid extra complexity.

* Fri Jan 25 2008 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-8
- resolve multiarch conflicts (#341181):
  - split references to separate freetds-doc subpackage
  - add arch-specific suffixes for arch-specific filenames in -devel
  - add wrapper for tds_sysdep_public.h
- add readline support (#430196)

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.64-7
- Rebuild for selinux ppc32 issue.

* Thu Aug 16 2007 Dmitry Butskoy <Dmitry@Butskoy.name>
- Change License tag to "LGPLv2+ and GPLv2+"

* Fri Jun 15 2007 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-6 
- bump release to provide update path over Livna

* Wed Jun 13 2007 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-5
- spec file cleanups
- allowed for Fedora (no patent issues exist), clarification by
  James K. Lowden <jklowden [AT] freetds.org>
- approved for Fedora (review by Hans de Goede <j.w.r.degoede@hhs.nl>)

* Wed Aug  2 2006 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-4
- approved for Livna (review by Hans de Goede <j.w.r.degoede@hhs.nl>)

* Tue Aug  1 2006 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-4
- add patch to fix sed scripts in the doc/ Makefile
- avoid using rpath in binaries
- cleanup in samples/ dir

* Thu Jul 27 2006 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-3
- rebuild userguide too.
- move reference docs to -devel

* Mon Jul 24 2006 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-2
- Properly clear extra executable bit in source
- Regenerate docs using doxygen

* Thu Jul 20 2006 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-1
- Upgrade to 0.64
- Some spec file and distro cleanups

* Tue Sep 20 2005 V.C.G.Yeah <VCGYeah@iname.com> - 0.63-1
- Upgrade to 0.63
- spec file cleanups
- build static libs conditional

* Thu Sep  2 2004 V.C.G.Yeah <VCGYeah@iname.com> - 0.62.4-1Y
- Updated to release 0.62.4.
- Leave includes in system default include dir (needed for php-mssql build)

* Mon May 17 2004 Dag Wieers <dag@wieers.com> - 0.62.3-1
- Updated to release 0.62.3.

* Wed Feb 04 2004 Dag Wieers <dag@wieers.com> - 0.61.2-0
- Added --enable-msdblib configure option. (Dean Mumby)
- Updated to release 0.61.2.

* Fri Jun 13 2003 Dag Wieers <dag@wieers.com> - 0.61-0
- Initial package. (using DAR)
