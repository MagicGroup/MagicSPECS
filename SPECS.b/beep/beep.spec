%if 0%{?fedora} >= 12
%global ship_modprobe_config 1
%else
%global ship_modprobe_config 0
%endif


Summary:        Beep the PC speaker any number of ways
Summary(zh_CN.UTF-8): 让电脑的喇叭发声
Name:           beep
Version:        1.3
Release:        4%{?dist}

Group:          Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
License:        GPLv2+
URL:            http://www.johnath.com/beep/
Source0:        http://www.johnath.com/beep/%{name}-%{version}.tar.gz
Source1:        %{name}-README.fedora
Source2:        %{name}-modprobe.conf
Patch0:         beep-1.2.2-install-fixes.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  glibc-kernheaders


%description
Beep allows the user to control the PC speaker with precision,
allowing different sounds to indicate different events. While it
can be run quite happily on the commandline, it's intended place
of residence is within shell/perl scripts, notifying the user when
something interesting occurs. Of course, it has no notion of
what's interesting, but it's real good at that notifying part.

%description -l zh_CN.UTF-8
Beep 允许用户更精确的控制电脑的喇叭发声，以不同的声音指示不同的事件。
虽然可以在命令上用，但它还是在脚本中使用更好，以通知用户有事发生。

%prep
%setup -q
%patch0 -p1 -b .install-fixes
cp -p %{SOURCE1} README.fedora


%build
make %{?_smp_mflags} CFLAGS="${RPM_OPT_FLAGS}"


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%if %{ship_modprobe_config}
install -d -m 0755 "$RPM_BUILD_ROOT/etc/modprobe.d/"
install -p -m 0644 %{SOURCE2} "$RPM_BUILD_ROOT/etc/modprobe.d/beep.conf"
%endif


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc CHANGELOG COPYING CREDITS README
%attr(0755,root,root) %{_bindir}/beep
%{_mandir}/man1/beep.1.gz
%if %{ship_modprobe_config}
%doc README.fedora
%attr(0644,root,root) %{_sysconfdir}/modprobe.d/beep.conf
%endif


%changelog
* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 16 2010 Hans Ulrich Niedermann <hun@n-dimensional.de> - 1.3-1
- Update to upstream release beep-1.3

* Fri Jan 22 2010 Hans Ulrich Niedermann <hun@n-dimensional.de> - 1.2.2-6
- Ship modprobe config file with alias for pcspkr on F12 and later

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Sep  7 2008 Hans Ulrich Niedermann <hun@n-dimensional.de> - 1.2.2-3
- Initial package for submission to Fedora
