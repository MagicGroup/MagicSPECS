Name:           fuse-convmvfs
Version:        0.2.6
Release:        5%{?dist}
Summary:        FUSE-Filesystem to convert filesystem encodings
Summary(zh_CN.UTF-8): 转换文件系统编码的文件系统

Group:          System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
License:        GPLv2
URL:            http://fuse-convmvfs.sourceforge.net/
Source0:        fuse-convmvfs-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  fuse-devel >= 2.5.0

BuildRequires:  libattr-devel

%description
This is a filesystem client use the FUSE(Filesystem in
USErspace) interface to convert file name from one charset
to another. Inspired by convmv.

%description -l zh_CN.UTF-8
这是使用 FUSE 的一个文件系统，可以转换文件名的编码。

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/convmvfs
%doc README* COPYING ChangeLog AUTHORS NEWS


%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 0.2.6-5
- 为 Magic 3.0 重建

* Fri Nov 25 2011 Liu Di <liudidi@gmail.com> - 0.2.6-4
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.2.6-2
- Rebuilt for gcc bug 634757

* Sun Sep 19 2010 ZC Miao <hellwolf.misty@gmail.com> - 0.2.6-1
- Update to 0.2.6

* Sat May 15 2010 ZC Miao <hellwolf.misty@gmail.com> - 0.2.5-1
- Update to 0.2.5

* Thu Sep 17 2009 Peter Lemenkov <lemenkov@gmail.com> - 0.2.4-10
- Rebuilt with new fuse

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jul 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.2.4-7
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.2.4-6
- Autorebuild for GCC 4.3

* Fri Jan 18 2008 ZC Miao <hellwolf.misty@gmail.com> - 0.2.4-5
- rebuild

* Tue Aug  7 2007 ZC Miao <hellwolf.misty@gmail.com> - 0.2.4-4
- increase release ver to fix EVR problems

* Fri Jun  1 2007 ZC Miao <hellwolf.misty@gmail.com> - 0.2.4-1
- update to 0.2.4

* Mon Feb 12 2007 ZC Miao <hellwolf.misty@gmail.com> - 0.2.3-2
- add doc AUTHORS NEWS, remove doc INSTALL
- Change URL

* Mon Feb 12 2007 ZC Miao <hellwolf.misty@gmail.com> - 0.2.3-1
- update to 0.2.3

* Fri Jul 28 2006 ZC Miao <hellwolf@seu.edu.cn> - 0.2.2-1
- update to 0.2.2

* Tue Jul 25 2006 ZC Miao <hellwolf@seu.edu.cn> - 0.2.1-1
- update to 0.2.1

* Mon Jul  3 2006 ZC Miao <hellwolf@seu.edu.cn> - 0.2-2
- add URL for Source0

* Fri Jun 30 2006 ZC Miao <hellwolf@seu.edu.cn> - 0.2-1
- init build
