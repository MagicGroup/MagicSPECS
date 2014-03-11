%define utempter_compat_ver 0.5.2

Summary: A privileged helper for utmp/wtmp updates
Summary(zh_CN.UTF-8): utmp/wtmp 更新的私有帮助器
Name: libutempter
Version: 1.1.5
Release: 5%{?dist}
License: LGPLv2
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: ftp://ftp.altlinux.org/pub/people/ldv/utempter
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0: ftp://ftp.altlinux.org/pub/people/ldv/utempter/%{name}-%{version}.tar.bz2

Requires(pre): shadow-utils
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

Provides: utempter = %{utempter_compat_ver}
Obsoletes: utempter

%description
This library provides interface for terminal emulators such as
screen and xterm to record user sessions to utmp and wtmp files.

%description -l zh_CN.UTF-8
这个库提供了一个终端模拟器的接口，比如 screen 和 xterm，来记录
用户会话到 utmp 和 wtmp 文件。

%package devel
Summary: Development environment for utempter
Summary(zh_CN.UTF-8): %{name} 的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
This package contains development files required to build
utempter-based software.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
make CFLAGS="$RPM_OPT_FLAGS" libdir="%{_libdir}" libexecdir="%{_libexecdir}"

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR="$RPM_BUILD_ROOT" libdir="%{_libdir}" libexecdir="%{_libexecdir}"

# FIXME: We might need to enable this part for backward compat with the
# Red Hat / Fedora 'utempter' package:
#
# mkdir -p %{_sbindir}
# ln -sf %{helperdir}/utempter %{_sbindir}/utempter


# NOTE: Static lib intentionally disabled.
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%pre
{
    %{_sbindir}/groupadd -g 22 -r -f utmp || :
    %{_sbindir}/groupadd -g 35 -r -f utempter || :
}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README
%{_libdir}/libutempter.so.0
%{_libdir}/libutempter.so.1.1.5
%dir %attr(755,root,utempter) %{_libexecdir}/utempter
%attr(2711,root,utmp) %{_libexecdir}/utempter/utempter
# FIXME: If a symlink is needed for compat here, uncomment the code in the
# install section and this as well:
#%{_sbindir}/utempter

%files devel
%defattr(-,root,root,-)
%{_includedir}/utempter.h
%{_libdir}/libutempter.so

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.1.5-5
- 为 Magic 3.0 重建

* Thu Jan 12 2012 Liu Di <liudidi@gmail.com> - 1.1.5-4
- 为 Magic 3.0 重建


