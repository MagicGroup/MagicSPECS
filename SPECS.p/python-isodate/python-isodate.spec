%global modulename isodate
%global with_python3 1

Name:           python-%{modulename}
Version:	0.5.4
Release:	1%{?dist}
Summary:        An ISO 8601 date/time/duration parser and formatter
Summary(zh_CN.UTF-8): ISO 8601 日期时间解析器
Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言
License:        BSD
URL:            http://pypi.python.org/pypi/%{modulename}
Source0:        http://pypi.python.org/packages/source/i/%{modulename}/%{modulename}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif # if with_python3

%description
This module implements ISO 8601 date, time and duration parsing. The
implementation follows ISO8601:2004 standard, and implements only date/time
representations mentioned in the standard. If something is not mentioned there,
then it is treated as non existent, and not as an allowed option.

For instance, ISO8601:2004 never mentions 2 digit years. So, it is not intended
by this module to support 2 digit years. (while it may still be valid as ISO
date, because it is not explicitly forbidden.) Another example is, when no time
zone information is given for a time, then it should be interpreted as local
time, and not UTC.

As this module maps ISO 8601 dates/times to standard Python data types, like
date, time, datetime and timedelta, it is not possible to convert all possible
ISO 8601 dates/times. For instance, dates before 0001-01-01 are not allowed by
the Python date and datetime classes. Additionally fractional seconds are
limited to microseconds. That means if the parser finds for instance
nanoseconds it will round it to microseconds.

%description -l zh_CN.UTF-8
ISO 8601 日期时间解析器。

%if 0%{?with_python3}
%package -n python3-%{modulename}
Summary:        An ISO 8601 date/time/duration parser and formatter
Summary(zh_CN.UTF-8): ISO 8601 日期时间解析器
Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言

%description -n python3-%{modulename}
This module implements ISO 8601 date, time and duration parsing. The
implementation follows ISO8601:2004 standard, and implements only date/time
representations mentioned in the standard. If something is not mentioned there,
then it is treated as non existent, and not as an allowed option.

For instance, ISO8601:2004 never mentions 2 digit years. So, it is not intended
by this module to support 2 digit years. (while it may still be valid as ISO
date, because it is not explicitly forbidden.) Another example is, when no time
zone information is given for a time, then it should be interpreted as local
time, and not UTC.

As this module maps ISO 8601 dates/times to standard Python data types, like
date, time, datetime and timedelta, it is not possible to convert all possible
ISO 8601 dates/times. For instance, dates before 0001-01-01 are not allowed by
the Python date and datetime classes. Additionally fractional seconds are
limited to microseconds. That means if the parser finds for instance
nanoseconds it will round it to microseconds.
%description -n python3-%{modulename} -l zh_CN.UTF-8
ISO 8601 日期时间解析器。
%endif

%prep
%setup -qn %{modulename}-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
rm -rf %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd
%endif

%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%check
%{__python2} setup.py test

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif


%files
%defattr(-,root,root,-)
%doc CHANGES.txt README.rst TODO.txt
%{python2_sitelib}/%{modulename}*.egg-info
%{python2_sitelib}/%{modulename}

%if 0%{?with_python3}
%files -n python3-%{modulename}
%doc CHANGES.txt README.rst TODO.txt
%{python3_sitelib}/%{modulename}-*.egg-info
%{python3_sitelib}/%{modulename}
%endif 

%changelog
* Sun Sep 06 2015 Liu Di <liudidi@gmail.com> - 0.5.4-1
- 更新到 0.5.4

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri Apr 18 2014 Dan Scott <dan@coffeecode.net> - 0.5.0-1
- Update to 0.5.0
- Add a Python3 build
- Run unit tests
- Remove python-setuptools-devel BR per https://fedoraproject.org/wiki/Changes/Remove_Python-setuptools-devel

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 26 2012 James Laska <jlaska@redhat.com> - 0.4.7-1
- Update to 0.4.7

* Mon Jan 23 2012 James Laska <jlaska@redhat.com> - 0.4.6-1
- Update to 0.4.6

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Sep 28 2011 James Laska <jlaska@redhat.com> - 0.4.4-1
- Initial package build
