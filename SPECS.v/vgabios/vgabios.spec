Name:		vgabios
Version:	0.7a
Release:	2%{?dist}
Summary:	LGPL implementation of a vga video bios
Summary(zh_CN.UTF-8): vga 视频 bios 的 LGPL 实现

Group:		Applications/Emulators	
Group(zh_CN.UTF-8):	应用程序/模拟器	
License:	LGPLv2
URL:		http://www.nongnu.org/vgabios/
Source0:	http://savannah.gnu.org/download/%{name}/%{name}-%{version}.tgz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	dev86
BuildArch: noarch

%description
vgabios is an LPGL implementation of a bios for a video card.
It is tied to plex86/bochs, althoug it will likely work on other
emulators. It is not intended for use in real cards.

%description -l zh_CN.UTF-8
vga 视频 bios 的 LGPL 实现。

%prep 
%setup -q -n %{name}-%{version}

%build 
make clean
make biossums %{?_smp_mflags}
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/vgabios
install -m 0644 VGABIOS-lgpl-*.bin $RPM_BUILD_ROOT%{_datadir}/vgabios 


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%dir %{_datadir}/vgabios/
%doc README COPYING
%{_datadir}/vgabios/VGABIOS-lgpl-latest.bin
%{_datadir}/vgabios/VGABIOS-lgpl-latest.cirrus.bin
%{_datadir}/vgabios/VGABIOS-lgpl-latest.cirrus.debug.bin
%{_datadir}/vgabios/VGABIOS-lgpl-latest.debug.bin




%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.7a-2
- 为 Magic 3.0 重建

* Thu Nov 03 2011 Liu Di <liudidi@gmail.com> - 0.7a-1
- 更新到 0.7a
