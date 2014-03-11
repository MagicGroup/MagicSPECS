%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"
)}

%global oname exif-py

Summary:        Python module to extract EXIF information
Name:           python-exif
# Remember to update setup.py
Version:        1.1.0
Release:        2%{?dist}
License:        BSD
Group:          Development/Libraries
URL:            https://github.com/ianare/exif-py
Source0:        http://downloads.sourceforge.net/exif-py/EXIFpy_%{version}.tar.gz
Source1:        setup.py
Source2:        EXIF
BuildArch:      noarch
BuildRequires:  python-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Python Library to extract EXIF information in digital camera image files

%prep
%setup -q -n EXIFpy_%{version}
%{__cp} %{SOURCE1} .
%{__cp} %{SOURCE2} .
%{__chmod} 0644 EXIF.py
%{__sed} -e "/^# ----- See 'changes.txt'/q" EXIF.py > COPYING
%{__chmod} 0644 COPYING

%build
CFLAGS="%{optflags}" %{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%{__chmod} 0755 %{buildroot}%{python_sitelib}/EXIF.py

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc COPYING README.md changes.txt
%{_bindir}/EXIF
%{python_sitelib}/EXIF*

%changelog
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 03 2012 Terje Rosten <terjeros@phys.ntnu.no> - 1.1.0-1
- 1.1.0

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.0.8-2
- Rebuild for Python 2.6

* Fri Aug 15 2008 Terje Rosten <terjeros@phys.ntnu.no> - 1.0.8-1
- 1.0.8

* Mon Mar  3 2008 Terje Rosten <terjeros@phys.ntnu.no> - 1.0.7-4
- Fix script (bz #435758)

* Mon Feb 11 2008 Terje Rosten <terjeros@phys.ntnu.no> - 1.0.7-3
- add script and changes.txt

* Sat Jan 19 2008 Terje Rosten <terjeros@phys.ntnu.no> - 1.0.7-2
- Improve setup.py

* Thu Jan  3 2008 Terje Rosten <terjeros@phys.ntnu.no> - 1.0.7-1
- 1.0.7
- Include egg info

* Mon Nov 19 2007 Terje Rosten <terjeros@phys.ntnu.no> - 1.0.5-1
- 1.0.5

* Mon Aug 06 2007 Terje Rosten <terjeros@phys.ntnu.no> - 1.0.2-3
- Tagging...

* Mon Aug 06 2007 Terje Rosten <terjeros@phys.ntnu.no> - 1.0.2-2
- Fix typo in url
- Add python-devel to buildreq
- Add license to setup.py
- Strip code from %%doc file
- Fix typo in sitelib macro

* Sat Aug 04 2007 Terje Rosten <terjeros@phys.ntnu.no> - 1.0.2-1
- Initial build

