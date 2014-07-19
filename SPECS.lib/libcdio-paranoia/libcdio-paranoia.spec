Name: libcdio-paranoia
Version: 10.2+0.90+1
Release: 3%{?dist}
Summary: CD paranoia on top of libcdio
Summary(zh_CN.UTF-8): 基于 libcdio 的 CD 抓轨工具
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License: GPLv2+ and LGPLv2+
URL: http://www.gnu.org/software/libcdio/
Source0: http://ftp.gnu.org/gnu/libcdio/libcdio-paranoia-%{version}.tar.gz
Patch0: libcdio-paranoia-manpage.patch
BuildRequires: pkgconfig 
BuildRequires: gettext-devel
BuildRequires: chrpath
BuildRequires: libcdio-devel


%description
This CDDA reader distribution ('libcdio-cdparanoia') reads audio from the
CDROM directly as data, with no analog step between, and writes the
data to a file or pipe as .wav, .aifc or as raw 16 bit linear PCM.

Split off from libcdio to allow more flexible licensing and to be compatible
with cdparanoia-III-10.2's license. And also, libcdio is just too large.

%description -l zh_CN.UTF-8
基于 libcdio 的 CD 抓轨工具。

%package devel
Summary: Header files and libraries for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains header files and libraries for %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch0 -p1

# fix pkgconfig files
sed -i -e 's,-I${includedir},-I${includedir}/cdio,g' libcdio_paranoia.pc.in
sed -i -e 's,-I${includedir},-I${includedir}/cdio,g' libcdio_cdda.pc.in

f=doc/ja/cd-paranoia.1.in
iconv -f euc-jp -t utf-8 -o $f.utf8 $f && mv $f.utf8 $f
iconv -f ISO88591 -t utf-8 -o THANKS.utf8 THANKS && mv THANKS.utf8 THANKS

%build
%configure \
	--disable-dependency-tracking \
	--disable-static \
	--disable-rpath
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

mv $RPM_BUILD_ROOT%{_mandir}/{jp,ja}

# copy include files to an additional directory for backward compatibility
# this is where most software still expects those files
cp -a $RPM_BUILD_ROOT%{_includedir}/cdio/paranoia/*.h $RPM_BUILD_ROOT%{_includedir}/cdio/

# remove rpath
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/*
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/*.so.*
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README THANKS COPYING-GPL COPYING-LGPL
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%doc doc/FAQ.txt doc/overlapdef.txt
%{_includedir}/cdio/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Sun Jul 13 2014 Liu Di <liudidi@gmail.com> - 10.2+0.90+1-3
- 为 Magic 3.0 重建

* Mon Dec 16 2013 Adrian Reber <adrian@lisas.de> - 10.2+0.90+1-2
- Rebuilt for new libcdio-0.92

* Tue Aug 20 2013 Adrian Reber <adrian@lisas.de> - 10.2+0.90+1-1
- updated to 10.2+0.90+1
- removed all patches previously taken from git

* Wed Jul 31 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 10.2+0.90-8
- long name in manual page caused 'whatis' to misbehave

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.2+0.90-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 11 2013 Adrian Reber <adrian@lisas.de> - 10.2+0.90-6
- remove sed changes on non-installed file
- fix -devel subpackage Require

* Sat Dec 22 2012 Adrian Reber <adrian@lisas.de> - 10.2+0.90-5
- provide include files also in the paranoia directory (like in upstream's git)

* Thu Nov 22 2012 Adrian Reber <adrian@lisas.de> - 10.2+0.90-4
- fix pkgconfig files to point to right include directory

* Mon Nov 05 2012 Adrian Reber <adrian@lisas.de> - 10.2+0.90-3
- included upstreamed patches which are changing the license
  headers to be LGPLv2+ for the library parts and GPLv2+ for the
  binaries

* Tue Oct 30 2012 Adrian Reber <adrian@lisas.de> - 10.2+0.90-2
- added missing files from git: COPYING-GPL and COPYING-LGPL
- added patch from git for missing pkgconfig requires
  and fixed FSF address

* Mon Oct 29 2012 Adrian Reber <adrian@lisas.de> - 10.2+0.90-1
- initial release
