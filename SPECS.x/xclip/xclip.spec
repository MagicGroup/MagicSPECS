Name:		xclip
Version:	0.12
Release:	5%{?dist}
License:	GPLv2+
Group:		Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Summary:	Command line clipboard grabber
Summary(zh_CN.UTF-8): 命令行的剪贴板抓取程序
URL:		http://sourceforge.net/projects/xclip
Source0:	http://downloads.sourceforge.net/xclip/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libXmu-devel, libICE-devel, libX11-devel, libXext-devel

%description
xclip is a command line utility that is designed to run on any system with an
X11 implementation. It provides an interface to X selections ("the clipboard")
from the command line. It can read data from standard in or a file and place it
in an X selection for pasting into other X applications. xclip can also print
an X selection to standard out, which can then be redirected to a file or
another program.
%description -l zh_CN.UTF-8
命令行的剪贴板抓取程序。

%prep
%setup -q

%build
%configure
make CDEBUGFLAGS="$RPM_OPT_FLAGS" %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
make DESTDIR=$RPM_BUILD_ROOT install.man
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING README
%{_bindir}/xclip
%{_bindir}/xclip-copyfile
%{_bindir}/xclip-cutfile
%{_bindir}/xclip-pastefile
%{_mandir}/man1/xclip*.1*

%changelog
* Thu Oct 22 2015 Liu Di <liudidi@gmail.com> - 0.12-5
- 为 Magic 3.0 重建

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul  8 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 0.12-1
- update to 0.12

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 16 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 0.11-1
- update to 0.11

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.10-3
- Autorebuild for GCC 4.3

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.10-2
- enable utf8 support by default

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.10-1
- bump to 0.10
- new URL

* Mon Aug 27 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.08-4
- license tag fix
- rebuild for BuildID

* Wed Apr 25 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.08-3
- add extra BR for old FC versions

* Wed Apr 25 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.08-2
- smp_mflags

* Tue Apr 24 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.08-1
- initial package for Fedora Extras
