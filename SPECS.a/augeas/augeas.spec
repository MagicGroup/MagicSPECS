Name:           augeas
Version:	1.4.0
Release:        3%{?dist}
Summary:        A library for changing configuration files
Summary(zh_CN.UTF-8): 一个更改配置文件的库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
URL:            http://augeas.net/
Source0:        http://download.augeas.net/%{name}-%{version}.tar.gz

# Format of the patch name is augeas-VERSION-NUMBER-HASH where VERSION
# gives the first version where this patch was applied, NUMBER orders patches
# against the same version, and HASH is the git commit hash from upstream

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  readline-devel libxml2-devel
Requires:       %{name}-libs = %{version}-%{release}

%description
A library for programmatically editing configuration files. Augeas parses
configuration files into a tree structure, which it exposes through its
public API. Changes made through the API are written back to the initially
read files.

The transformation works very hard to preserve comments and formatting
details. It is controlled by ``lens'' definitions that describe the file
format and the transformation into a tree.

%description -l zh_CN.UTF-8
这是一个编辑配置文件的工具，可以把配置文件的本地格式转成树形，编辑后再转回去。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}-libs = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package        libs
Summary:        Libraries for %{name}
Summary(zh_CN.UTF-8): %{name} 的库
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description    libs
The libraries for %{name}.

%description libs -l zh_CN.UTF-8
%{name} 的动态运行库。

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/augtool
%{_bindir}/augparse
%{_bindir}/fadot
%doc %{_mandir}/man1/*
%{_datadir}/vim/vimfiles/syntax/augeas.vim
%{_datadir}/vim/vimfiles/ftdetect/augeas.vim

%files libs
%defattr(-,root,root,-)
# %{_datadir}/augeas and %{_datadir}/augeas/lenses are owned
# by filesystem.
%{_datadir}/augeas/lenses/dist
%{_libdir}/*.so.*
%doc AUTHORS COPYING NEWS

%files devel
%defattr(-,root,root,-)
%doc
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/augeas.pc

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 1.4.0-3
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1.4.0-2
- 为 Magic 3.0 重建

* Fri Sep 18 2015 Liu Di <liudidi@gmail.com> - 1.4.0-1
- 更新到 1.4.0

* Sun Mar 02 2014 Liu Di <liudidi@gmail.com> - 1.2.0-2
- 更新到 1.2.0

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan  4 2013 David Lutterkort <lutter@redhat.com> - 1.0.0-1
- New version; remove all patches

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 10 2012 David Lutterkort <lutter@redhat.com> - 0.10.0-3
- Add patches for bugs 247 and 248 (JSON lens)

* Sat Dec  3 2011 Richard W.M. Jones <rjones@redhat.com> - 0.10.0-2
- Add patch to resolve missing libxml2 requirement in augeas.pc.

* Fri Dec  2 2011 David Lutterkort <lutter@redhat.com> - 0.10.0-1
- New version

* Mon Jul 25 2011 David Lutterkort <lutter@redhat.com> - 0.9.0-1
- New version; removed patch pathx-whitespace-ea010d8

* Tue May  3 2011 David Lutterkort <lutter@redhat.com> - 0.8.1-2
- Add patch pathx-whitespace-ea010d8.patch to fix BZ 700608

* Fri Apr 15 2011 David Lutterkort <lutter@redhat.com> - 0.8.1-1
- New version

* Wed Feb 23 2011 David Lutterkort <lutter@redhat.com> - 0.8.0-1
- New version

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 22 2010 Matthew Booth <mbooth@redhat.com> - 0.7.4-1
- Update to version 0.7.4

* Thu Nov 18 2010 Richard W.M. Jones <rjones@redhat.com> - 0.7.3-2
- Upstream patch proposed to fix GCC optimization bug (RHBZ#651992).

* Fri Aug  6 2010 David Lutterkort <lutter@redhat.com> - 0.7.3-1
- Remove upstream patches

* Tue Jun 29 2010 David Lutterkort <lutter@redhat.com> - 0.7.2-2
- Patches based on upstream fix for BZ 600141

* Tue Jun 22 2010 David Lutterkort <lutter@redhat.com> - 0.7.2-1
- Fix ownership of /usr/share/augeas. BZ 569393

* Wed Apr 21 2010 David Lutterkort <lutter@redhat.com> - 0.7.1-1
- New version

* Thu Jan 14 2010 David Lutterkort <lutter@redhat.com> - 0.7.0-1
- Remove patch vim-ftdetect-syntax.patch. It's upstream

* Tue Dec 15 2009 David Lutterkort <lutter@redhat.com> - 0.6.0-2
- Fix ftdetect file for vim

* Mon Nov 30 2009 David Lutterkort <lutter@redhat.com> - 0.6.0-1
- Install vim syntax files

* Mon Sep 14 2009 David Lutterkort <lutter@redhat.com> - 0.5.3-1
- Remove separate xorg.aug, included in upstream source

* Tue Aug 25 2009 Matthew Booth <mbooth@redhat.com> - 0.5.2-3
- Include new xorg lens from upstream

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 David Lutterkort <lutter@redhat.com> - 0.5.2-1
- New version

* Fri Jun  5 2009 David Lutterkort <lutter@redhat.com> - 0.5.1-1
- Install fadot

* Fri Mar 27 2009 David Lutterkort <lutter@redhat.com> - 0.5.0-2
- fadot isn't being installed just yet

* Tue Mar 24 2009 David Lutterkort <lutter@redhat.com> - 0.5.0-1
- New program /usr/bin/fadot

* Mon Mar  9 2009 David Lutterkort <lutter@redhat.com> - 0.4.2-1
- New version

* Fri Feb 27 2009 David Lutterkort <lutter@redhat.com> - 0.4.1-1
- New version

* Fri Feb  6 2009 David Lutterkort <lutter@redhat.com> - 0.4.0-1
- New version

* Mon Jan 26 2009 David Lutterkort <lutter@redhat.com> - 0.3.6-1
- New version

* Tue Dec 23 2008 David Lutterkort <lutter@redhat.com> - 0.3.5-1
- New version

* Mon Feb 25 2008 David Lutterkort <dlutter@redhat.com> - 0.0.4-1
- Initial specfile
