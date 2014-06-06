%define name   kcometen3
%define version  1.1
%define release  2%{?dist}


Summary:        An comet OpenGL screensaver for KDE 3
Summary(zh_CN.UTF-8): KDE 3 的一个彗星 OpenGL 屏幕保护程序
Name:           %{name}
Version:        %{version}
Release:        %{release}
License:         GPL
Vendor:         Magic Linux
URL:            http://www.kde-look.org/content/show.php?content=30313
Packager:       Liu Di <ludidi@gmail.com>
Group:          Applications/Screensaver
Group(zh_CN.UTF-8):	应用程序/屏幕保护
Source0:	http://user.cs.tu-berlin.de/~pmueller/%{name}-%{version}.tar.bz2
Source1:	kcometen3.desktop
Source2:	kcometen3.zh_CN.po
Source3:	kcometen3.pot
Source4:	kcometen3.POTFILES.in
Patch1:		kcometen3-1.1-tde.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}%{testver}-%{release}-buildroot-%(%{__id_u} -n)
Prefix:         %(kde-config --prefix)
Requires:       kdelibs >= 3
BuildRequires:  kdelibs-devel >= 3

%description
KCometen3 is an comet OpenGL screensaver for KDE.

%description -l zh_CN.UTF-8
KCometen3 是 KDE 3 的一个彗星 OpenGL 屏幕保护程序。

%prep
%setup -q
%patch1 -p1

%build
%configure --with-extra-includes=%{_includedir}/tqt
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_datadir}/applnk/System/ScreenSavers/%{name}.desktop
install -m644 -D %{SOURCE1} %{buildroot}%{_datadir}/applnk/System/ScreenSavers/%{name}.desktop
install -d %{buildroot}%{_datadir}/locale/zh_CN/LC_MESSAGES/
msgfmt %{SOURCE2} -o %{buildroot}%{_datadir}/locale/zh_CN/LC_MESSAGES/%{name}.mo

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root)
%{_bindir}
%{_datadir}



%changelog
* Fri Jul 06 2007 kde <athena_star {at} 163 {dot} com> -1.1-1mgc
- init spec
