%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary: Creates a common metadata repository
Summary(zh_CN.UTF-8): 建立公用元数据仓库
Name: createrepo
Version: 0.9.9
Release: 2%{?dist}
License: GPLv2
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
Source: %{name}-%{version}.tar.gz
Patch0: ten-changelog-limit.patch
Patch1: createrepo-head.patch
URL: http://createrepo.baseurl.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArchitectures: noarch
Requires: python >= 2.1, rpm-python, rpm >= 4.1.1, libxml2-python
Requires: yum-metadata-parser, yum >= 3.2.20, deltarpm
BuildRequires: python

%description
This utility will generate a common metadata repository from a directory of rpm
packages.

%description -l zh_CN.UTF-8
这个工具会建立 rpm 包的公用元数据仓库。

%prep
%setup -q
%patch0 -p0
%patch1 -p1

%build

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-, root, root,-)
%doc ChangeLog README COPYING
%{_datadir}/%{name}/
%{_bindir}/createrepo
%{_bindir}/modifyrepo
%{_bindir}/mergerepo
%{_mandir}/*/*
%{python_sitelib}/createrepo
/usr/etc/bash_completion.d/createrepo.bash

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.9.9-2
- 为 Magic 3.0 重建


