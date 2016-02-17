%global with_python3 1

%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$ 
%filter_setup
}

Summary:       Python bindings for libsmbclient API from Samba
Summary(zh_CN.UTF-8): Samba 的 libsmbclient 的 Python 绑定
Name:          python-smbc
Version:	1.0.15.5
Release:	2%{?dist}
URL:           http://cyberelk.net/tim/software/pysmbc/
Source:        http://pypi.python.org/packages/source/p/pysmbc/pysmbc-%{version}.tar.bz2
License:       GPLv2+
Group:         Development/Languages
Group(zh_CN.UTF-8): 开发/语言
BuildRequires: python2-devel
%if 0%{?with_python3}
BuildRequires: python3-devel
%endif
BuildRequires: libsmbclient-devel >= 3.2
BuildRequires: epydoc

%description
This package provides Python bindings for the libsmbclient API
from Samba, known as pysmbc. It was written for use with
system-config-printer, but can be put to other uses as well.

%description -l zh_CN.UTF-8
Samba 的 libsmbclient 的 Python 绑定。

%if 0%{?with_python3}
%package -n python3-smbc
Summary:       Python3 bindings for libsmbclient API from Samba
Summary(zh_CN.UTF-8): Samba 的 libsmbclient 的 Python3 绑定
Group:         Development/Languages
Group(zh_CN.UTF-8): 开发/语言

%description -n python3-smbc
This package provides Python bindings for the libsmbclient API
from Samba, known as pysmbc. It was written for use with
system-config-printer, but can be put to other uses as well.

This is a ported release for python 3
%description -n python3-smbc -l zh_CN.UTF-8
Samba 的 libsmbclient 的 Python3 绑定。
%endif

%package doc
Summary:       Documentation for python-smbc
Summary(zh_CN.UTF-8): %{name} 的文档
Group:         Documentation
Group(zh_CN.UTF-8): 文档

%description doc
Documentation for python-smbc.

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%prep
%setup -q -n pysmbc-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif


%build
CFLAGS="%{optflags}" %{__python} setup.py build
rm -rf html
#epydoc -o html --html build/lib*/smbc.so

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="%{optflags}" %{__python3} setup.py build
popd
%endif


%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
#chmod 755 %{buildroot}%{python3_sitearch}/smbc*.so
popd
%endif

%{__python} setup.py install -O1 --skip-build --root %{buildroot}
#chmod 755 %{buildroot}%{python_sitearch}/smbc.so
magic_rpm_clean.sh

%files
%defattr(-,root,root,-)
%{python_sitearch}/_smbc.so
%{python_sitearch}/smbc/*
%{python_sitearch}/pysmbc*.egg-info

%files doc
%defattr(-,root,root,-)
#%doc html

%if 0%{?with_python3}
%files -n python3-smbc
%defattr(-,root,root,-)
%{python3_sitearch}/_smbc.cpython-3*.so
%{python3_sitearch}/smbc/*
%{python3_sitearch}/pysmbc*.egg-info
%endif


%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.0.15.5-2
- 更新到 1.0.15.5

* Tue Sep 08 2015 Liu Di <liudidi@gmail.com> - 1.0.15.4-1
- 更新到 1.0.15.4

* Tue Jun 17 2014 Liu Di <liudidi@gmail.com> - 1.0.13-7
- 为 Magic 3.0 重建

* Wed Nov 21 2012 Tim Waugh <twaugh@redhat.com> - 1.0.13-6
- Use pkg-config for smbclient include_dirs, fixing rebuild failure.

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 1.0.13-5
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 1.0.13-4
- add with_python3 conditionals

* Thu Jul 26 2012 David Malcolm <dmalcolm@redhat.com> - 1.0.13-3
- generalize file globbing to ease transition to Python 3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 15 2012 Tim Waugh <twaugh@redhat.com> - 1.0.13-1
- 1.0.13.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri May 20 2011 Tim Waugh <twaugh@redhat.com> - 1.0.11-1
- 1.0.11.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 29 2010 David Malcolm <dmalcolm@redhat.com> - 1.0.10-3
- rework python3 DSO name for PEP 3149, and rebuild for newer python3

* Wed Nov 17 2010 Jiri Popelka <jpopelka@redhat.com> - 1.0.10-2
- Fixed rpmlint errors/warnings (#648987)
- doc subpackage

* Mon Nov 01 2010 Jiri Popelka <jpopelka@redhat.com> - 1.0.10-1
- Initial RPM spec file
