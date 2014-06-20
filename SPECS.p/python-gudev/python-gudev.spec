%if 0%{?fedora} > 12 || 0%{?rhel} > 6
%global with_python3 1
%else
%{!?python_sitearch: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib(1))")}
%endif


Summary:        Python (PyGObject) bindings to the GUDev library
Name:           python-gudev
URL:            http://github.com/nzjrs/python-gudev

Version:        147.2
Release:        4%{?dist}

%global _srcname nzjrs-python-gudev-%{version}-0-ga9f8dd2
%global _dirname nzjrs-python-gudev-ee8a644

# Tar.gz can be downloaded from
# http://github.com/nzjrs/python-gudev/tarball/%{version}
Source0:        %{_srcname}.tar.gz
Group:          Development/Libraries
License:        LGPLv3+
Requires:       libgudev1 >= 147
Requires:       pygobject2
BuildRequires:  python-devel
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  libgudev1-devel >= 147
BuildRequires:  pygobject2-devel

%description
python-gudev is a Python (PyGObject) binding to the GUDev UDEV library.

%prep
%setup -q -n %{_dirname}

%build
sh autogen.sh --prefix %{_prefix} --disable-static
make %{?_smp_mflags} CFLAGS="%{optflags}"

%install
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -name gudev.la | xargs rm
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc COPYING README NEWS
%doc test.py
%{python_sitearch}/*
%{_datadir}/*

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 147.2-4
- 为 Magic 3.0 重建

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 147.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 147.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 147.2-1
- Update to latest upstream

* Thu Jul 21 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 147.1-7
- Added upstream patch
- Resolves: rhbz#637084,rhbz#723795
- Related: rhbz#631789

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 147.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 147.1-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Mar 15 2010 Miroslav Suchý <msuchy@redhat.com> 147.1-4
- 572609 - do not strip all debuginfo

* Mon Feb  8 2010 Miroslav Suchý <msuchy@redhat.com> 147.1-3
- initial release
