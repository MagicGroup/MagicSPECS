Name:		chromium-ffmpegsumo
Version:	27.0.1453.93
Release:	2%{?dist}
Summary:	Media playback library for chromium
Group:		System Environment/Libraries
License:	LGPLv2+
URL:		http://www.chromium.org/
# TODO: Document how I made the source for this beast from the chromium checkout
Source0:	%{name}-%{version}.tar.bz2
%ifarch %{ix86} x86_64
BuildRequires:	yasm
%endif
BuildRequires:	libvpx-devel
ExclusiveArch:	x86_64 %{ix86} %{arm}

%description
A media playback library for chromium. This is a fork of ffmpeg.
Because Google doesn't understand open source community involvement.
It only supports unencumbered codecs.

%package devel
Group:		Development/Libraries
Summary:	Development headers and libraries for ffmpegsumo
Requires:	%{name} = %{version}-%{release}

%description devel
Development headers and	libraries for ffmpegsumo.

%prep
%setup -q

%build
%ifarch %{ix86}
make ARCH=ia32 OPTFLAGS="%{optflags}" libdir=%{_libdir} includedir=%{_includedir}
%endif

%ifarch x86_64
make ARCH=x64 OPTFLAGS="%{optflags}" libdir=%{_libdir}	includedir=%{_includedir}
%endif

%ifarch %{arm}
make ARCH=arm OPTFLAGS="%{optflags}" libdir=%{_libdir}  includedir=%{_includedir}
%endif

%install
%ifarch %{ix86}
make ARCH=ia32 install DESTDIR=%{buildroot} libdir=%{_libdir}  includedir=%{_includedir}
%endif

%ifarch x86_64
make ARCH=x64 install DESTDIR=%{buildroot} libdir=%{_libdir}  includedir=%{_includedir}
%endif

%ifarch	%{arm}
make ARCH=arm install DESTDIR=%{buildroot} libdir=%{_libdir}  includedir=%{_includedir}
%endif

mkdir -p %{buildroot}%{_libdir}/chromium-browser/
pushd %{buildroot}%{_libdir}/chromium-browser/
ln -s ../libffmpegsumo.so.0.0.0 libffmpegsumo.so
popd
pushd %{buildroot}%{_libdir}
ln -s libffmpegsumo.so.0.0.0 libffmpegsumo.so.0
ln -s libffmpegsumo.so.0.0.0 libffmpegsumo.so
popd

# HACK
%ifarch %{ix86}
cp -a config/ia32/libavutil/avconfig.h %{buildroot}%{_includedir}/ffmpegsumo/libavutil/
%endif
%ifarch x86_64
cp -a config/x64/libavutil/avconfig.h %{buildroot}%{_includedir}/ffmpegsumo/libavutil/
%endif
%ifarch %{arm}
cp -a config/arm-neon/libavutil/avconfig.h %{buildroot}%{_includedir}/ffmpegsumo/libavutil/
%endif

%post 
/sbin/ldconfig
# This may seem counter-intuitive, but
# A) selinux doesn't treat /usr/lib64 differently from /usr/lib at a policy level.
#    In fact, it throws an error if you try to pass it.
# B) On systems where selinux is disabled, this command fails, so we just ignore it if it does.
/usr/sbin/semanage fcontext -a -t textrel_shlib_t '/usr/lib/libffmpegsumo.so.0.0.0' &> /dev/null
/sbin/restorecon %{_libdir}/libffmpegsumo.so.0.0.0 &> /dev/null || :

%postun -p /sbin/ldconfig

%files
%doc LICENSE COPYING.LGPLv2.1
%{_libdir}/libffmpegsumo.so.*
%{_libdir}/chromium-browser/libffmpegsumo.so

%files devel
%{_includedir}/ffmpegsumo/
%{_libdir}/libffmpegsumo.so

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 27.0.1453.93-2
- 为 Magic 3.0 重建

* Thu May 30 2013 Tom Callaway <spot@fedoraproject.org> - 27.0.1453.93-1
- update to 27.0.1453.93 sync

* Thu Apr  4 2013 Tom Callaway <spot@fedoraproject.org> - 25.0.1364.172-3
- drop explicit selinux scriptlet requires. If you don't have these tools,
  then you're not worried about selinux issues. :)

* Wed Apr  3 2013 Tom Callaway <spot@fedoraproject.org> - 25.0.1364.172-2
- give execmod permissions to libffmpegsumo.so.0.0.0

* Thu Mar 28 2013 Tom Callaway <spot@fedoraproject.org> - 25.0.1364.172-1
- resync with chromium 25.0.1364.172

* Thu Dec 13 2012 Tom Callaway <spot@fedoraproject.org> - 23.0.1271.95
- resync with chromium 23.0.1271.95

* Tue Aug 28 2012 Tom Callaway <spot@fedoraproject.org> - 21.0.1180.81-1
- sync with chromium 21.0.1180.81

* Thu Jun 14 2012 Tom Callaway <spot@fedoraproject.org> - 19.0.1084.56-2
- include config header

* Tue Jun 12 2012 Tom Callaway <spot@fedoraproject.org> - 19.0.1084.56-1
- update to 19.0.1084.56 forked tree

* Mon Feb 13 2012 Tom Callaway <spot@fedoraproject.org> - 17.0.963.46-1
- update to 17.0.963.46 forked tree

* Sat Feb  4 2012 Tom Callaway <spot@fedoraproject.org> - 14.0.827.10-2
- rebuild for newer libvpx

* Mon Jul 25 2011 Tom Callaway <spot@fedoraproject.org> - 14.0.827.10-1
- update to 14.0.827.10 forked tree

* Wed May 18 2011 Tom Callaway <spot@fedoraproject.org> - 11.0.696.68-1
- initial package
