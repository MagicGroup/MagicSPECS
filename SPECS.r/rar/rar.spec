# $Id$
# Authority: matthias

# The source contains only binaries...
%define _use_internal_dependency_generator 0
# Disable stripping or the default.sfx will get trashed
%define __strip /bin/true

Summary: RAR archiver to create and manage RAR archives
Summary(zh_CN.UTF-8): 建立和管理RAR档案
Name: rar
Version:	5.2.1
Release:	2%{?dist}
License: Shareware
Group: Applications/Archiving
Group(zh_CN.UTF-8): 应用程序/归档
URL: http://www.rarlabs.com/
Source0: http://www.rarlabs.com/rar/rarlinux-%{version}.tar.gz
Source1: http://www.rarlabs.com/rar/rarlinux-x64-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: %{ix86} x86_64

%description
RAR is a powerful tool allowing you to manage and control archive files.
Console RAR supports archives only in RAR format, which names usually have
a ".rar" extension. ZIP and other formats are not supported.

%description -l zh_CN.UTF-8
RAR是一个强力工具，它允许你管理和控制归档。控制台RAR只支持RAR格式，就是带有
.rar扩展名的。ZIP和其它格式不支持。

%prep
rm -rf rar
%ifarch %{ix86}
tar xvf %{SOURCE0}
%endif
%ifarch x86_64
tar xvf %{SOURCE1}
%endif
/bin/chmod -Rf a+rX,u+w,g-w,o-w .

%install
cd rar
%{__rm} -rf %{buildroot}
%{__install} -D -p -m 0755 rar %{buildroot}%{_bindir}/rar
%{__install} -D -p -m 0755 unrar %{buildroot}%{_bindir}/unrar
%{__install} -D -p -m 0755 rar_static %{buildroot}%{_bindir}/rar_static
%{__install} -D -p -m 0644 rarfiles.lst %{buildroot}%{_sysconfdir}/rarfiles.lst
%{__install} -D -p -m 0755 default.sfx %{buildroot}%{_libdir}/default.sfx

magic_rpm_clean.sh

%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
%{_sysconfdir}/rarfiles.lst
%{_bindir}/*
%{_libdir}/default.sfx


%changelog
* Sat Sep 12 2015 Liu Di <liudidi@gmail.com> - 5.2.1-2
- 为 Magic 3.0 重建

* Sat Sep 12 2015 Liu Di <liudidi@gmail.com> - 5.2.1-1
- 更新到 5.2.1

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 4.2.0-2
- 为 Magic 3.0 重建

* Tue Oct 10 2006 Liu Di <liudidi@gmail.com> - 3.6.0-1mgc
- update to 3.6.0(aka 3.60)

* Mon Dec 5 2005 KanKer <kanker@163.com>
- rebuild

* Fri Oct 14 2005 Matthias Saou <http://freshrpms.net/> 3.5.1-1
- Update to 3.5.1 (aka 3.51).

* Sun Jun  5 2005 Matthias Saou <http://freshrpms.net/> 3.5-0.b1
- Update to 3.5.b1.

* Wed Nov  3 2004 Matthias Saou <http://freshrpms.net/> 3.4.1-1
- Update to 3.4.1.

* Wed May 19 2004 Matthias Saou <http://freshrpms.net/> 3.3.0-2
- Updated description.
- Fixed the rarfiles.lst installation.
- Rebuild for Fedora Core 2.

* Thu Feb 26 2004 Matthias Saou <http://freshrpms.net/> 3.3.0-1
- Update to 3.3.0.

* Fri Nov  7 2003 Matthias Saou <http://freshrpms.net/> 3.2.0-3
- Rebuild for Fedora Core 1.

* Mon Nov  3 2003 Matthias Saou <http://freshrpms.net/> 3.2.0-2.fr
- Disable stripping to not trash the default.sfx file.
- Add back rarfiles.lst, as it does work, thanks to Ondrej Svejda.

* Thu Oct 30 2003 Matthias Saou <http://freshrpms.net/> 3.2.0-1.fr
- Update to latest version.
- Spec file cleanup.
- Remove the internal dep check to avoid "corrupted program header size" msg.

* Sun Mar 18 2001 Matthias Saou <http://freshrpms.net/>
- Fix the %files with a %dir (cleaner uninstall)
- Spec file cleanup

* Sun Mar 18 2001 Alexander Skwar <ASkwar@Linux-Mandrake.com> 2.80-1
- New non-beta release

* Mon Feb 26 2001 Alexander Skwar <ASkwar@Linux-Mandrake.com> 2.80b5-1
- New release, see http://www.rarsoft.com/rar/WhatsNew.txt for
  list of fixed bugs

* Sun Jan 28 2001 Alexander Skwar <ASkwar@Linux-Mandrake.com> 2.80b4-1
- Nothing exciting, besides the latest beta

* Thu Jan  4 2001 Alexander Skwar <ASkwar@Linux-Mandrake.com> 2.80b2-1
- Another new version

* Sat Sep 15 2000 01:00:35 Alexander Skwar <ASkwar@DigitalProjects.com> 2.71-1
- New version
