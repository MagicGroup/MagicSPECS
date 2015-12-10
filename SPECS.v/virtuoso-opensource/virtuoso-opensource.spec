
# workaround vad creation fail on ppc,
# http://bugzilla.redhat.com/725347 
%ifarch ppc ppc64
# set to omit demos
%define _disable_all_vads   --disable-all-vads
%endif

Name:    virtuoso-opensource
Epoch:   1
Version: 6.1.6
Release: 4%{?dist}
Summary: A high-performance object-relational SQL database
Summary(zh_CN.UTF-8): 高性能的对象关系型数据库

Group:   Applications/Databases
Group(zh_CN.UTF-8): 应用程序/数据库
# see LICENSE for exception details
License: GPLv2 with exceptions
URL:     http://virtuoso.sourceforge.net/
%if 0%{?snap:1}
Source0: ftp://download.openlinksw.com/support/vos/virtuoso-opensource-6-%{snap}.tar.gz
%else
Source0: http://downloads.sourceforge.net/virtuoso/virtuoso-opensource-%{version}.tar.gz
%endif
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

## Upstreamable patches
Patch52: virtuoso-opensource-6.1.0-nodemos_buildfix.patch
Patch53: virtuoso-opensource-6.1.4-no_strip.patch

## Upstream patches

BuildRequires: automake libtool
BuildRequires: bison
BuildRequires: flex
BuildRequires: gawk
BuildRequires: gperf
BuildRequires: htmldoc
## when/if we ever decide to build and ship .jar's
#BuildRequires: java-devel
BuildRequires: openldap-devel
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(libiodbc)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(zlib)

Provides: virtuoso = %{version}-%{release}

%if 0%{?_disable_all_vads:1}
Obsoletes: virtuoso-opensource-apps < %{version}-%{release} 
Obsoletes: virtuoso-opensource-conductor < %{version}-%{release} 
Obsoletes: virtuoso-opensource-doc < %{version}-%{release} 
%endif

%description
Virtuoso is a scalable cross-platform server that combines SQL/RDF/XML
Data Management with Web Application Server and Web Services Platform
functionality.

%description -l zh_CN.UTF-8
高性能的对象关系型数据库。

%package apps
Summary: Applications
Summary(zh_CN.UTF-8): %{name} 的程序
Group:   Applications/Databases
Group(zh_CN.UTF-8): 应用程序/数据库
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
%description apps 
%{summary}.

%description apps -l zh_CN.UTF-8
%{name} 的程序。

%package conductor
Summary: Server pages 
Summary(zh_CN.UTF-8): %{name} 的服务器页
Group:   Applications/Databases
Group(zh_CN.UTF-8): 应用程序/数据库
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
BuildArch: noarch
%description conductor 
%{summary}.

%description conductor -l zh_CN.UTF-8
%{name} 的服务器页。

%package doc 
Summary: Documentation 
Summary(zh_CN.UTF-8): %{name} 的文档
Group:   Documentation 
Group(zh_CN.UTF-8): 文档
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
BuildArch: noarch
%description doc 
%{summary}.
%description doc -l zh_CN.UTF-8
%{name} 的文档。

%package utils
Summary: Utilities
Summary(zh_CN.UTF-8): %{name} 的工具
Group:   Applications/Databases
Group(zh_CN.UTF-8): 应用程序/数据库
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
%description utils
%{summary}.
%description utils -l zh_CN.UTF-8
%{name} 的工具。

%prep
%setup -q -n virtuoso-opensource-%{!?snap:%{version}}%{?snap:6-%{snap}}

%if 0%{?_disable_all_vads:1}
%patch52 -p1 -b .nodemos_buildfix
%endif
%patch53 -p1 -b .no_strip

# required by both patch52/53
./autogen.sh

find -name "*.jar"
find -name "*.jar" -delete

# hack in links for --with-odbc below
# not sure this is any better than our external_iodbc patch above
mkdir libiodbc
pushd libiodbc
ln -s %(pkg-config --variable includedir libiodbc) include
ln -s %(pkg-config --variable libdir libiodbc) lib
popd


