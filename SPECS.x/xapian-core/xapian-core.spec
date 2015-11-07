Name:          xapian-core
Version:	1.2.21
Release:	3%{?dist}
Summary:       The Xapian Probabilistic Information Retrieval Library
Summary(zh_CN.UTF-8):  Xapian 概率信息检索库

Group:         Applications/Databases
Group(zh_CN.UTF-8): 应用程序/数据库
License:       GPLv2+
URL:           http://www.xapian.org/
Source0:       http://www.oligarchy.co.uk/xapian/%{version}/%{name}-%{version}.tar.xz

BuildRequires: zlib-devel
BuildRequires: libuuid-devel
Requires:      %{name}-libs = %{version}-%{release}

%description
Xapian is an Open Source Probabilistic Information Retrieval Library. It
offers a highly adaptable toolkit that allows developers to easily add advanced
indexing and search facilities to applications

%description -l zh_CN.UTF-8
Xapian 概率信息检索库。

%package libs
Summary:       Xapian search engine libraries
Summary(zh_CN.UTF-8): %{name} 的运行库
Group:         System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description libs
Xapian is an Open Source Probabilistic Information Retrieval framework. It
offers a highly adaptable toolkit that allows developers to easily add advanced
indexing and search facilities to applications. This package provides the
libraries for applications using Xapian functionality

%description libs -l zh_CN.UTF-8
%{name} 的运行库。

%package devel
Group:         Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary:       Files needed for building packages which use Xapian
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:      %{name} = %{version}-%{release}
Requires:      %{name}-libs = %{version}-%{release}

%description devel
Xapian is an Open Source Probabilistic Information Retrieval framework. It
offers a highly adaptable toolkit that allows developers to easily add advanced
indexing and search facilities to applications. This package provides the
files needed for building packages which use Xapian

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
# Disable SSE on x86, but leave it intact for x86_64
%ifarch x86_64
%configure --disable-static
%else
%configure --disable-static --disable-sse
%endif

# Remove rpath as per https://fedoraproject.org/wiki/Packaging/Guidelines#Beware_of_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot} INSTALL='install -p'

# Remove libtool archives
# find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Remove the dev docs, we pick them up below
rm -rf %{buildroot}%{_datadir}/doc/%{name}
magic_rpm_clean.sh

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-, root, root)
%{_bindir}/xapian*
%{_bindir}/quest
%{_bindir}/delve
%{_bindir}/copydatabase
%{_bindir}/simpleindex
%{_bindir}/simplesearch
%{_bindir}/simpleexpand
# man pages may be gzipped, hence the trailing wildcard.
%{_mandir}/man1/xapian*
%{_mandir}/man1/quest.1*
%{_mandir}/man1/delve.1*
%{_mandir}/man1/copydatabase.1*

%files libs
%defattr(-, root, root)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/libxapian.so.*

