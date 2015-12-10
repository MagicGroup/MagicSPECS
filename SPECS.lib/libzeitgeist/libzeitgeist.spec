Name:           libzeitgeist
Version:        0.3.18
Release:        6%{?dist}
Summary:        Client library for applications that want to interact with the Zeitgeist daemon
Summary(zh_CN.UTF-8): 与 Zeitgeist 服务交互的程序所需要的客户端库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv3 and GPLv3
URL:            https://launchpad.net/libzeitgeist
Source0:        http://launchpad.net/%{name}/0.3/%{version}/+download/%{name}-%{version}.tar.gz
Patch0:         %{name}-disable-log-test.patch

BuildRequires:  glib2-devel%{?_isa} >= 2.26
BuildRequires:  gtk-doc

Requires:  zeitgeist

%description
This project provides a client library for applications that want to interact
with the Zeitgeist daemon. The library is written in C using glib and provides
an asynchronous GObject oriented API.

%description -l zh_CN.UTF-8
与 Zeitgeist 服务交互的程序所需要的客户端库。

%package        devel
Summary:        Development files for %{name}%{?_isa}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch0 -p1


%build
%configure --disable-static
make V=1 %{?_smp_mflags}


%check
make check


%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
install -d -p -m 755 %{buildroot}%{_datadir}/vala/vapi
install -D -p -m 644 bindings/zeitgeist-1.0.{vapi,deps} %{buildroot}%{_datadir}/vala/vapi
find %{buildroot} -name '*.la' -exec rm -f {} ';'

# remove duplicate documentation
rm -fr %{buildroot}%{_defaultdocdir}/%{name}
magic_rpm_clean.sh

%post -p /usr/sbin/ldconfig

%postun -p /usr/sbin/ldconfig


%files
%defattr(-,root,root,-)

# documentation
%doc COPYING COPYING.GPL README

# essential
%{_libdir}/*.so.*


%files devel
%defattr(-,root,root,-)

# Documentation
%doc AUTHORS ChangeLog COPYING COPYING.GPL MAINTAINERS NEWS 
%doc examples/*.vala examples/*.c
%{_datadir}/gtk-doc/html/zeitgeist-1.0/

# essential
%{_includedir}/zeitgeist-1.0/
%{_libdir}/pkgconfig/zeitgeist-1.0.pc
%{_libdir}/*.so

# extra
%{_datadir}/vala/vapi/


%changelog
* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 0.3.18-6
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 0.3.18-5
- 为 Magic 3.0 重建

* Fri Aug 08 2014 Liu Di <liudidi@gmail.com> - 0.3.18-4
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.3.18-3
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat May 5 2012 Renich Bon Ciric <renich@woralelandia.com> - 0.3.18-1
- Updated to version 0.3.18.
- Disabled a log test since it's failing because no libzeitgeist daemon is present at build time.
- Added missing Result Type constant (*CurrentUri and *EventOrigin).
- Now async functions fail instead of lingering indefinitely if Zeitgeist isn't available.

* Mon Mar 19 2012 Renich Bon Ciric <renich@woralelandia.com> - 0.3.14-1
- Updated to version 0.3.14
- Update to shared-desktop-ontologies-0.8
- Return relevancies of events when searching index
- Update the ZeitgeistEvent and ZeitgeistSubject with event origin and subject current uri
- Zeitgeist isn't autostarted after it disappears
- Removed log-fix patch

* Wed Apr 06 2011 Renich Bon Ciric <renich@woralelandia.com> - 0.3.10-1
- Updated to version 0.3.10
- Fixed bugs:
    https://bugs.launchpad.net/ubuntu/+source/libzeitgeist/+bug/742438
- Renamed log fix patch to something more appropriate

* Sat Apr 02 2011 Renich Bon Ciric <renich@woralelandia.com> - 0.3.6-4
- Added -p to install statements (forgot some)
- Moved README to the main package from devel

* Fri Mar 25 2011 Renich Bon Ciric <renich@woralelandia.com> - 0.3.6-3
- Removed Rubys geo2 dependency since is not needed; it's provided by glibc-devel

* Thu Mar 24 2011 Renich Bon Ciric <renich@woralelandia.com> - 0.3.6-2
- Log test failure repaired by patch from Mamoru Tasaka

* Mon Mar 21 2011 Renich Bon Ciric <renich@woralelandia.com> - 0.3.6-1
- Updated to 0.3.6
- Implemented the isa macro for the devel subpackage.
- Eliminated the doc macro from gtk-doc since it gets marked automatically

* Sat Mar 12 2011 Renich Bon Ciric <renich@woralelandia.com> - 0.3.4-3
- Removed mistaken isa macro from zeitgeist require

* Thu Mar 10 2011 Renich Bon Ciric <renich@woralelandia.com> - 0.3.4-2
- Cleaned up old stuff (BuildRoot, Clean and stuff of sorts)
    https://fedoraproject.org/wiki/Packaging/Guidelines#BuildRoot_tag
    https://fedoraproject.org/wiki/Packaging/Guidelines#.25clean
- Added glib2-devel and gtk-doc as a BuildRequires
- Added GPLv3 since it covers the documentation examples
- Updated Requires to use the new arch specification macro when accordingly
    https://fedoraproject.org/wiki/Packaging/Guidelines#Requires
- Configured install to preserve timestamps
- Added V=1 to the make flags for more verbosity on build
- Added a check section
- Removed disable-module from configure statement since it's not needed anymore: 
    https://bugs.launchpad.net/libzeitgeist/+bug/683805

* Thu Feb 24 2011 Renich Bon Ciric <renich@woralelandia.com> - 0.3.4-1
- updated to latest version

* Sun Feb 06 2011 Renich Bon Ciric <renich@woralelandia.com> - 0.3.2-3
- got rid of INSTALL from docs
- got rid ot dorcdir and used doc to include html docs

* Sat Feb 05 2011 Renich Bon Ciric <renich@woralelandia.com> - 0.3.2-2
- removed duplicate documentation
- added the use of macros for everything; including source and build dir.
- revised path syntax

* Thu Jan 27 2011 - Renich Bon Ciric <renich@woralelandia.com> - 0.3.2-1
- First buildName:           libzeitgeist
