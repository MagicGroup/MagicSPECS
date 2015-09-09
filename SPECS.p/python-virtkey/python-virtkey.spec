# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           python-virtkey
Version:        0.50
Release:        12%{?dist}
Summary:        Python extension for emulating keypresses and getting current keyboard layout
Summary(zh_CN.UTF-8): 模拟按下键盘和取得当前键盘布局的 Python 扩展

Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言
#missing copy of GPL, licensing info in source file
License:        GPLv2+
URL:            https://launchpad.net/virtkey
Source0:        http://launchpad.net/virtkey/trunk/0.50/+download/%{name}-%{version}.tar.gz
Patch0:         virtkey-gdk-pixbuf-headers.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel, libXtst-devel, gtk2-devel, glib2-devel

%description
Python-virtkey is a python extension for emulating keypresses and getting
current keyboard layout.

%description -l zh_CN.UTF-8
模拟按下键盘和取得当前键盘布局的 Python 扩展。

%prep
%setup -q -c %{name}-%{version} -a0
%patch0 -p1

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
magic_rpm_clean.sh
 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
#no documentation included in upstream tarball
%{python_sitearch}/*


%changelog
* Wed Sep 09 2015 Liu Di <liudidi@gmail.com> - 0.50-12
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.50-11
- 为 Magic 3.0 重建

* Wed Nov 16 2011 Adam Jackson <ajax@redhat.com> 0.50-10
- Rebuild to break bogus libpng dep

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.50-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 27 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.50-8
- Patch to find gdk-pixbuf2 headers

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.50-7
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.50-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.50-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.50-4
- Rebuild for Python 2.6

* Tue May 22 2008 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 0.50-3
- Add patch to fix 64bit build issue, thanks Parag and Ivazquez
* Tue May 06 2008 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 0.50-2
- Add missing glib2-devel build dependency
* Tue May 06 2008 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 0.50-1
- Initial build
