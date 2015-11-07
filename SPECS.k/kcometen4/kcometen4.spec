Name:           kcometen4
Version:        1.0.7
Release:        3%{?dist}
Summary:        An OpenGL screensaver with exploding comets for KDE4
Summary(zh_CN): KDE 4 的一个彗星 OpenGL 屏幕保护程序
Group:          Amusements/Graphics
Group(zh_CN):	娱乐/图形
License:        GPLv2+
URL:            http://www.mehercule.net/staticpages/index.php/kcometen4
Source0:        http://www.mehercule.net/kcometen4/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  cmake
BuildRequires:  qt4-devel
BuildRequires:  kdebase4-workspace-devel

%description
KCometen4 is an OpenGL KDE screensaver. Inside a box is a nifty
light show that features lightning and exploding comets. It lets
you configure various effects like comet behavior, camera
movement, box face images, etc.

%description -l zh_CN
KDE 4 的一个彗星 OpenGL 屏幕保护程序。

%prep
%setup -q

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT -C %{_target_platform}
rm -rf $RPM_BUILD_ROOT%{kde4_mandir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1/
install -p -D -m 644 src/%{name}.kss.1 $RPM_BUILD_ROOT%{_mandir}/man1/
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING
%{_kde4_bindir}/%{name}.kss
%{_kde4_appsdir}/%{name}
%{_kde4_datadir}/kde4/services/ScreenSavers/%{name}.desktop
%{_mandir}/man1/%{name}.kss.1.gz

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 1.0.7-3
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.0.7-2
- 为 Magic 3.0 重建


