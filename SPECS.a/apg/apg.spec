Summary:		Automated Password Generator for random password generation
Summary(zh_CN.UTF-8):	产生随机密码的自动密码生成器
Name:			apg

Version:		2.3.0b
Release:		14%{?dist}
License:		BSD
Group:			System Environment/Base
Group(zh_CN.UTF-8):	系统环境/基本
URL:			http://www.adel.nursat.kz/%{name}/

Source0:		http://www.adel.nursat.kz/%{name}/download/%{name}-%{version}.tar.gz
Source1:		apg.xinetd
Patch0:			apg-2.3.0b-gen_rand_pass.patch

BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires(post): grep

%description
APG (Automated Password Generator) is the tool set for random password
generation. This standalone version generates some random words of
required type and prints them to standard output.

%description -l zh_CN.UTF-8
产生随机密码的自动密码生成器，这是个独立版本。

%prep
%setup -q
%patch0 -p1 -b .gen_rand_pass

%build
# Build server
make CFLAGS="$RPM_OPT_FLAGS" FLAGS="$RPM_OPT_FLAGS" %{?_smp_mflags} cliserv

# Build standalone files
make CFLAGS="$RPM_OPT_FLAGS" FLAGS="$RPM_OPT_FLAGS" %{?_smp_mflags} standalone

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
install -D apg %{buildroot}%{_bindir}/apg
install -D apgbfm %{buildroot}%{_bindir}/apgbfm
install -D apgd %{buildroot}%{_sbindir}/apgd
install -D -m 644 doc/man/apg.1 %{buildroot}%{_mandir}/man1/apg.1
install -D -m 644 doc/man/apgbfm.1 %{buildroot}%{_mandir}/man1/apgbfm.1
install -D -m 644 doc/man/apgd.8 %{buildroot}%{_mandir}/man8/apgd.8

install -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/xinetd.d/apgd

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%post
# add a service for apg if it doesn't already exist
if ! grep -q ^pwdgen /etc/services; then
    echo -e 'pwdgen\t\t129/tcp\t\t\t# PWDGEN service' >> /etc/services
fi


%files
%defattr(-, root, root)
%doc CHANGES COPYING README THANKS TODO doc/rfc*
%{_bindir}/apg
%{_bindir}/apgbfm
%{_sbindir}/apgd
%{_mandir}/man*/*
%{_sysconfdir}/xinetd.d/apgd

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 2.3.0b-13
- 为 Magic 3.0 重建

* Sat Oct 29 2011 Liu Di <liudidi@gmail.com> - 2.3.0b-12
- 为 Magic 3.0 重建
