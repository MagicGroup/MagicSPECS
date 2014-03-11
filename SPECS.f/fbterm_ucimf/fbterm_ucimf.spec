Summary: Ucimf for fbterm
Summary(zh_CN.UTF-8): Fbterm 的 Ucimf 支持
Name: fbterm_ucimf
Version: 0.2.9
Release: 3%{?dist}
License: GPL+
Group: Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
Source0: http://ucimf.googlecode.com/files/%{name}-%{version}.tar.gz
URL: http://code.google.com/p/ucimf
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: libucimf-devel >= 2.3.7

%description
http://code.google.com/p/ucimf/

%description -l zh_CN.UTF-8
Fbterm 的 Ucimf 支持。

%prep
%setup -q 

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/fbterm_ucimf
%{_mandir}/*

%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 0.2.9-3
- 为 Magic 3.0 重建

* Tue Jul 17 2012 Liu Di <liudidi@gmail.com> - 0.2.9-2
- 为 Magic 3.0 重建

* Mon Nov 11 2011 Liu Di <liudidi@gmail.com> - 0.2.9-1
- 更新到 0.2.9
