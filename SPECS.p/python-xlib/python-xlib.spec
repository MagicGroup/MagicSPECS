# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define pre_release rc1 
Name:           python-xlib
Version:        0.15
Release:        0.10.%{pre_release}%{?dist}
Summary:        X client library for Python
Summary(zh_CN.UTF-8): Python 下的 X 客户端库

Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言
License:        GPLv2+
URL:            http://python-xlib.sourceforge.net/
Source0:        http://prdownloads.sourceforge.net/python-xlib/python-xlib-%{version}%{pre_release}.tar.gz
Source1:        defs 
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Patch0:         increase-receiving-buffer
Patch1:         fix-unix-socket-in-display
Patch2:         fix-ssh-tunnel-auth 
Patch3:         fix-rhomboid-examples 
Patch4:         python-xlib-0.15rc1-xauthority.patch
Patch5:         r138-mggr-get-rid-of-annoying-Xlib.protocol.request.Query.patch
Patch6:         r139-allow-IPv6-addresses-e.g.-d-Xlib.display.Display-fff.patch
# Fix perl usage
# https://sourceforge.net/p/python-xlib/bugs/41/
Patch7:         python-xlib-perl.patch
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  texinfo-tex tetex-dvips

%package doc
Summary:        Documentation and examples for python-xlib
Summary(zh_CN.UTF-8): %{name} 的文档
Group:          Documentation
Group(zh_CN.UTF-8): 文档
Requires:       %{name} = %{version}-%{release}


%description
The Python X Library is a complete X11R6 client-side implementation, 
written in pure Python. It can be used to write low-levelish X Windows 
client applications in Python.

%description -l zh_CN.UTF-8
Python 下的 X 客户端库。

%description doc
Install this package if you want the developers' documentation and examples
that tell you how to program with python-xlib.

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%prep
%setup -q -n %{name}-%{version}%{pre_release}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p0
%patch5 -p2
%patch6 -p2
%patch7 -p1

%build
%{__python} setup.py build
cp %{SOURCE1} doc/src/ 
cd doc
#make html ps
cd html
rm Makefile texi2html

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
chmod a-x examples/*.py
 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README COPYING
# For noarch packages: sitelib
%{python_sitelib}/*

%files doc
%defattr(-,root,root,-)
%doc COPYING examples


%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.15-0.10.rc1
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.15-0.9.rc1
- 为 Magic 3.0 重建

* Wed Sep 09 2015 Liu Di <liudidi@gmail.com> - 0.15-0.8.rc1
- 为 Magic 3.0 重建

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-0.7.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-0.6.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Jun 04 2011 Luke Macken <lmacken@redhat.com> - 0.15-0.5.rc1
- Apply a couple of patches from upstream:
    * r139 - Accept IPv6 addresses in Xlib.display.Display
    * r138 - Remove a stray print statement

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-0.4.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Sep  3 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.15-0.3.rc1
- try a workaround proposed by upstream for #552491

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.15-0.2.rc1
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Dec 14  2009 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.15-0.1.rc1
- New upstream pre-release and some cherry picked patches from Debian from Fedora bug 537264 

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.14-3
- Rebuild for Python 2.6

* Wed Sep  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.14-2
- fix license tag

* Tue Jul 1 2008 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.14-1
- Latest upstream release

* Tue Apr 10 2007 Jef Spaleta <jspaleta@gmail.com> - 0.13-3
- Created doc subpackage per suggestion in review

* Mon Mar 26 2007 Jef Spaleta <jspaleta@gmail.com> - 0.13-2
- Review Cleanup

* Sat Mar 24 2007 Jef Spaleta <jspaleta@gmail.com> - 0.13-1
- Initial packaging

