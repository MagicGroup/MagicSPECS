%{!?python_sitelib_platform: %define python_sitelib_platform %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}


Summary: A fast metadata parser for yum
Summary(zh_CN.UTF-8): yum 使用的快速元数据解析器
Name: yum-metadata-parser
Version: 1.1.4
Release: 7%{?dist}
Source0: http://linux.duke.edu/projects/yum/download/%{name}/%{name}-%{version}.tar.gz
Patch0: BZ-612409-handle-2GB-rpms.patch
License: GPLv2
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL: http://linux.duke.edu/projects/yum/
Conflicts: yum < 3.2.0
BuildRequires: python-devel
BuildRequires: glib2-devel
BuildRequires: libxml2-devel
BuildRequires: sqlite-devel
BuildRequires: pkgconfig
Requires: glib2 >= 2.15
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Fast metadata parser for yum implemented in C.

%description -l zh_CN.UTF-8
yum 使用的快速元数据解析器。

%prep
%setup -q
%patch0 -p1

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --root=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README AUTHORS ChangeLog
%{python_sitelib_platform}/_sqlitecache.so
%{python_sitelib_platform}/sqlitecachec.py
%{python_sitelib_platform}/sqlitecachec.pyc
%{python_sitelib_platform}/sqlitecachec.pyo

%{python_sitelib_platform}/*egg-info

%changelog
* Tue Oct 27 2015 Liu Di <liudidi@gmail.com> - 1.1.4-7
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.1.4-6
- 为 Magic 3.0 重建

