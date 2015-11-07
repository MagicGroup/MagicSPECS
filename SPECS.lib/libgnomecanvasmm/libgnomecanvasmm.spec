Name:           libgnomecanvasmm26
Version:        2.26.0
Release:        7%{?dist}

Summary:        C++ interface for Gnome libs (a GUI library for X)
Summary(zh_CN.UTF-8): Gnome 库的 C++ 接口

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
URL:            http://www.gtkmm.org/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/libgnomecanvasmm/2.26/libgnomecanvasmm-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  gtkmm24-devel >= 2.4.0
BuildRequires:  libgnomecanvas-devel >= 2.6.0

%description
This package provides a C++ interface for GnomeUI.  It is a subpackage
of the gnomemm project.  The interface provides a convenient interface for C++
programmers to create Gnome GUIs with GTK+'s flexible object-oriented
framework.

%description -l zh_CN.UTF-8
Gnome 库的 C++ 接口。

%package devel
Summary:        Headers for developing programs that will use libgnomecanvasmm.
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       gtkmm24-devel
Requires:       libgnomecanvas-devel

%description devel
This package contains the headers that programmers will need to
develop applications which will use libgnomecanvasmm, part of gnomemm
- the C++ interface to the GTK+ GUI library.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n libgnomecanvasmm-%{version}


%build
%configure --disable-static --enable-docs
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} install
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/ldconfig


%postun
/sbin/ldconfig


%files
%defattr(-, root, root, -)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root, -)
%{_includedir}/libgnomecanvasmm-2.6
%{_libdir}/*.so
%{_libdir}/libgnomecanvasmm-2.6
%{_libdir}/pkgconfig/*.pc

%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 2.26.0-7
- 为 Magic 3.0 重建

* Wed Jul 16 2014 Liu Di <liudidi@gmail.com> - 2.26.0-6
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 2.26.0-5
- 为 Magic 3.0 重建

* Sat Jan 07 2012 Liu Di <liudidi@gmail.com> - 2.26.0-4
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr  6 2009 Denis Leroy <denis@poolshark.org> - 2.26.0-1
- Update to upstream 2.26.0

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.23.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Aug 29 2008 Denis Leroy <denis@poolshark.org> - 2.23.1-1
- Update to upstream 2.23.1

* Wed Mar 12 2008 Denis Leroy <denis@dedibox.albator.org> - 2.22.0-1
- Update to upstream 2.22.0

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.20.0-2
- Autorebuild for GCC 4.3

* Mon Sep 17 2007 Denis Leroy <denis@poolshark.org> - 2.20.0-1
- Update to new stable branch 2.20

* Tue Aug 28 2007 Stepan Kasal <skasal@redhat.com> - 2.16.0-3
- Fix typo in description.

* Mon Aug 28 2006 Denis Leroy <denis@poolshark.org> - 2.16.0-2
- FE6 Rebuild

* Mon Aug 21 2006 Denis Leroy <denis@poolshark.org> - 2.16.0-1
- Update to 2.16.0

* Thu Mar 23 2006 Denis Leroy <denis@poolshark.org> - 2.14.0-1
- Update to 2.14.0

* Tue Feb 28 2006 Denis Leroy <denis@poolshark.org> - 2.12.0-3
- Rebuild

* Fri Nov 25 2005 Denis Leroy <denis@poolshark.org> - 2.12.0-2
- Disabled static libraries

* Mon Sep 19 2005 Denis Leroy <denis@poolshark.org> - 2.12.0-1
- Update to 2.12.0

* Thu Apr 28 2005 Denis Leroy <denis@poolshark.org> - 2.10.0-1
- Upgrade to 2.10.0

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Mon Jun 27 2004 Denis Leroy <denis@poolshark.org> - 0:2.6.1-0.fdr.1
- Upgrade to 2.6.1

* Sun Dec 21 2003 Eric Bourque <ericb@computer.org>
- fixed dependency to gtkmm2 instead of gtkmm

* Thu Sep 25 2003 Eric Bourque <ericb@computer.org>
- updated for libgnomecanvasmm-2.0

* Tue Mar 20 2001 Eric Bourque <ericb@computer.org>
- added gnome--.m4 to files devel section

* Sat Mar 10 2001 Herbert Valerio Riedel <hvr@gnu.org>
- improved examples.conf
- fixed example build problems

* Thu May 11 2000 Herbert Valerio Riedel <hvr@gnu.org>
- removed lib/gtkmm from files section
- removed empty obsolete tags

* Sun Jan 30 2000 Karl Einar Nelson <kenelson@sourceforge.net>
- adapted from gtk--.spec
