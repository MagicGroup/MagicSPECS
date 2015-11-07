%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define WITH_SELINUX 0

Name: libuser
Version: 0.62
Release: 2%{?dist}
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
License: LGPLv2+
URL: https://fedorahosted.org/libuser/
Source: https://fedorahosted.org/releases/l/i/libuser/libuser-%{version}.tar.xz
BuildRequires: glib2-devel, linuxdoc-tools, pam-devel, popt-devel, python2-devel
BuildRequires: cyrus-sasl-devel
%if %{WITH_SELINUX}
BuildRequires: libselinux-devel
%endif
BuildRequires: openldap-devel
# To make sure the configure script can find it
BuildRequires: nscd
# For %%check
BuildRequires: openldap-clients, openldap-servers
Summary: A user and group account administration library
Summary(zh_CN.UTF-8): 用户和组账号管理库

%description
The libuser library implements a standardized interface for manipulating
and administering user and group accounts.  The library uses pluggable
back-ends to interface to its data sources.

Sample applications modeled after those included with the shadow password
suite are included.

%description -l zh_CN.UTF-8
用户和组账号管理库。

%package devel
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary: Files needed for developing applications which use libuser
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: glib2-devel%{?_isa}

%description devel
The libuser-devel package contains header files, static libraries, and other
files useful for developing applications with libuser.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package python
Summary: Python bindings for the libuser library
Summary(zh_CN.UTF-8): %{name} 的 Python 绑定
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: libuser%{?_isa} = %{version}-%{release}

%description python
The libuser-python package contains the Python bindings for
the libuser library, which provides a Python API for manipulating and
administering user and group accounts.

%description python -l zh_CN.UTF-8
%{name} 的 Python 绑定。

%prep
%setup -q

%build
%configure \
           %if %{WITH_SELINUX}
	   --with-selinux \
	   %else
	   --without-selinux \
	   %endif
           --with-ldap --with-html-dir=%{_datadir}/gtk-doc/html
make

%clean
rm -fr $RPM_BUILD_ROOT

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
magic_rpm_clean.sh
%find_lang %{name}

%check

make check

# Verify that all python modules load, just in case.
LD_LIBRARY_PATH=$RPM_BUILD_ROOT/%{_libdir}:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH
cd $RPM_BUILD_ROOT/%{python_sitearch}
python -c "import libuser"

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS README TODO docs/*.txt
%config(noreplace) %{_sysconfdir}/libuser.conf

%attr(0755,root,root) %{_bindir}/*
%{_libdir}/*.so.*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so
%attr(0755,root,root) %{_sbindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*

%exclude %{_libdir}/*.la
%exclude %{_libdir}/%{name}/*.la

%files python
%defattr(-,root,root)
%doc python/modules.txt
%{python_sitearch}/*.so
%exclude %{python_sitearch}/*.la

%files devel
%defattr(-,root,root)
%{_includedir}/libuser
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/gtk-doc/html/*

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 0.62-2
- 更新到 0.62

* Fri Aug 01 2014 Liu Di <liudidi@gmail.com> - 0.60-1
- 更新到 0.60

* Fri Aug 01 2014 Liu Di <liudidi@gmail.com> - 0.57.2-2
- 更新到 0.60

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.57.2-2
- 为 Magic 3.0 重建