%build
%configure \
  --with-layout=redhat \
  --enable-shared --disable-static \
  --without-internal-zlib \
  --with-iodbc=`pwd`/libiodbc \
  --enable-openssl \
  --disable-imagemagick \
  %{?_disable_all_vads} 

make %{?_smp_mflags}


%install
rm -rf %{buildroot} 

make install DESTDIR=%{buildroot}

# silly that both binaries with internal vs. external libiodbc get built 
mv %{buildroot}%{_bindir}/virtuoso-iodbc-t %{buildroot}%{_bindir}/virtuoso-t

mkdir -p %{buildroot}%{_sysconfdir}/virtuoso
mv %{buildroot}%{_var}/lib/virtuoso/db/virtuoso.ini %{buildroot}%{_sysconfdir}/virtuoso/
ln -s ../../../..%{_sysconfdir}/virtuoso/virtuoso.ini %{buildroot}%{_var}/lib/virtuoso/db/virtuoso.ini

# generic'ish binaries, hide them away safely
pushd %{buildroot}%{_bindir}
# make links to libexecdir relative, be warned ! -- rex
mkdir -p ../libexec/virtuoso/
mv %{buildroot}%{_bindir}/{inifile,isql,isql-iodbc,isqlw,isqlw-iodbc,odbc_mail,virt_mail} \
  ../libexec/virtuoso/
ln -s ../libexec/virtuoso/isql isql-vt
ln -s ../libexec/virtuoso//isql-iodbc isql-iodbc-vt
ln -s ../libexec/virtuoso/isqlw isqlw-vt
ln -s ../libexec/virtuoso/isqlw-iodbc isqlw-iodbc-vt
ln -s ../libexec/virtuoso/odbc_mail odbc_mail-vt
ln -s ../libexec/virtuoso/virt_mail virt_mail-vt
popd

