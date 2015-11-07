%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-which
Version:        1.1.0
Release:        12%{?dist}
Summary:        Small which replacement that can be used as a Python module
Summary(zh_CN.UTF-8): 可以做为 which 替代的 Python 模块

Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言
License:        MIT
URL:            http://trentm.com/projects/which/
Source0:        http://trentm.com/downloads/which/%{version}/which-%{version}.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel

%description
which.py is a small which replacement. It has the following features:

 * it can print all matches on the PATH;
 * it can note "near misses" on the PATH (e.g. files that match but 
   may not, say, have execute permissions); and
 * it can be used as a Python module.

%description -l zh_CN.UTF-8
可以做为 which 替代的 Python 模块。

%prep
%setup -q -n which-%{version}


%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
# add a script that calls the python module
cat << \EOF > which-python
#!/bin/sh
python -m which $@
EOF
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m0755 -p which-python $RPM_BUILD_ROOT%{_bindir}
magic_rpm_clean.sh
 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE.txt README.txt TODO.txt
%{_bindir}/which-python
%{python_sitelib}/which.py*
%{python_sitelib}/which-*.egg-info


%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.1.0-12
- 为 Magic 3.0 重建

* Wed Sep 09 2015 Liu Di <liudidi@gmail.com> - 1.1.0-11
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.1.0-10
- 为 Magic 3.0 重建

* Sun Jan 22 2012 Liu Di <liudidi@gmail.com> - 1.1.0-9
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.1.0-4
- Rebuild for Python 2.6

* Mon Jan  7 2008 Patrice Dumas <pertusus@free.fr> - 1.1.0-3
- ship egg file

* Sun Oct 28 2007  <ndbecker2@gmail.com> - 1.1.0-2
- Remove ref to GNU

* Sat Oct 27 2007  <ndbecker2@gmail.com> - 1.1.0-1
- Package for fedora

* Thu Jul 19 2007 Patrice Dumas <pertusus@free.fr> 1.1.0-1
- initial packaging
