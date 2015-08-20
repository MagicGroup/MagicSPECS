%global pyname ipaddress

Name:           python-%{pyname}
Version:        1.0.7
Release:        5%{?dist}
Summary:        Port of the python 3.3+ ipaddress module to 2.6+

License:        Python
URL:            https://pypi.python.org/pypi/%{pyname}/%{version}
Source0:        https://pypi.python.org/packages/source/i/%{pyname}/%{pyname}-1.0.7.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel

%description
ipaddress provides the capabilities to create, manipulate and operate
on IPv4 and IPv6 addresses and networks.

The functions and classes in this module make it straightforward to
handle various tasks related to IP addresses, including checking
whether or not two hosts are on the same subnet, iterating over all
hosts in a particular subnet, checking whether or not a string
represents a valid IP address or network definition, and so on.

%prep
%setup -q -n %{pyname}-%{version}


%build
%{__python2} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT


%files
%doc README.txt
%{python2_sitelib}/*


%changelog
* Mon Aug 17 2015 Liu Di <liudidi@gmail.com> - 1.0.7-5
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Nathaniel McCallum <npmccallum@redhat.com> - 1.0.7-3
- Remove Conflicts: python-ipaddr

* Mon Jun  8 2015 Nathaniel McCallum <npmccallum@redhat.com> - 1.0.7-2
- Add Conflicts: python-ipaddr

* Thu May 14 2015 Nathaniel McCallum <npmccallum@redhat.com> - 1.0.7-1
- Update to 1.0.7

* Wed Mar 20 2013 Matt Domsch <mdomsch@fedoraproject.org> - 1.0.3-1
- initial release
