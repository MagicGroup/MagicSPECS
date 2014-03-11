%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%define real_name sexy-python
Name:           python-sexy
Version:        0.1.9
Release:        5%{?dist}

Summary:        Python bindings to libsexy
Summary(zh_CN.UTF-8): libsexy 的 Python 绑定

Group:          System Environment/Libraries
Group(zh_CN.UTF-8):	系统环境/库
License:        LGPL
URL:            http://www.chipx86.com/wiki/Libsexy
Source0:        http://releases.chipx86.com/libsexy/sexy-python/sexy-python-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libsexy-devel >= 0.1.10
BuildRequires:  python-devel >= 2
BuildRequires:  pygtk2-devel >= 2.8.0
BuildRequires:  libxml2-devel
Requires:  libsexy >= 0.1.10

%description
sexy-python is a set of Python bindings around libsexy.

%description -l zh_CN.UTF-8
sexy-python 是 libsexy 的 Python 绑定。

%prep
%setup -q -n  %{real_name}-%{version}

%build
%configure --enable-docs
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} install
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT



%files
%defattr(-, root, root, -)
%doc AUTHORS COPYING ChangeLog NEWS README
%{python_sitearch}/gtk-2.0/sexy.so
%{_datadir}/pygtk/2.0/defs/sexy.defs



%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.1.9-5
- 为 Magic 3.0 重建

* Sun Jan 22 2012 Liu Di <liudidi@gmail.com> - 0.1.9-4
- 为 Magic 3.0 重建

* Sun May 31 2008 Liu Di <liudidi@gmail.com> - 0.1.9-2mgc
- 重新为 magic 打包。
