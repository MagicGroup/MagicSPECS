Summary:    Non-interactive SSH authentication utility
Summary(zh_CN.UTF-8): 非交互式的 SSH 认证工具
Name:       sshpass
Version:    1.05
Release:    5%{?dist}
License:    GPLv2
Group:      Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
Url:        http://sshpass.sourceforge.net/
Source0:    http://downloads.sourceforge.net/sshpass/sshpass-%{version}.tar.gz

%description
Tool for non-interactively performing password authentication with so called
"interactive keyboard password authentication" of SSH. Most users should use
more secure public key authentication of SSH instead.

%description -l zh_CN.UTF-8
非交互式的 SSH 认证工具。

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
magic_rpm_clean.sh

%files
%{_bindir}/sshpass
%{_datadir}/man/man1/sshpass.1.gz
%doc AUTHORS COPYING ChangeLog NEWS

%changelog
* Tue Sep 29 2015 Liu Di <liudidi@gmail.com> - 1.05-5
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.05-4
- 为 Magic 3.0 重建

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild


* Tue Aug 23 2011 Martin Cermak <mcermak@redhat.com> 1.05-1
- Packaged for Fedora 

