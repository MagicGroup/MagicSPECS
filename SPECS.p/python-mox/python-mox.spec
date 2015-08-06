%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global upstream_name mox

Name:           python-%{upstream_name}
Version:        0.5.3
Release:        9%{?dist}
Summary:        Mock object framework

Group:          Development/Languages
License:        ASL 2.0
URL:            http://code.google.com/p/pymox
Source0:        http://pypi.python.org/packages/source/m/mox/mox-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel

%description
Mox is a mock object framework for Python based on the Java mock object
framework EasyMock.

%prep
%setup -q -n %{upstream_name}-%{version}
# Fix non-executable-script error
sed -i '/^#!\/usr\/bin\/python2.4$/,+1 d' mox.py
sed -i '/^#!\/usr\/bin\/python2.4$/,+1 d' stubout.py

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%check
%{__python} mox_test.py

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING README
%{python_sitelib}/%{upstream_name}.py*
%{python_sitelib}/stubout.py*
%{python_sitelib}/%{upstream_name}-%{version}*.egg-info

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 26 2010 Silas Sewell <silas@sewell.ch> - 0.5.3-2
- Fix various issues relating to review (shebangs, url, etc..)

* Wed Oct 13 2010 Silas Sewell <silas@sewell.ch> - 0.5.3-1
- Initial package
