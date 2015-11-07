%global with_python3 1


Summary:        Python (PyGObject) bindings to the GUDev library
Summary(zh_CN.UTF-8): GUDev 库的 Python 绑定
Name:           python-gudev
URL:            http://github.com/nzjrs/python-gudev

Version:        147.2
Release:        9%{?dist}

%global srcname nzjrs-python-gudev-%{version}-0-ga9f8dd2
%global _dirname nzjrs-python-gudev-ee8a644

# Tar.gz can be downloaded from
# http://github.com/nzjrs/python-gudev/tarball/%{version}
Source0:        %{srcname}.tar.gz
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

%description -l zh_CN.UTF-8
GUDev 库的 Python 绑定。

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
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 147.2-9
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 147.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 147.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 147.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Nov 05 2013 Kyle McMartin <kyle@fedoraproject.org>
- Fix FTBFS when using dirname macro.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 147.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 147.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

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
