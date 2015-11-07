Summary: A compact getty program for virtual consoles only
Summary(zh_CN.UTF-8): 虚拟终端使用的紧凑 getty 程序
Name: mingetty
Version: 1.08
License: GPLv2+
Release: 11%{?dist}
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
BuildRoot: %{_tmppath}/%{name}-root
URL: http://sourceforge.net/projects/mingetty/
Source: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0: mingetty-1.00-opt.patch
# Bug #635412
Patch1: mingetty-1.08-check_chroot_chdir_nice.patch
Patch2: mingetty-1.08-openlog_authpriv.patch
# Bug #551754
Patch3: mingetty-1.08-limit_tty_length.patch
# Bug #647143
Patch4: mingetty-1.08-Allow-login-name-up-to-LOGIN_NAME_MAX-length.patch

%description
The mingetty program is a lightweight, minimalist getty program for
use only on virtual consoles.  Mingetty is not suitable for serial
lines (you should use the mgetty program in that case).

%description -l zh_CN.UTF-8
虚拟终端使用的紧凑 getty 程序。

%prep
%setup -q
%patch0 -p1 -b .opt
%patch1 -p1 -b .chroot
%patch2 -p1 -b .openlog
%patch3 -p1 -b .tty_length
%patch4 -p1 -b .loginname_length

%build
make "RPM_OPTS=$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{%{_sbindir},%{_mandir}/man8}

install -m 0755 mingetty $RPM_BUILD_ROOT%{_sbindir}/
install -m 0644 mingetty.8 $RPM_BUILD_ROOT/%{_mandir}/man8/

magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING
%{_sbindir}/mingetty
%{_mandir}/man8/mingetty.*

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.08-11
- 为 Magic 3.0 重建

* Wed Sep 17 2014 Liu Di <liudidi@gmail.com> - 1.08-10
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.08-9
- 为 Magic 3.0 重建

* Fri Apr 20 2012 Liu Di <liudidi@gmail.com> - 1.08-8
- 为 Magic 3.0 重建

* Mon Jan 16 2012 Liu Di <liudidi@gmail.com> - 1.08-7
- 为 Magic 3.0 重建

