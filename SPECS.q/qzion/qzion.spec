%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           qzion
Version:        0.4.0
Release:        4%{?dist}
Summary:        An canvas abstraction
Summary(zh_CN.UTF-8): 一个图形抽象层

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        GPLv3+
URL:            http://code.openbossa.org/projects/qzion
Source0:        %{name}-%{version}.tar.gz

Patch0:         qzion-0.4.0-fix_python_install.patch
Patch1:         qzion-0.4.0-fix_char_conversion.patch
#Make configure_file use full path so that qzion.pc can be found correctly.
Patch2:         qzion-0.4.0-fix_configure_paths.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  qt4-devel
BuildRequires:  eet-devel
BuildRequires:  pkgconfig
BuildRequires:  PyQt4-devel
BuildRequires:  cmake
BuildRequires:  python-devel
BuildRequires:  sip-devel

%description
QZion is an canvas abstraction used by and made for QEdje.

%description -l zh_CN.UTF-8
QZion 是用于 QEdje 的图形抽象层。

%package devel
Summary:   Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文件
Group:     Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:  pkgconfig
Requires:  %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name}-devel 软件包包含了使用 %{name} 开发应用程序所需的库和头文件。

%package python
Summary:  Python bindings for %{name}
Summary(zh_CN.UTF-8): %{name} 的 Python 绑定
Group:    Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: PyQt4

%description python
The %{name}-python package contains python bindings for %{name}.

%description python -l zh_CN.UTF-8
%{name}-python 软件包包含了 %{name} 的 Python 绑定。

%package python-devel
Summary:  Python bindings for %{name}
Summary(zh_CN.UTF-8): %{name} 的 Python 绑定
Group:    Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: sip
Requires: PyQt4-devel
Requires: %{name}-python = %{version}-%{release}

%description python-devel
The %{name}-python-devel package contains the development files for
the python bindings for %{name}.

%description python-devel -l zh_CN.UTF-8
%{name}-python-devel 软件包包含了 %{name} 的 Python 绑定的开发文件。

%prep
%setup -q -n %{name}-mainline
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build

mkdir build
cd build
%cmake \
    -DPYTHON_SITE_PACKAGES_DIR=%{python_sitearch} ..

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
cd build
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc README COPYING
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/%{name}.pc

%files python
%defattr(-,root,root,-)
%{python_sitearch}/%{name}

%files python-devel
%defattr(-,root,root,-)
%{_datadir}/sip/%{name}

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.4.0-4
- 为 Magic 3.0 重建

* Tue Jan 31 2012 Liu Di <liudidi@gmail.com> - 0.4.0-3
- 为 Magic 3.0 重建

* Sat May 16 2009 Ni Hui <shuizhuyuanluo@126.com> - 0.4.0-1mgc
- 更新至 0.4.0
- 己丑  四月廿二

* Sat Dec 20 2008 Ni Hui <shuizhuyuanluo@126.com> - 0.3.0-0.1mgc
- 修正 spec 文件
- 戊子  十一月廿三

* Fri Dec 19 2008 John5342 <john5342 at, fedoraproject.org> 0.3.0-1
- Initial package
