Name:       fbterm
Version:    1.7
Release:    4%{?dist}
License:    GPLv2+
Group:      Applications/System
Group(zh_CN.UTF-8):	应用程序/系统
URL:        http://code.google.com/p/fbterm/
Source0:    http://fbterm.googlecode.com/files/%{name}-%{version}.0.tar.gz
#Patch0:     %{name}-1.2-kernel-header.patch
#Patch1:     %{name}-1.3-setcap.patch
Patch2:	    %{name}-1.4-iminput.patch
Summary:    A frame buffer terminal emulator
Summary(zh_CN.UTF-8): 运行在帧缓冲的快速终端仿真器


BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: fontconfig-devel gpm-devel
Requires: fontconfig

%description
FbTerm is a fast terminal emulator for linux with frame buffer device. 
Features include: 
- mostly as fast as terminal of linux kernel while accelerated scrolling
  is enabled on framebuffer device 
- select font with fontconfig and draw text with freetype2, same as 
  Qt/Gtk+ based GUI apps 
- dynamicly create/destroy up to 10 windows initially running default
  shell 
- record scrollback history for every window 
- auto-detect text encoding with current locale, support double width 
  scripts like  Chinese, Japanese etc 
- switch between configurable additional text encodings with hot keys
  on the fly 
- copy/past selected text between windows with mouse when gpm server 
  is running

%description -l zh_CN.UTF-8
运行在帧缓冲的快速终端仿真器。

%prep
%setup -q 
#%patch0 -p0 -b .kernel-header
#%patch1 -p0 -b .setcap
#%patch2 -p0 -b .iminput

%build
# --disable-static --disable-rpath
%configure || make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} install
chmod 755 $RPM_BUILD_ROOT/%{_bindir}/%{name}
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post
setcap 'cap_sys_tty_config+ep' %{_bindir}/%{name}


%files 
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz


%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 1.7-4
- 为 Magic 3.0 重建

* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 1.7-3
- 为 Magic 3.0 重建

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 1.7-2
- 为 Magic 3.0 重建


