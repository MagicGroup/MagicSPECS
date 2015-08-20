%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global debug_package %{nil}

Name:           pyatspi
Version:	2.16.0
Release:	1%{?dist}
Summary:        Python bindings for at-spi
Summary(zh_CN.UTF-8): at-spi 的 Python 绑定

Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言
License:        LGPLv2 and GPLv2
URL:            http://www.linuxfoundation.org/en/AT-SPI_on_D-Bus
#VCS: git:git://git.gnome.org/pyatspi
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://download.gnome.org/sources/pyatspi/%{majorver}/%{name}-%{version}.tar.xz

BuildRequires:  python
BuildRequires:  pygobject3-devel >= 2.90.1

Requires:       at-spi2-core
Requires:       python-xlib
Requires:       gnome-python2-gconf

BuildArch:      noarch

%description
at-spi allows assistive technologies to access GTK-based
applications. Essentially it exposes the internals of applications for
automation, so tools such as screen readers, magnifiers, or even
scripting interfaces can query and interact with GUI controls.

This version of at-spi is a major break from previous versions.
It has been completely rewritten to use D-Bus rather than
ORBIT / CORBA for its transport protocol.

This package includes a python client library for at-spi.

%description -l zh_CN.UTF-8
at-spi 的 Python 绑定。

%prep
%setup -q

%build
%configure --disable-relocate
make


%install
make install DESTDIR=$RPM_BUILD_ROOT
magic_rpm_clean.sh

%files
%doc COPYING COPYING.GPL AUTHORS README
%{python_sitelib}/pyatspi


%changelog
* Wed Aug 12 2015 Liu Di <liudidi@gmail.com> - 2.16.0-1
- 更新到 2.16.0

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 2.2.1-2
- 为 Magic 3.0 重建

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> - 2.2.1-1
- Update to 2.2.1

* Wed Sep 28 2011 Matthias Clasen <mclasen@redhat.com> - 2.2.0-1
- Update to 2.2.0

* Tue Sep 20 2011 Matthias Clasen <mclasen@redhat.com> - 2.1.91-1
- Update to 2.1.91

* Mon Jul 25 2011 Matthias Clasen <mclasen@redhat.com> - 2.1.4-1
- Update to 2.1.4

* Thu Jun 16 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.1.2-1
- Update to 2.1.2

* Wed May 11 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.1.1-1
- Update to 2.1.1

* Tue Apr 26 2011 Matthias Clasen <mclasen@redhat.com> - 2.0.1-1
- Update to 2.0.1

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> - 2.0.0-1
- Update to 2.0.0

* Tue Mar 22 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.92-1
- Update to 1.91.92

* Mon Mar  7 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.91-1
- Update to 1.91.91

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.90-1
- Update to 1.91.90

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.91.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Christopher Aillon <caillon@redhat.com> - 1.91.6-1
- Update to 1.91.6

* Tue Jan 11 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.5-1
- Update to 1.91.5

* Thu Dec  2 2010 Matthias Clasen <mclasen@redhat.com> - 1.91.3-1
- Update to 1.91.3

* Tue Oct  5 2010 Matthias Clasen <mclasen@redhat.com> - 1.91.0-1
- Update to 1.91.0

* Wed Sep 29 2010 Matthias Clasen <mclasen@redhat.com> - 0.4.0-1
- Update to 0.4.0

* Mon Sep 20 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.91-2
- Require python-xlib and and gnome-python2-gconf (#635484)

* Tue Aug 31 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.91-1
- Update to 0.3.91

* Wed Aug 18 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.90-1
- Update to 0.3.90

* Mon Aug  2 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.6-1
- Update to 0.3.6

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jun 29 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.4-1
- Update to 0.3.4

* Tue Jun  8 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.3-1
- Update to 0.3.3

* Fri May 28 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.2-1
- Update to 0.3.2

* Sat May 15 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.1.1-1
- Update to 0.3.1.1

* Tue Mar 30 2010 Matthias Clasen <mclasen@redhat.com> - 0.1.8-1
- Update to 0.1.8

* Sat Feb 20 2010 Matthias Clasen <mclasen@redhat.com> - 0.1.7-1
- Update to 0.1.7

* Wed Feb 10 2010 Tomas Bzatek <tbzatek@redhat.com> - 0.1.6-1
- Update to 0.1.6

* Wed Feb  3 2010 Matthias Clasen <mclasen@redhat.com> - 0.1.5-2
- Relocate

* Sun Jan 16 2010 Matthias Clasen <mclasen@redhat.com> - 0.1.5-1
- Update to 0.1.5

* Thu Jan  7 2010 Matthias Clasen <mclasen@redhat.com> - 0.1.4-3
- Incorporate review feedback

* Thu Jan  7 2010 Matthias Clasen <mclasen@redhat.com> - 0.1.4-2
- Fix License field
- Change CORBA/DBus switching method

* Tue Dec 22 2009 Matthias Clasen <mclasen@redhat.com> - 0.1.4-1
- Update to 0.1.4

* Sat Dec  5 2009 Matthias Clasen <mclasen@redhat.com> - 0.1.3-1
- Initial packaging