## unpackaged files 
rm -vf %{buildroot}%{_libdir}/*.{la,a}
rm -vf %{buildroot}%{_libdir}/virtuoso/hosting/*.la
%if 0%{?_disable_all_vads:1}
rm -rvf %{buildroot}%{_docdir}/virtuoso/
rm -vf  %{buildroot}%{_libdir}/{hibernate,jdbc-?.?,jena}/*.jar
%endif
rm -rvf %{buildroot}%{_libdir}/sesame
magic_rpm_clean.sh

%check
## these take a very long time
%{?_with_check:make check}


%clean
rm -rf %{buildroot} 


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING CREDITS LICENSE
%doc README.UPGRADE
%dir %{_sysconfdir}/virtuoso/
%config(noreplace) %{_sysconfdir}/virtuoso/virtuoso.ini
%{_bindir}/virtuoso-t
%{_libdir}/virt*.so
%dir %{_datadir}/virtuoso/
%dir %{_datadir}/virtuoso/vad/
%dir %{_libdir}/virtuoso/
%dir %{_libexecdir}/virtuoso/
%dir %{_var}/lib/virtuoso
%{_var}/lib/virtuoso/db/

%if ! 0%{?_disable_all_vads:1}
%files apps
%defattr(-,root,root,-)
%{_libdir}/virtuoso/hosting/
%{_datadir}/virtuoso/vad/*.vad
%exclude %{_datadir}/virtuoso/vad/conductor_dav.vad

%files conductor
%defattr(-,root,root,-)
%{_datadir}/virtuoso/vad/conductor_dav.vad
%{_var}/lib/virtuoso/vsp/

%files doc
%defattr(-,root,root,-)
%{_docdir}/virtuoso/
%endif

%files utils
%defattr(-,root,root,-)
%{_bindir}/*-vt
%{_libexecdir}/virtuoso/*


%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 1:6.1.6-4
- 为 Magic 3.0 重建

* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 1:6.1.6-3
- 为 Magic 3.0 重建

* Sun Oct 18 2015 Liu Di <liudidi@gmail.com> - 1:6.1.6-2
- 为 Magic 3.0 重建

* Sun Oct 18 2015 Liu Di <liudidi@gmail.com> - 1:6.1.6-1
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1:6.1.4-5
- 为 Magic 3.0 重建

* Wed Jan 18 2012 Rex Dieter <rdieter@fedoraproject.org> 1:6.1.4-4
- make proper optimized build 
- -utils: include both normal and iodbc variants
- -utils: include -vt symlinks for compatiblity with opensuse packaging

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:6.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 02 2011 Rex Dieter <rdieter@fedoraproject.org> 6.1.4-2
- --disable-all-vads on ppc/ppc64 to workaround FTBFS (#725347)

* Tue Nov 01 2011 Rex Dieter <rdieter@fedoraproject.org> 6.1.4-1
- 6.1.4

* Tue Oct 11 2011 Rex Dieter <rdieter@fedoraproject.org> 6.1.3-3
- gawk4 patch (#744189)

* Tue Oct 11 2011 Rex Dieter <rdieter@fedoraproject.org> 6.1.3-2.1
- respin, enable 'make check'

* Wed Sep 14 2011 Rex Dieter <rdieter@fedoraproject.org> 6.1.3-2
- upstream patch to fix encoding errors (#728857, kde#271664)

* Fri Jul 08 2011 Rex Dieter <rdieter@fedoraproject.org> 6.1.3-1
- 6.1.3 (final)
- epoch++ (to allow upgrade from f15's 1:6.1.2-3)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.1.3-0.3.rc3.20110105
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Rex Dieter <rdieter@fedoraproject.org> 6.1.3-0.2.rc3.20110105
- don't autogen.sh things by default

* Thu Jan 06 2011 Rex Dieter <rdieter@fedoraproject.org> 6.1.3-0.1.rc3.20110105
- virtuoso-opensource-6-20110105 snapshot

* Thu Oct 21 2010 Pierre-Yves Chibon <pingou@pingoured.fr> 6.1.2-2
- Enable creation subpackage -conductor
- Remove all .jar from sources before building

* Wed Jul 21 2010 Rex Dieter <rdieter@fedoraproject.org> 6.1.2-1
- virtuoso-opensource-6.1.2

* Mon May 10 2010 Rex Dieter <rdieter@fedoraproject.org> 6.1.1-1
- virtuoso-opensource-6.1.1
- Obsoletes: -doc

* Tue Feb 09 2010 Rex Dieter <rdieter@fedoraproject.org> 6.1.0-2
- fix Obsoletes: -apps,-conductor

* Thu Feb 04 2010 Rex Dieter <rdieter@fedoraproject.org> 6.1.0-1
- virtuoso-opensource-6.1.0
- build only what we need for nepomuk, Obsoletes: -apps,-conductor

* Sat Jan 09 2010 Rex Dieter <rdieter@fedoraproject.org> 6.0.0-1
- virtuoso-opensource-6.0.0

* Tue Oct 20 2009 Rex Dieter <rdieter@fedoraproject.org> 5.0.12-1
- virtuoso-opensource-5.0.12

* Sun Oct 11 2009 Rex Dieter <rdieter@fedoraproject.rog> 5.0.12-0.1.rc9.20090916
- virtuoso-opensource-20090916 (5.0.12-rc9)

* Wed Aug 26 2009 Tomas Mraz <tmraz@redhat.com> - 5.0.11-4
- rebuilt with new openssl

* Fri Jul 24 2009 Rex Dieter <rdieter@fedoraproject.org> 5.0.11-3
- BR: htmldoc
- -doc subpkg

* Sun Jun 07 2009 Rex Dieter <rdieter@fedoraproject.org> 5.0.11-2
- omit remaining .la files
- fix %%changelog
- fix virtuoso.ini dangling symlink

* Fri May 22 2009 Rex Dieter <rdieter@fedoraproject.org> 5.0.11-1
- virtuoso-opensource-5.0.11

