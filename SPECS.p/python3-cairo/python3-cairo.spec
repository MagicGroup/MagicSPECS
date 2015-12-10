%define cairo_version 1.10.2

### Abstract ###

Name: python3-cairo
Version: 1.10.0
Release: 6%{?dist}
License: MPLv1.1 or LGPLv2
Group: Development/Languages
Group(zh_CN.UTF-8): 开发/库
Summary: Python 3 bindings for the cairo library
Summary(zh_CN.UTF-8): cairo 库的 Python3 绑定
URL: http://cairographics.org/pycairo
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Source: http://cairographics.org/releases/pycairo-%{version}.tar.bz2
# Since Python 3.4, pythonX.Y-config is shell script, not Python script,
#  so prevent waf from trying to invoke it as a Python script
Patch0: cairo-waf-use-python-config-as-shell-script.patch
Patch1: pycairo-1.10.0-test-python3.patch

### Build Dependencies ###

BuildRequires: cairo-devel >= %{cairo_version}
BuildRequires: pkgconfig
BuildRequires: python3-devel

%description
Python 3 bindings for the cairo library.

%description -l zh_CN.UTF-8
cairo 库的 Python3 绑定。

%package devel
Summary: Libraries and headers for python3-cairo
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: cairo-devel
Requires: pkgconfig
Requires: python3-devel

%description devel
This package contains files required to build wrappers for cairo add-on
libraries so that they interoperate with python3-cairo.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n pycairo-%{version}

# Ensure that ./waf has created the cached unpacked version
# of the wafadmin source tree.
# This will be created to a subdirectory like
#    .waf3-1.5.18-a7b91e2a913ce55fa6ecdf310df95752
python3 ./waf --version

%patch0 -p0
%patch1 -p1

%build
# FIXME: we should be using the system version of waf (e.g. %{_bindir}/waf)
#        however it is not yet python 3 compatible but should be when 1.6.0
#        is released - https://bugzilla.redhat.com/show_bug.cgi?id=637935 
export CFLAGS="$RPM_OPT_FLAGS"
export PYTHON=python3
python3 ./waf --prefix=%{_usr} \
              --libdir=%{_libdir} \
              configure

python3 ./waf build -v

# remove executable bits from examples
find ./examples/ -type f -print0 | xargs -0 chmod -x

# add executable bit to the _cairo.so library so we strip the debug info:wq

%install
rm -rf $RPM_BUILD_ROOT
DESTDIR=$RPM_BUILD_ROOT python3 ./waf install
# add executable bit to the .so libraries so we strip the debug info
find $RPM_BUILD_ROOT -name '*.so' | xargs chmod +x

find $RPM_BUILD_ROOT -name '*.la' | xargs rm -f
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING* INSTALL NEWS README
%doc examples doc/faq.rst doc/overview.rst doc/README 
%{python3_sitearch}/cairo/

%files devel
%defattr(-,root,root,-)
%doc COPYING*
%{_includedir}/pycairo/py3cairo.h
%{_libdir}/pkgconfig/py3cairo.pc

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.10.0-6
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.10.0-5
- 为 Magic 3.0 重建

* Mon Aug 17 2015 Liu Di <liudidi@gmail.com> - 1.10.0-4
- 为 Magic 3.0 重建

* Wed Jun 18 2014 Liu Di <liudidi@gmail.com> - 1.10.0-3
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.10.0-2
- 为 Magic 3.0 重建

* Thu Aug 18 2011 John (J5) Palmieri <johnp@redhat.com> - 1.10.0-1
- update to upstream 1.10.0

* Thu Feb 10 2011 John (J5) Palmieri <johnp@redhat.com> - 1.8.10-12
- remove cairo_rectangle_int_t patch as it was rejected upstream and is
  no longer needed

* Thu Feb 10 2011 David Malcolm <dmalcolm@redhat.com> - 1.8.10-11
- fix embedded copy of waf so that the package builds against python
3.2 (PEP-3149)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 10 2010 John (J5) Palmieri <johnp@redhat.com> - 1.8.10-9
- add rectangle_int_t wrapper patch which is needed by PyGObject

* Thu Sep 30 2010 John (J5) Palmieri <johnp@redhat.com> - 1.8.10-8
- typo, set CFLAGS to $RPM_OPT_FLAGS not RPM_BUILD_OPTS

* Tue Sep 28 2010 John (J5) Palmieri <johnp@redhat.com> - 1.8.10-7
- add patch to move to using PyCapsule API since PyCObject was removed from 3.2

* Tue Sep 28 2010 John (J5) Palmieri <johnp@redhat.com> - 1.8.10-6
- move defattr above the first file manifest item in the devel sub package 

* Mon Sep 27 2010 John (J5) Palmieri <johnp@redhat.com> - 1.8.10-5
- revert back to using the provided waf script until 
  https://bugzilla.redhat.com/show_bug.cgi?id=637935
  is fixed

* Mon Sep 27 2010 John (J5) Palmieri <johnp@redhat.com> - 1.8.10-4
- add buildreq for waf

* Wed Sep 22 2010 John (J5) Palmieri <johnp@redhat.com> - 1.8.10-3
- Use system waf instead of bundled version (this does not work
  on F13 since the system waf contains syntax which has changed
  in python3)

* Wed Sep 22 2010 John (J5) Palmieri <johnp@redhat.com> - 1.8.10-2
- Fixed up for package review

* Thu Sep 16 2010 John (J5) Palmieri <johnp@redhat.com> - 1.8.10-1
- Initial build.

