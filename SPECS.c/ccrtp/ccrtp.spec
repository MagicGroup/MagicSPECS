Summary: Common C++ class framework for RTP/RTCP
Summary(zh_CN.UTF-8): RTP/RTCP 的通用 C++ 类框架
Name: ccrtp
Version: 2.0.8
Release: 4%{?dist}
License: GPLv2+
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Source0: http://ftp.gnu.org/pub/gnu/ccrtp/ccrtp-%{version}.tar.gz
URL: http://www.gnu.org/software/commoncpp/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: commoncpp2-devel >= 1.7.0, doxygen, libgcrypt-devel, ucommon-devel

%description
ccRTP is a generic, extensible and efficient C++ framework for
developing applications based on the Real-Time Transport Protocol
(RTP) from the IETF. It is based on Common C++ and provides a full
RTP/RTCP stack for sending and receiving of realtime data by the use
of send and receive packet queues. ccRTP supports unicast,
multi-unicast and multicast, manages multiple sources, handles RTCP
automatically, supports different threading models and is generic as
for underlying network and transport protocols.

%description -l zh_CN.UTF-8
RTP/RTCP 的通用 C++ 类框架。

%package devel
Summary: Header files and libraries for %{name} development
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
# Some of the headers are LGPLv2+
License: GPLv2+ and LGPLv2+
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig, commoncpp2-devel
Requires(post): /usr/sbin/install-info
Requires(preun): /usr/sbin/install-info

%description devel
The %{name}-devel package contains the header files and libraries needed
to develop programs that use the %{name} library.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
chmod 644 src/ccrtp/rtp.h

%build
%configure \
	--disable-static
%{__make} # %{?_smp_mflags} smp builds disabled

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_infodir}/dir
find %{buildroot} -name '*.la' -exec rm -f {} \;
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /usr/sbin/ldconfig

%post devel
/usr/sbin/install-info %{_infodir}/ccrtp.info* %{_infodir}/dir || :

%preun devel
if [ $1 = 0 ]; then
    /usr/sbin/install-info --delete %{_infodir}/ccrtp.info* %{_infodir}/dir || :
fi

%postun -p /usr/sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README COPYING.addendum
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/html
%dir %{_includedir}/ccrtp
%{_includedir}/ccrtp/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libccrtp.pc
%{_infodir}/ccrtp.info*


%changelog
* Fri Apr 11 2014 Liu Di <liudidi@gmail.com> - 2.0.8-4
- 更新到 2.0.8

* Fri Mar 07 2014 Liu Di <liudidi@gmail.com> - 2.0.7-2
- 更新到 2.0.7

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 2.0.2-2
- 为 Magic 3.0 重建

* Sun Jan 22 2012 Kevin Fenzi <kevin@scrye.com> - 2.0.2-1
- Update to 2.0.2

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 07 2009 Andreas Thienemann <andreas@bawue.net> - 1.7.1-1
- Update to upstream release 1.7.1

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.6.0-2
- fix license tag

* Wed Feb 06 2008 Andreas Thienemann <andreas@bawue.net> - 1.6.0-1
- Updated to upstream version 1.6.0
- Added patch enabling build with gcc-4.3

* Wed Feb 06 2008 Dennis Gilmore <dennis@ausil.us> - 1.5.1-2
- rebuild for new commoncpp2

* Wed Mar 07 2007 Andreas Thienemann <andreas@bawue.net> - 1.5.1-1
- Updated package to 1.5.1
- Fixed #219396

* Fri Nov 10 2006 Andreas Thienemann <andreas@bawue.net> - 1.5.0-1
- Updated package to 1.5.0, fixing #209026

* Sun Sep 10 2006 Andreas Thienemann <andreas@bawue.net> - 1.4.1-2
- *bump*

* Fri Sep 08 2006 Andreas Thienemann <andreas@bawue.net> - 1.4.1-1
- Updated to 1.4.1

* Sun Jul 23 2006 Andreas Thienemann <andreas@bawue.net> - 1.3.7-2
- Added doxygen BuildRequire

* Mon Apr 24 2006 Andreas Thienemann <andreas@bawue.net> - 1.3.7-1
- Updated to 1.3.7

* Fri Feb 03 2006 Andreas Thienemann <andreas@bawue.net> - 1.3.6-1
- Initial spec.
