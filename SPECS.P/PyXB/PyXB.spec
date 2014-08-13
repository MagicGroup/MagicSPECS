Name:           PyXB
Version:        1.2.3
Release:        2%{?dist}
Summary:        Python XML Schema Bindings
License:        Apache
URL:            http://pyxb.sourceforge.net/
Source0:        http://downloads.sourceforge.net/project/pyxb/pyxb/%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python-devel

%description
PyXB (“pixbee”) is a pure Python package that generates Python source
code for classes that correspond to data structures defined by
XMLSchema.

%prep
%setup -q

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
 
%files
%doc doc/* LICENSE NOTICE PKG-INFO README.txt examples/*
%{python_sitelib}/*
%{_bindir}/pyx*

%changelog
* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 25 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2.3-1
- Update to upstream version 1.2.3
- Resolves: rhbz#1086133

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Mar 16 2011 Marek Mahut <mmahut@fedoraproject.org> - 1.1.2-1
- Initial build
