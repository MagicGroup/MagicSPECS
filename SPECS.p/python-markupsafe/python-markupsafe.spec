%global with_python3 1

Name: python-markupsafe
Version:	0.23
Release:	1%{?dist}
Summary: Implements a XML/HTML/XHTML Markup safe string for Python
Summary(zh_CN.UTF-8): Python 的 XML/HTML/XHTML 标记安全字符串实现

Group: Development/Languages
Group(zh_CN.UTF-8): 开发/语言
License: BSD
URL: http://pypi.python.org/pypi/MarkupSafe
Source0: http://pypi.python.org/packages/source/M/MarkupSafe/MarkupSafe-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: python-devel python-setuptools-devel

%if 0%{?with_python3}
BuildRequires: python3-devel python3-setuptools
# For /usr/bin/2to3
BuildRequires: python-tools
%endif # if with_python3


%description
A library for safe markup escaping.

%description -l zh_CN.UTF-8
Python 的 XML/HTML/XHTML 标记安全字符串实现。

%if 0%{?with_python3}
%package -n python3-markupsafe
Summary: Implements a XML/HTML/XHTML Markup safe string for Python
Summary(zh_CN.UTF-8): Python3 的 XML/HTML/XHTML 标记安全字符串实现
Group: Development/Languages
Group(zh_CN.UTF-8): 开发/语言

%description -n python3-markupsafe
A library for safe markup escaping.
%description -n python3-markupsafe -l zh_CN.UTF-8
Python3 的 XML/HTML/XHTML 标记安全字符串实现
%endif #if with_python3

%prep
%setup -q -n MarkupSafe-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
2to3 --write --nobackups %{py3dir}
%endif # with_python3

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
popd
%endif # with_python3


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
# C code errantly gets installed
rm $RPM_BUILD_ROOT/%{python_sitearch}/markupsafe/*.c

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{python3_sitearch}/markupsafe/*.c
popd
%endif # with_python3
magic_rpm_clean.sh

%check
%{__python} setup.py test

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif # with_python3

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE README.rst
%{python_sitearch}/*

%if 0%{?with_python3}
%files -n python3-markupsafe
%defattr(-,root,root,-)
%doc AUTHORS LICENSE README.rst
%{python3_sitearch}/*
%endif # with_python3


%changelog
* Tue Sep 08 2015 Liu Di <liudidi@gmail.com> - 0.23-1
- 更新到 0.23

* Tue Jun 17 2014 Liu Di <liudidi@gmail.com> - 0.11-9
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.11-8
- 为 Magic 3.0 重建

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 0.11-7
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 0.11-6
- remove rhel logic from with_python3 conditional

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 29 2010 David Malcolm <dmalcolm@redhat.com> - 0.11-2
- rebuild for newer python3

* Thu Sep 30 2010 Luke Macken <lmacken@redhat.com> - 0.11-1
- Update to 0.11

* Wed Aug 25 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.9.2-5
- rebuild with python3.2
  http://lists.fedoraproject.org/pipermail/devel/2010-August/141368.html

* Fri Jul 23 2010 David Malcolm <dmalcolm@redhat.com> - 0.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jun 24 2010 Kyle VanderBeek <kylev@kylev.com> - 0.9.2-3
- Fix missing setuptools BuildRequires.

* Thu Jun 24 2010 Kyle VanderBeek <kylev@kylev.com> - 0.9.2-2
- Fixed sitearch and python3 definitions to work better with older Fedora/RHEL.

* Wed Jun 23 2010 Kyle VanderBeek <kylev@kylev.com> - 0.9.2-1
- Initial version.
