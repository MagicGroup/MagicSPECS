%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: Helper scripts for rpm.
Summary(zh_CN.UTF-8): 与 rpm 有关的一些脚本
Name: rpmhelper
URL: http://www.linuxfans.org
Version: 0.03
Release: 5%{?dist}
Source0: %{name}.tar.xz
License: GPL
Group: Application/Tools
Group(zh_CN.UTF-8): 应用程序/工具
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: python

%description
rpmhelper is a set of scripts and libs aimed for ease management of
rpm files.

%description -l zh_CN.UTF-8
rpmhelper 是一组脚本和库，它的目的是为了更容易的管理 rpm 文件。

%prep
%setup -q -n %{name}

%build
make

%install
rm -rf %{buildroot}
python setup.py install --root=${RPM_BUILD_ROOT} --install-lib=%{python_sitearch}
#make DESTDIR=${RPM_BUILD_ROOT} install

magic_rpm_clean.sh
#%find_lang %name

%clean
rm -rf %{buildroot}

#%files -f %{name}.lang
%files
%defattr(-,root,root,-)
%doc README ChangeLog COPYING
%dir %{python_sitearch}/mgcrpmhelper
%{python_sitearch}/mgcrpmhelper
%{python_sitearch}/mgcrpmhelper-0.03-py2.*.egg-info
%{_bindir}/rpm-diff
%{_bindir}/rpm-findold
%{_bindir}/rpm-findnewest
%{_bindir}/rpm-parsespec
%{_bindir}/mb-init
%{_bindir}/mb-prepare
%{_bindir}/mb-build
%{_bindir}/mb-pull-pkg
%{_bindir}/mb-push-pkg
%{_bindir}/mb-fetch-fcpkg

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.03-5
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.03-4
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.03-3
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.03-2
- 为 Magic 3.0 重建

* Sat Feb 04 2012 Liu Di <liudidi@gmail.com> - 0.02-5
- 为 Magic 3.0 重建

* Tue Aug 21 2007 Levin Du <zsdjw@21cn.com> 0.02
- Add mb-init, mb-build, mb-prepare
- Add mb-pull-pkg, mb-push-pkg, mb-fetch-fcpkg
- Add rpm-parsespec
- Rename rpmdiff, rpmfindold to rpm-diff, rpm-findold
- Add rpm-findnewest

* Thu Aug  2 2007 Levin Du <zsdjw@21cn.com> 0.01
- First created.

