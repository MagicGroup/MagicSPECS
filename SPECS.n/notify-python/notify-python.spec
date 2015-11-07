%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           notify-python
Version:        0.1.1
Release:        17%{?dist}
Summary:        Python bindings for libnotify
Summary(zh_CN.UTF-8): libnotify 的 Python 绑定

Group:          Development/Languages
Group(zh_CN.UTF-8):	开发/语言
# No version specified, just COPYING.
License:        LGPLv2+
URL:            http://www.galago-project.org/specs/notification
Source0:        http://www.galago-project.org/files/releases/source/notify-python/notify-python-%{version}.tar.gz
Patch0:         notify-python-0.1.1-fix-GTK-symbols.patch
Patch1:         libnotify07.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel, pkgconfig, libnotify-devel, pygtk2-devel
BuildRequires:  gtk2-devel, dbus-devel, dbus-glib-devel

Requires:   libnotify >= 0.4.3
Requires:   notification-daemon

%define pypkgname pynotify

%description
Python bindings for libnotify

%description -l zh_CN.UTF-8
libnotify 的 Python 绑定。

%prep
%setup -q
%patch0 -p1
%patch1 -p1

# WARNING - we touch src/pynotify.override in build because upstream did not rebuild pynotify.c
# from the input definitions, this forces pynotify.c to be regenerated, at some point this can be removed

%build
CFLAGS="$RPM_OPT_FLAGS"
PYTHON=%{__python}
%configure
touch src/pynotify.override
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
# remove unnecessary la file
rm $RPM_BUILD_ROOT/%{python_sitearch}/gtk-2.0/%{pypkgname}/_%{pypkgname}.la

 
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc
%{python_sitearch}/gtk-2.0/%{pypkgname}
%{_datadir}/pygtk/2.0/defs/%{pypkgname}.defs
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 0.1.1-17
- 为 Magic 3.0 重建

* Thu Feb 26 2015 Liu Di <liudidi@gmail.com> - 0.1.1-16
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.1.1-15
- 为 Magic 3.0 重建

* Thu Jan 19 2012 Liu Di <liudidi@gmail.com> - 0.1.1-14
- 为 Magic 3.0 重建

* Thu Nov 03 2011 Liu Di <liudidi@gmail.com> - 0.1.1-13
- 为 Magic 3.0 重建
