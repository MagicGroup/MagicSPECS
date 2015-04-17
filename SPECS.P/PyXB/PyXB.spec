Name:           PyXB
<<<<<<< HEAD
Version:	1.2.4
Release:	1%{?dist}
Summary:        Python XML Schema Bindings
Summary(zh_CN.UTF-8): Python XML Schema 绑定
=======
Version:        1.2.3
Release:        3%{?dist}
Summary:        Python XML Schema Bindings
>>>>>>> 54cb407384ac63300039a28ea6cd00ef0bab6697
License:        Apache
URL:            http://pyxb.sourceforge.net/
Source0:        http://downloads.sourceforge.net/project/pyxb/pyxb/%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python-devel

%description
PyXB (“pixbee”) is a pure Python package that generates Python source
code for classes that correspond to data structures defined by
XMLSchema.

<<<<<<< HEAD
%description -l zh_CN.UTF-8
Python XML Schema 绑定。

=======
>>>>>>> 54cb407384ac63300039a28ea6cd00ef0bab6697
%prep
%setup -q

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
<<<<<<< HEAD
magic_rpm_clean.sh

=======
 
>>>>>>> 54cb407384ac63300039a28ea6cd00ef0bab6697
%files
%doc doc/* LICENSE NOTICE PKG-INFO README.txt examples/*
%{python_sitelib}/*
%{_bindir}/pyx*

%changelog
<<<<<<< HEAD
* Tue Apr 14 2015 Liu Di <liudidi@gmail.com> - 1.2.4-1
- 更新到 1.2.4

=======
>>>>>>> 54cb407384ac63300039a28ea6cd00ef0bab6697
* Wed Aug 13 2014 Liu Di <liudidi@gmail.com> - 1.2.3-3
- 为 Magic 3.0 重建

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
