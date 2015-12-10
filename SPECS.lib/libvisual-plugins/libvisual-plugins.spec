Name:           libvisual-plugins
Version:        0.4.0
Release:        9%{?dist}
Summary:        Plugins for use with libvisual
Summary(zh_CN.UTF-8):	使用libvisual的插件

Group:          Applications/Multimedia
Group(zh_CN.UTF-8):	应用程序/多媒体
License:        GPL
URL:            http://libvisual.sourceforge.net/v2/
Source0:        http://easynews.dl.sourceforge.net/sourceforge/libvisual/%{name}-%{version}.tar.bz2
Patch0:         libvisual-plugins-0.2.0.mkinstalldirs.patch
Patch1:         libvisual-plugins-0.2.0-configure.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libvisual-devel >= 0.2.0
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  libX11-devel
BuildRequires:  libXt-devel
BuildRequires:  gtk2-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  esound-devel
BuildRequires:  pango-devel
BuildRequires:  mesa-libGL-devel


%description
Libvisual is an abstraction library that comes between applications and audio
visualisation plugins. This package provides visualizer plugins for use with
libvisual aware applications.

%description -l zh_CN.UTF-8
Libvisual是应用程序和音频可视化插件之间的一个抽象库。这个包提供了使用libvisual
的应用程序的可视化插件。

%prep
%setup -q
#%patch0 -p1
#%patch1 -p1


%build
%ifarch i386
export CFLAGS="${RPM_OPT_FLAGS} -mmmx"
%endif

%configure \
--enable-extra-optimization \
--disable-infinite \
--disable-flower \
--disable-dancingparticles \
--disable-gltest \
--disable-madspin \
--disable-nebulus 
# infinite disabled due to gcc 4 issue
# rest disabled because they are broken
# and cause totem to fail in a bad way

make %{?_smp_mflags}

%install
rm -rf %buildroot

make DESTDIR=%buildroot install

find %buildroot%_libdir -type f -name "*.la" -exec rm -f {} ';'

# there are no transform plugins. The library refers to it
# though as a place to look for plugins. Creating the directory
# even though empty prevents some meaningless error messages.
[ ! -d %buildroot%_libdir/libvisual/transform ] && install -d -m755 %buildroot%_libdir/libvisual/transform
magic_rpm_clean.sh

%clean
rm -rf %buildroot


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%_libdir/libvisual/
%_libdir/libvisual-0.4/
%_datadir/libvisual-plugins-0.4/

%changelog
* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 0.4.0-9
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 0.4.0-8
- 为 Magic 3.0 重建

* Wed Aug 06 2014 Liu Di <liudidi@gmail.com> - 0.4.0-7
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.4.0-6
- 为 Magic 3.0 重建

* Thu Jan 12 2012 Liu Di <liudidi@gmail.com> - 0.4.0-5
- 为 Magic 3.0 重建

* Fri Sep 15 2006 Liu Di <liudidi@gmail.com> - 0.4.0-1mgc
- update to 0.4.0

* Fri Feb 17 2006 Michael A. Peters <mpeters@mac.com> - 0.2.0-3
- Rebuild in devel branch

* Sun Nov 20 2005 Michael A. Peters <mpeters@mac.com> - 0.2.0-2
- configure patch (patch1) to fix detection of xlibraries/xincludes
- removed sed line fix of rpath in %%prep - no longer needed with
- the configure patch

* Sun Nov 20 2005 Michael A. Peters <mpeters@mac.com> - 0.2.0-1.9
- fixed it so it builds (specified x-libraries)
- building OpenGL plugin

* Sat Nov 19 2005 Michael A. Peters <mpeters@mac.com> - 0.2.0-1.3
- fix BuildRequires for mock, specify x-includedir to configure

* Fri Nov 18 2005 Michael A. Peters <mpeters@mac.com> - 0.2.0-1.2
- changed the xorg-x11-devel BuildRequires to modular xorg-x11
- for fc5
- put / at end of directories owned in %%files for readability.

* Sun Jun 19 2005 Michael A. Peters <mpeters@mac.com> - 0.2.0-1.1
- remove explicit rpath from LIBTOOL options

* Wed Jun 15 2005 Michael A. Peters <mpeters@mac.com> - 0.2.0-1
- initial checkin to Extras CVS
