Summary: Python serial port access library
Summary(zh_CN.UTF-8): Python 的串口访问库
Name: pyserial
Version: 2.7
Release: 5%{?dist}
Source0: http://easynews.dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
License: Python
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
URL: http://pyserial.sourceforge.net
BuildRequires: python-devel
BuildRequires: python3-devel
BuildArch: noarch

%description
This module encapsulates the access for the serial port. It provides backends
for standard Python running on Windows, Linux, BSD (possibly any POSIX
compilant system) and Jython. The module named "serial" automaticaly selects
the appropriate backend.

%description -l zh_CN.UTF-8
Python 的串口访问库。

%package -n python3-pyserial
Summary: Python serial port access library
Summary(zh_CN.UTF-8):  Python 的串口访问库（Python3 版本）

%description -n python3-pyserial
This module encapsulates the access for the serial port. It provides backends
for standard Python running on Windows, Linux, BSD (possibly any POSIX
compilant system) and Jython. The module named "serial" automaticaly selects
the appropriate backend.

%description -n python3-pyserial -l zh_CN.UTF-8
Python 的串口访问库（Python3 版本）。

%prep
export UNZIP="-aa"
%setup -q
rm -rf %{py3dir}
cp -a . %{py3dir}

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python2} setup.py build
pushd %{py3dir}
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
popd

%install
rm -rf $RPM_BUILD_ROOT
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc LICENSE.txt CHANGES.txt README.txt examples
%{python_sitelib}/*
%{_bindir}/miniterm.py

%files -n python3-pyserial
%doc LICENSE.txt CHANGES.txt README.txt examples
%{python3_sitelib}/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 2.7-5
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 2.7-4
- 为 Magic 3.0 重建

* Mon Aug 17 2015 Liu Di <liudidi@gmail.com> - 2.7-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Mar 08 2015 Paul Komkoff <i@stingr.net> 2.7-1
- new upstream version

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 2.6-8
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sat Sep 07 2013 Till Maas <opensource@till.name> - 2.6-7
- Add python3 package

* Sat Sep 07 2013 Paul P. Komkoff <i@stingr.net> - 2.6-6
- patched to allow arbitrary speeds bz#982368

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 28 2011 Paul P. Komkoff Jr <i@stingr.net> - 2.6-1
- new upstream version.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 19 2010 Paul P. Komkoff Jr <i@stingr.net> - 2.5-1
- new upstream version

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Oct 18 2009 Paul P Komkoff Jr <i@stingr.net> - 2.4-1
- new upstream version

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.2-7
- Rebuild for Python 2.6

* Fri Aug 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.2-6
- fix license tag

* Tue Dec 12 2006 Paul P. Komkoff Jr <i@stingr.net>
- rebuilt

* Mon Nov  6 2006 Paul P Komkoff Jr <i@stingr.net> - 2.2-4
- remove "export libdirname"

* Tue Oct 24 2006 Paul P Komkoff Jr <i@stingr.net> - 2.2-3
- Minor specfile fixes

* Sat Oct 14 2006 Paul P Komkoff Jr <i@stingr.net> - 2.2-2
- Minor specfile fixes

* Tue May  9 2006 Paul P Komkoff Jr <i@stingr.net> - 2.2-1
- Fedora Extras submission