%files devel
%defattr(-, root, root)
%doc HACKING PLATFORMS docs/*html docs/apidoc docs/*pdf
%{_bindir}/xapian-config
%{_includedir}/xapian
%{_includedir}/xapian.h
%{_libdir}/libxapian.so
%{_libdir}/libxapian.la
%{_libdir}/cmake/xapian
%{_libdir}/pkgconfig/xapian-core.pc
%{_datadir}/aclocal/xapian.m4
# man pages may be gzipped, hence the trailing wildcard.
%{_mandir}/man1/xapian-config.1*

%changelog
* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 1.2.21-3
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1.2.21-2
- 为 Magic 3.0 重建

* Wed Oct 21 2015 Liu Di <liudidi@gmail.com> - 1.2.21-1
- 更新到 1.2.21

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.2.12-3
- 为 Magic 3.0 重建

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul  4 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.12-1
- Update to 1.2.12

* Sun Apr 29 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.9-1
- Update to 1.2.9

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-2
- Rebuilt for c++ ABI breakage

* Sat Jan 21 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.8-1
- Update to 1.2.8

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 18 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.7-1
- Update to 1.2.7

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 16 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.4-1
- Update to 1.2.4

* Mon Aug 30 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.3-1
- Update to 1.2.3

* Thu Aug  5 2010 Adel Gadllah <adel.gadllah@gmail.com> - 1.2.2-5
- Reenable SSE on x86_64

* Thu Aug  5 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.2-4
- Disable SSE instructions by default

* Wed Jul 14 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.2-3
- And remove non spec cut-n-paste issue

* Wed Jul 14 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.2-2
- Add cmake stuff

* Wed Jul 14 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.2-1
- Update to 1.2.2

* Fri May  7 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.0-4
- Move license to libs package, a few other spc cleanups

* Fri May  7 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.0-3
- Add the libtool archive (temporarily) to fix build of bindings

* Sat May  1 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.0-2
- Upload new source 

* Sat May  1 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0

* Sun Mar 21 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.18-1
- Update to 1.0.18

* Wed Dec  2 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.17-1
- Update to 1.0.17

* Sun Sep 19 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.16-1
- Update to 1.0.16, some spec file cleanups

* Thu Aug 27 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.15-1
- Update to 1.0.15

* Wed Jul 29 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.14-1
- Update to 1.0.14

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun  5 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.13-1
- Update to 1.0.13

* Sun Apr 12 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.12-1
- Update to 1.0.12

* Mon Apr 06 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.11-1
- Update to 1.0.11

* Wed Mar 04 2009 Caolán McNamara <caolanm@redhat.com> - 1.0.9-4
- include stdio.h for rename, fix bare #elif, EOF -> -1 for getopt

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 05 2008 Adel Gadllah <adel.gadllah@gmail.com> 1.0.9-2
- Fix build

* Sat Nov 29 2008 Adel Gadllah <adel.gadllah@gmail.com> 1.0.9-1
- Update to 1.0.9

* Sat Oct 11 2008 Adel Gadllah <adel.gadllah@gmail.com> 1.0.8-1
- Update to 1.0.8

* Sun Jul 20 2008 Adel Gadllah <adel.gadllah@gmail.com> 1.0.7-1
- Update to 1.0.7

* Sun Mar 30 2008 Adel Gadllah <adel.gadllah@gmail.com> 1.0.6-1
- Update to 1.0.6

* Sat Feb 09 2008 Adel Gadllah <adel.gadllah@gmail.com> 1.0.5-2
- Rebuild for gcc-4.3

* Thu Dec 27 2007 Adel Gadllah <adel.gadllah@gmail.com> 1.0.5-1
- Update to 1.0.5

* Tue Oct 30 2007 Adel Gadllah <adel.gadllah@gmail.com> 1.0.4-1
- Update to 1.0.4

* Fri Oct 25 2007 Adel Gadllah <adel.gadllah@gmail.com> 1.0.2-7
- Fix up multilib patch

* Thu Oct 25 2007 Adel Gadllah <adel.gadllah@gmail.com> 1.0.2-6
- Fix multilib conflict in devel package (RH #343471)

* Tue Aug 21 2007 Adel Gadllah <adel.gadllah@gmail.com> 1.0.2-5
- Rebuild for BuildID and ppc32 bug

* Wed Aug 08 2007 Adel Gadllah <adel.gadllah@gmail.com> 1.0.2-4
- Add disttag

* Wed Aug 08 2007 Adel Gadllah <adel.gadllah@gmail.com> 1.0.2-3
- Bump to avoid tag conflict

* Wed Aug 08 2007 Adel Gadllah <adel.gadllah@gmail.com> 1.0.2-2
- Add missing files
- Minor cleanups

* Wed Aug 08 2007 Adel Gadllah <adel.gadllah@gmail.com> 1.0.2-1
- Update to 1.0.2
- Fix License tag

* Sat Jun 16 2007 Marco Pesenti Gritti <mpg@redhat.com> 1.0.1-1
- Update to 1.0.1

* Tue May  8 2007 Marco Pesenti Gritti <mpg@redhat.com> 0.9.10-2.2.svn8397
- Initial build
