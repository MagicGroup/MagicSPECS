#global rcver -rc2

Name:		libgadu
Version: 1.12.1
Release:	5%{?dist}
Summary:	A Gadu-gadu protocol compatible communications library
Summary(zh_CN.UTF-8): Gadu-gadu 协议兼容通信库
License:	LGPLv2
#Source0:	https://github.com/wojtekka/libgadu/releases/download/%{version}%{?rcver}/libgadu-%{version}%{?rcver}.tar.gz
Source0:	https://github.com/wojtekka/%{name}/archive/%{version}.tar.gz
URL:		http://libgadu.net/
BuildRequires:	doxygen
BuildRequires:	gnutls-devel
BuildRequires:	gsm-devel
BuildRequires:	libxml2-devel
BuildRequires:	protobuf-c-devel
BuildRequires:	speex-devel
BuildRequires:	zlib-devel

%description
libgadu is intended to make it easy to add Gadu-Gadu communication
support to your software.

%description -l zh_CN.UTF-8
Gadu-gadu 协议兼容通信库

%package devel
Summary:	Libgadu development library
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	libgadu = %{version}-%{release}
Requires:	pkgconfig

%description devel
The libgadu-devel package contains the header files necessary
to develop applications with libgadu.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package doc
Summary:	Libgadu library developer documentation
Summary(zh_CN.UTF-8): %{name} 的开发文档
Group:		Documentation
Group(zh_CN.UTF-8): 文档
Requires:	libgadu = %{version}-%{release}
BuildArch:	noarch

%description doc
The libgadu-doc package contains the documentation for the
libgadu library.

%description doc -l zh_CN.UTF-8
%{name} 的开发文档。

%prep
%setup -q -n %{name}-%{version}%{?rcver}

%build
if ! [ -f configure ];then ./autogen.sh ;fi
%configure \
	--disable-silent-rules \
	--disable-static \
	--without-openssl \
	--with-pthread

make %{?_smp_mflags}

%install
make install INSTALL="install -p" DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
magic_rpm_clean.sh

%check
make check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING ChangeLog README
%{_libdir}/libgadu.so.*

%files devel
%{_libdir}/libgadu.so
%{_includedir}/libgadu.h
%{_libdir}/pkgconfig/*

%files doc
%doc docs/protocol.html docs/html

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 1.12.1-5
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 1.12.1-4
- 为 Magic 3.0 重建

* Fri Aug 07 2015 Liu Di <liudidi@gmail.com> - 1.12.1-3
- 更新到 1.12.1

* Wed Jul 16 2014 Liu Di <liudidi@gmail.com> - 1.12.0-3
- 为 Magic 3.0 重建

* Wed Jul 16 2014 Liu Di <liudidi@gmail.com> - 1.12.0-2
- 为 Magic 3.0 重建

* Wed May 07 2014 Liu Di <liudidi@gmail.com> - 1.12.0-0.5.rc2
- 为 Magic 3.0 重建

* Wed May 07 2014 Liu Di <liudidi@gmail.com> - 1.12.0-0.4.rc2
- 为 Magic 3.0 重建

* Tue Feb 11 2014 Dominik Mierzejewski <rpm@greysector.net> - 1.12.0-0.3.rc2
- update to 1.12.0-rc2 (fixes CVE-2013-6487)

* Wed Dec 11 2013 Dominik Mierzejewski <rpm@greysector.net> - 1.12.0-0.2.rc1
- update to 1.12.0-rc1
- drop attr from file list

* Wed Nov 06 2013 Dominik Mierzejewski <rpm@greysector.net> - 1.12.0-0.1.20131101git3f1b8ce
- update to 1.12.0 prerelease from git (fixes CVE-2013-4488)
- update Source and URL to new location
- clean up spec file

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.2-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.2-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Sep 04 2012 Dominik Mierzejewski <rpm@greysector.net> 1.11.2-1
- updated to 1.11.2 (bug 782047)
- dropped obsolete patch
- fix build (Dan Winship, bug 851676)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.0-2.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.0-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 12 2011 Dominik Mierzejewski <rpm@greysector.net> 1.11.0-2
- fixed TLS usage via gnutls (rhbz #718619)

* Sat Jun 04 2011 Dominik Mierzejewski <rpm@greysector.net> 1.11.0-1
- updated to 1.11.0
- enabled gsm/speex to support voice connections
- enabled zlib to support GG10 contact list import/export

* Mon Mar 14 2011 Dominik Mierzejewski <rpm@greysector.net> 1.10.1-1
- updated to 1.10.1

* Sun Feb 27 2011 Dominik Mierzejewski <rpm@greysector.net> 1.10.0-1
- updated to 1.10.0 final
- enabled SSL support via gnutls
- added API docs to -doc
- updated summaries and descriptions for -devel

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 15 2010 Dominik Mierzejewski <rpm@greysector.net> 1.9.1-1
- updated to 1.9.1

* Wed May 19 2010 Dominik Mierzejewski <rpm@greysector.net> 1.9.0-1
- updated to 1.9.0 final

* Sun Mar 14 2010 Dominik Mierzejewski <rpm@greysector.net> 1.9.0-0.4.rc3
- updated to 1.9.0-rc3
- adds basic support for new GG protocol (UTF-8 and new status messages)
- full upstream changelog (Polish only) http://toxygen.net/libgadu/releases/1.9.0-rc3.html
- drop Requires: openssl-devel from -devel subpackage

* Sun Dec 06 2009 Dominik Mierzejewski <rpm@greysector.net> 1.9.0-0.3.rc2
- disabled OpenSSL support (not used in practice),
  fixes license trouble for GPL apps

* Sun Dec 06 2009 Dominik Mierzejewski <rpm@greysector.net> 1.9.0-0.2.rc2
- updated to 1.9.0-rc2

* Sun Sep 13 2009 Dominik Mierzejewski <rpm@greysector.net> 1.9.0-0.1.rc1
- updated to 1.9.0-rc1

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.8.2-5
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> 1.8.2-2
- rebuild with new openssl

* Sun Oct 26 2008 Dominik Mierzejewski <rpm@greysector.net> 1.8.2-1
- updated to 1.8.2 (security update)
- preserve timestamps during make install
- put defattr at the top of files section (fixes rpmlint error)

* Wed Jun 18 2008 Dominik Mierzejewski <rpm@greysector.net> 1.8.1-1
- updated to 1.8.1

* Sun Feb 24 2008 Dominik Mierzejewski <rpm@greysector.net> 1.8.0-1
- updated to 1.8.0

* Sat Feb 16 2008 Dominik Mierzejewski <rpm@greysector.net> 1.7.2-1
- updated to 1.7.2

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - 1.7.1-3
 - Rebuild for deps

* Sun Aug 26 2007 Dominik Mierzejewski <rpm@greysector.net> 1.7.1-2
- rebuild for BuildID
- update license tag

* Wed Apr 25 2007 Dominik Mierzejewski <rpm@greysector.net> 1.7.1-1
- updated to 1.7.1 (security fixes)

* Sun Sep 17 2006 Dominik Mierzejewski <rpm@greysector.net> 1.7.0-1
- initial build
