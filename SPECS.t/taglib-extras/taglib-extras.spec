Summary:        Taglib support for other formats 
Summary(zh_CN.UTF-8): 支持其它格式的 Taglib
Name:           taglib-extras
Version:        1.0.1
Release:        6%{?dist}

Group:          Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
# all LGPLv2, except for rmff/ which is GPLv2+/LGPLv2+
License:        LGPLv2
URL:            http://websvn.kde.org/trunk/kdesupport/taglib-extras/
Source0:	http://www.kollide.net/~jefferai/taglib-extras-%{version}.tar.gz
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

# taglib-extras-config: drop multilib-conflicting mention of libdir, since
# it's already in default linker search path
Patch1: taglib-extras-0.1-multilib-1.patch

## upstream patches
Patch100: taglib-extras-1.0.1-version.patch

BuildRequires: cmake >= 2.6.0
BuildRequires: taglib-devel >= 1.6

Requires: taglib%{?_isa} => 1.6

%description
Taglib-extras delivers support for reading and editing the meta-data of 
audio formats not supported by taglib, including: asf, mp4v2, rmff, wav.

%description -l zh_CN.UTF-8
支持其它格式的 Taglib，包括：asf, mp4v2, rmff, wav等。

%package devel
Summary: Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:   Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig
Requires: taglib-devel
%description devel
%{summary}.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q 

%patch1 -p1 -b .multilib
%patch100 -p1 -b .version


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}   
%{cmake} ..
popd                        

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot} 

make install DESTDIR=%{buildroot} -C %{_target_platform}
magic_rpm_clean.sh

%clean
rm -rf %{buildroot} 


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING.LGPL
%{_libdir}/libtag-extras.so.1*

%files devel
%defattr(-,root,root,-)
%{_bindir}/taglib-extras-config
%{_includedir}/taglib-extras/
%{_libdir}/libtag-extras.so
%{_libdir}/pkgconfig/taglib-extras.pc


%changelog
* Wed Sep 30 2015 Liu Di <liudidi@gmail.com> - 1.0.1-6
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.0.1-5
- 为 Magic 3.0 重建

* Mon Oct 29 2012 Liu Di <liudidi@gmail.com> - 1.0.1-4
- 为 Magic 3.0 重建

* Mon Oct 29 2012 Liu Di <liudidi@gmail.com> - 1.0.1-5
- 为 Magic 3.0 重建

* Mon Oct 29 2012 Liu Di <liudidi@gmail.com> - 1.0.1-4
- 为 Magic 3.0 重建

* Mon Feb 13 2012 Liu Di <liudidi@gmail.com> - 1.0.1-3
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Sep 21 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.1-1
- taglib-extras-1.0.1

* Thu Sep 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.0-2
- drop (deprecated/no-op) kde integration

* Thu Sep 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.0-1
- taglib-extras-1.0.0 (API/ABI bump)

* Wed Sep 09 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.1.7-1
- taglib-extras-0.1.7

* Mon Aug 03 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.1.6-1
- taglib-extras-0.1.6

* Fri Jul 24 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.1.5-1
- taglib-extras-0.1.5

* Fri Jun 12 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.1.4-1
- taglib-extras-0.1.4

* Sat May 02 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.1.3-1
- taglib-extras-0.1.3

* Thu Apr 07 2009 Eelko Berkenpies <fedora@berkenpies.nl> - 0.1.2-1
- taglib-extras-0.1.2

* Thu Mar 26 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.1.1-2
- enable KDE integration, -DWITH_KDE

* Tue Mar 24 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.1.1-1
- taglib-extras-0.1.1

* Tue Mar 24 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.1-4
- refetch tarball

* Mon Mar 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.1-3
- -devel: Requires: taglib-devel
- Source0: full URL

* Mon Mar 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.1-2
- fixup for review

* Fri Mar 20 2009 Eelko Berkenpies <fedora@berkenpies.nl> - 0.1-1
- initial package
