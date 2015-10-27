%bcond_with static
%bcond_with xmms

%if 0%{?with_xmms}
%define	xmms_plugdir %(xmms-config --general-plugin-dir 2>/dev/null)
%endif

Name:           xosd
Version:        2.2.14
Release:        15%{?dist}
Summary:        On-screen display library for X
Summary(zh_CN.UTF-8): X 的屏幕显示库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8):	系统环境/库
License:        GPLv2+
URL:            http://www.ignavus.net/software.html
Source:         http://ftp.debian.org/debian/pool/main/x/xosd/%{name}_%{version}.orig.tar.gz
Patch0:         %{name}-aclocal18.patch
Patch1:         %{name}-defaults.patch
Patch2:		xosd-2.2.14-Do-not-install-some-manual-pages-twice.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  libXinerama-devel
# As of 2.2.14, the default font *must* be found, even if not used (#183971)
Requires:       xorg-x11-fonts-base

%description
XOSD displays text on your screen, sounds simple right? The difference
is it is unmanaged and shaped, so it appears transparent. This gives
the effect of an On Screen Display, like your TV/VCR etc.. The package
also includes an xmms plugin, which automatically displays various
interesting things as they change (song name, volume etc...)

%description -l zh_CN.UTF-8
X 的屏幕显示库。

%package        devel
Summary:        Development files for the XOSD on-screen display library
Summary(zh_CN.UTF-8):	%name 的开发包。
Group:          Development/Libraries
Group(zh_CN.UTF-8):	开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       libX11-devel
Requires:       libXext-devel
Requires:       libXinerama-devel

%description    devel
The xosd-devel package contains static libraries, header files and
documentation for developing applications that use the XOSD on-screen
display.

%description devel -l zh_CN.UTF-8
%name 的开发包。

%if 0%{?with_xmms}
%package     -n xmms-%{name}
Summary:        XMMS plugin for on-screen display using the XOSD library
Summary(zh_CN.UTF-8):	XOSD 库的 XMMS 插件
Group:          Applications/Multimedia
Group(zh_CN.UTF-8):	应用程序/多媒体
BuildRequires:  gtk+-devel >= 1.2.2
BuildRequires:  gdk-pixbuf-devel
BuildRequires:  xmms-devel
Requires:       %{name} = %{version}-%{release}
Requires:       xmms
Obsoletes:      %{name}-xmms <= 2.2.12

%description -n xmms-%{name}
X MultiMedia System plugin to display information on-screen through
the XOSD library, similarly to TV OSD.

%description -n xmms-%{name} -l zh_CN.UTF-8
XOSD 库的 XMMS 插件。

%package     -n bmp-%{name}
Summary:        BMP plugin for on-screen display using the XOSD library
Summary(zh_CN.UTF-8): XOSD 库的 BMP 插件
Group:          Applications/Multimedia
Group(zh_CN.UTF-8):   应用程序/多媒体
BuildRequires:  gtk2-devel >= 1.2.2
Requires:       %{name} = %{version}-%{release}
Requires:       beep-media-player

%description -n bmp-%{name}
X MultiMedia System plugin to display information on-screen through
the XOSD library, similarly to TV OSD.

%description -n bmp-%{name} -l zh_CN.UTF-8
XOSD 库的 BMP 插件。
%endif

%prep
%setup -q
%patch0 -p0
%patch1 -p1
%patch2 -p1
for f in ChangeLog man/xosd_{create,destroy,display,is_onscreen,set_bar_length}.3 ; do
    iconv -f iso-8859-1 -t utf-8 $f > $f.utf8 ; mv $f.utf8 $f
done


%build
%configure --disable-dependency-tracking %{!?with_static:--disable-static}
make %{?_smp_mflags}
%{__perl} -pi -e "s|$RPM_OPT_FLAGS\\s*|| ; s|\\s*-Wall||" script/xosd-config


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT{%{_libdir},%{xmms_plugdir},%{_libdir}/bmp/General}/*.la
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README TODO
%{_bindir}/osd_cat
%{_libdir}/libxosd.so.*
%{_datadir}/xosd/
%{_mandir}/man1/osd_cat.1*

%files devel
%defattr(-,root,root,-)
%{_bindir}/xosd-config
%{_includedir}/xosd.h
%{_libdir}/libxosd.so
%if %{with static}
%{_libdir}/libxosd.a
%endif
%{_datadir}/aclocal/libxosd.m4
%{_mandir}/man1/xosd-config.1*
%{_mandir}/man3/xosd*.3*

%if 0%{?with_xmms}
%files -n xmms-%{name}
%defattr(-,root,root,-)
%{xmms_plugdir}/libxmms_osd.so

%files -n bmp-%{name}
%defattr(-,root,root,-)
%{_libdir}/bmp/General/libbmp_osd.so
%endif

%changelog
* Tue Oct 27 2015 Liu Di <liudidi@gmail.com> - 2.2.14-15
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 2.2.14-14
- 为 Magic 3.0 重建


