Name: linuxconsoletools
Version: 1.4.8
Release: 4%{?dist}
Summary: Tools for connecting joysticks & legacy devices to the kernel's input subsystem
Summary(zh_CN.UTF-8): 连接游戏摇杆和过时设备到内核输入子系统的工具
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
License: GPLv2+
URL: http://sourceforge.net/projects/linuxconsole/

Source: http://downloads.sourceforge.net/linuxconsole/%{name}-%{version}.tar.bz2

BuildRequires: SDL-devel

Provides: joystick = %{version}-%{release}
Provides: ff-utils = 1:%{version}-%{release}
Obsoletes: joystick < 1.2.16-1
Obsoletes: ff-utils < 2.4.22-1
Conflicts: gpm < 1.20.6-26

%description
This package contains utilities for testing and configuring joysticks,
connecting legacy devices to the kernel's input subsystem (providing support
for serial mice, touchscreens etc.), and test the input event layer.

%description -l zh_CN.UTF-8
连接游戏摇杆和过时设备（比如串口鼠标，触摸屏等）到内核输入子系统的测试和配置工具，

%prep
%setup -q

%build
make PREFIX=%{_prefix} CFLAGS="%{optflags}" %{?_smp_mflags}

# moving helper scripts from /usr/share/joystick to /usr/libexec/joystick
sed -i "s|%{_prefix}/share/joystick|%{_libexecdir}/joystick|g" utils/jscal-restore utils/jscal-store


%install
make DESTDIR=%{buildroot} PREFIX=%{_prefix} install

# moving helper scripts from /usr/share/joystick to /usr/libexec/joystick
install -d -m 0755 %{buildroot}%{_libexecdir}/joystick
mv -f %{buildroot}%{_prefix}/share/joystick/* %{buildroot}%{_libexecdir}/joystick/

# fixing man permissions
chmod -x %{buildroot}%{_mandir}/man1/*
magic_rpm_clean.sh

%files
%doc COPYING README NEWS

%{_bindir}/ffcfstress
%{_bindir}/ffmvforce
%{_bindir}/ffset
%{_bindir}/fftest
%{_bindir}/inputattach
%{_bindir}/jscal
%{_bindir}/jscal-restore
%{_bindir}/jscal-store
%{_bindir}/jstest

%{_libexecdir}/joystick/extract
%{_libexecdir}/joystick/filter
%{_libexecdir}/joystick/ident

%{_mandir}/man1/*


%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 1.4.8-4
- 更新到 1.4.8

* Tue Jul 01 2014 Liu Di <liudidi@gmail.com> - 1.4.7-3
- 为 Magic 3.0 重建

* Mon Apr 14 2014 Liu Di <liudidi@gmail.com> - 1.4.7-2
- 为 Magic 3.0 重建

* Wed Jan 08 2014 Jaromir Capik <jcapik@redhat.com> - 1.4.7-1
- Update to 1.4.7

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 07 2013 Jaromir Capik <jcapik@redhat.com> - 1.4.6-1
- Update to 1.4.6

* Tue Apr 09 2013 Jaromir Capik <jcapik@redhat.com> - 1.4.5-1
- Update to 1.4.5

* Wed Feb 06 2013 Jaromir Capik <jcapik@redhat.com> - 1.4.4-7
- Adding new switches to the ffcfstress man page

* Wed Feb 06 2013 Jaromir Capik <jcapik@redhat.com> - 1.4.4-6
- Merging the 64bit patch from ff-utils

* Mon Feb 04 2013 Jaromir Capik <jcapik@redhat.com> - 1.4.4-5
- Resolving conflicts with ff-utils

* Fri Jan 04 2013 Jaromir Capik <jcapik@redhat.com> - 1.4.4-4
- Adding conflict with gpm < 1.20.6-26 (inputattach)

* Thu Jan 03 2013 Jaromir Capik <jcapik@redhat.com> - 1.4.4-3
- Passing optflags to make

* Wed Jan 02 2013 Jaromir Capik <jcapik@redhat.com> - 1.4.4-2
- Using prefix macro

* Wed Jan 02 2013 Jaromir Capik <jcapik@redhat.com> - 1.4.4-1
- Initial package
