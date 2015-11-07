Summary: Converts filenames from one encoding to another.
Summary(zh_CN.UTF-8): 转换文件名从一个编码到另一个。
Name:    convmv
Version: 1.15
Release: 3%{?dist}
License: GPL
Group:   Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Source:  http://j3e.de/linux/convmv/%{name}-%{version}.tar.gz
Prefix:  %{_prefix}
BuildRoot: %{_tmppath}/%{name}-root
Requires:  perl

%description
convmv is meant to help convert a single filename, a directory tree and the
contained files or a whole filesystem into a different encoding. It just
converts the filenames, not the content of the files. A special feature of
convmv is that it also takes care of symlinks, also converts the symlink target
pointer in case the symlink target is being converted, too.

All this comes in very handy when one wants to switch over from old 8-bit
locales to UTF-8 locales. It is also possible to convert directories to UTF-8
which are already partly UTF-8 encoded. convmv is able to detect if certain
files are UTF-8 encoded and will skip them by default. To turn this smartness
off use the --nosmart switch.

%description -l zh_CN.UTF-8
convmv 可以帮助转换单个文件名，目录树和它包含的文件或整个文件系统到不同的编码。
它只转换文件名，不是文件的内容。

%prep
%setup -q

%build
make DESTDIR=${RPM_BUILD_ROOT} PREFIX=%{_prefix}

%install
rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=${RPM_BUILD_ROOT} PREFIX=%{_prefix}

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%doc CREDITS Changes TODO
%{_bindir}/convmv
%{_mandir}/man1/*

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1.15-3
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.15-2
- 为 Magic 3.0 重建

* Tue Nov 08 2011 Liu Di <liudidi@gmail.com> - 1.15-1
- 更新到 1.15

* Fri Mar 09 2007 Liu Di <liudidi@gmail.com> - 1.10-1mgc
- update to 1.10

* Mon Feb 20 2006 liudi <liudidi@gmail.com>
- Update to 1.09
* Fri Aug 05 2005 sejishikong<sejishikong@263.net>
- First Build for Magiclinux 2.0 beta2
