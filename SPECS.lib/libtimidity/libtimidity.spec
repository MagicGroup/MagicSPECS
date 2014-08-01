Name:           libtimidity
Version:        0.1.0
Release:        11%{?dist}
Summary:        MIDI to WAVE converter library
Summary(zh_CN.UTF-8): MIDI 转 WAV 转换库
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
URL:            http://libtimidity.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Patch0:         libtimidity-0.1.0-missing-protos.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       timidity++-patches

%description
This library is based on the TiMidity decoder from SDL_sound library.
Purpose to create this library is to avoid unnecessary dependences.
SDL_sound requires SDL and some other libraries, that not needed to
process MIDI files. In addition libtimidity provides more suitable
API to work with MIDI songs, it enables to specify full path to the
timidity configuration file, and have function to retrieve meta data
from MIDI song.

%description -l zh_CN.UTF-8
MIDI 转 WAV 转换库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       pkgconfig, %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch0 -p1


%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/libtimidity.la
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS CHANGES COPYING ChangeLog NEWS README* TODO
%{_libdir}/libtimidity-0.1.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/timidity.h
%{_libdir}/libtimidity.so
%{_libdir}/pkgconfig/libtimidity.pc


%changelog
* Fri Aug 01 2014 Liu Di <liudidi@gmail.com> - 0.1.0-11
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.1.0-10
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Apr  3 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.1.0-6
- Fix missing prototype compiler warnings

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.1.0-5
- Autorebuild for GCC 4.3

* Sun Oct 14 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.1.0-4
- Require timidity++-patches instead of timidity++ itself so that we don't
  drag in arts and through arts, qt and boost.

* Mon Aug 13 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.1.0-3
- Update License tag for new Licensing Guidelines compliance

* Wed Jul 25 2007 Jesse Keating <jkeating@redhat.com> - 0.1.0-2
- Rebuild for RH #249435

* Fri Jun 29 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.1.0-1
- Initial Fedora package
