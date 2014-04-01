%{!?python_sitearch:%global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python_inc:%global python_inc %(%{__python} -c "from distutils.sysconfig import get_python_inc; print get_python_inc(1)")}

%define dbus_glib_version 0.70
%define dbus_version 0.90

Summary: D-Bus Python Bindings 
Summary(zh_CN.UTF-8): D-Bus 的 Python 绑定
Name: dbus-python
Version: 1.2.0
Release: 1%{?dist}

License: MIT
URL: http://www.freedesktop.org/software/dbus/
Source0: http://dbus.freedesktop.org/releases/dbus-python/%{name}-%{version}.tar.gz

BuildRequires: dbus-devel >= %{dbus_version}
BuildRequires: dbus-glib-devel >= %{dbus_glib_version}
BuildRequires: python-devel
# for %%check
BuildRequires: dbus-x11 pygobject3

%description
D-Bus python bindings for use with python programs.   

%description -l zh_CN.UTF-8
D-Bus 的 Python 绑定。

%package devel
Summary: Libraries and headers for dbus-python
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and static libraries for hooking up custom mainloops to the dbus python
bindings.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q


%build
%configure

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# unpackaged files
rm -fv $RPM_BUILD_ROOT%{python_sitearch}/*.la
rm -rfv $RPM_BUILD_ROOT%{_datadir}/doc/dbus-python/


%check
make check


%files
%doc COPYING ChangeLog README NEWS
%{python_sitearch}/*.so
%{python_sitelib}/dbus/

%files devel
%doc doc/API_CHANGES.txt doc/HACKING.txt doc/tutorial.txt
%{_includedir}/dbus-1.0/dbus/dbus-python.h
%{_libdir}/pkgconfig/dbus-python.pc


%changelog
* Wed Mar 19 2014 Liu Di <liudidi@gmail.com> - 1.2.0-1
- 更新到 1.2.0

* Tue Aug 07 2012 Rex Dieter <rdieter@fedoraproject.org> 1.1.1-1
- dbus-python-1.1.1 (#800487)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.83.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.83.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.83.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.83.0-7
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.83.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.83.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.83.0-4
- Rebuild for Python 2.6

* Tue Sep 16 2008 Marco Pesenti Gritti - 0.83.0-3
- Add patch for https://bugs.freedesktop.org/show_bug.cgi?id=17551 

* Tue Aug 05 2008  Huang Peng <phuang@redhat.com> - 0.83.0-2
- Update to 0.83.0.

* Wed Jul 16 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.82.4-3
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.82.4-2
- Autorebuild for GCC 4.3

* Sun Jan 20 2008 Matthias Clasen <mclasen@redhat.com> - 0.82.4-1
- Update to 0.82.4

* Mon Oct 22 2007 Matthias Clasen <mclasen@redhat.com> - 0.82.0-3
- Rebuild against new dbus-glib

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.82.0-2
- Rebuild for selinux ppc32 issue.

* Fri Jun 22 2007 Matthias Clasen <mclasen@redhat.com> - 0.82.0-1
- Update to 0.82.0
- Put all docs in the usual place

* Tue Apr 03 2007 David Zeuthen <davidz@redhat.com> - 0.80.2-3
- Rebuild

* Tue Apr 03 2007 David Zeuthen <davidz@redhat.com> - 0.80.2-2
- Don't examine args for functions declared METH_NOARGS (#235017)

* Tue Feb 13 2007 John (J5) Palmieri <johnp@redhat.com> - 0.80.2-1
- upgrade to 0.80.2 which fixes some memleaks

* Wed Jan 24 2007 John (J5) Palmieri <johnp@redhat.com> - 0.80.1-1
- upgrade to 0.80.1
- remove dependency on Pyrex and libxml2
- some API breakage, 
  please see http://dbus.freedesktop.org/doc/dbus-python/NEWS.html
  for notes on changes 

* Wed Jan  3 2007 David Zeuthen <davidz@redhat.com> - 0.70-9%{?dist}
- rebuild against new Pyrex

* Wed Dec  6 2006 Jeremy Katz <katzj@redhat.com> - 0.70-8
- rebuild against python 2.5

* Tue Nov  7 2006 Matthias Clasen <mclasen@redhat.com> - 0.70-7
- Fix a typo in the spec file

* Fri Aug 18 2006 Karsten Hopp <karsten@redhat.com> - 0.70-6
- require libxml2-python for site-packages/dbus/introspect_parser.py

* Thu Jul 20 2006 Jesse Keating <jkeating@redhat.com> - 0.70-5
- Remove unnecessary obsoletes

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.70-4
- Try python_sitearch this time

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.70-3
- Add a BR on dbus-devel

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.70-2
- Spec file cleanups
- Add PKG_CONFIG_PATH

* Mon Jul 17 2006 John (J5) Palmieri <johnp@redhat.com> - 0.70-1
- Initial package import
