Name:           recordmydesktop
Version:        0.3.8.1
Release:        6%{?dist}
Summary:        Desktop session recorder with audio and video
Summary(zh_CN.UTF-8): 带有视频和音频的桌面会话记录器

Group:          Applications/Multimedia
Group(zh_CN.UTF-8):	应用程序/多媒体
License:        GPL
URL:            http://recordmydesktop.sourceforge.net/
Source0:        http://dl.sourceforge.net/recordmydesktop/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libXdamage-devel, libSM-devel
BuildRequires:  libXext-devel
BuildRequires:  alsa-lib-devel, zlib-devel
BuildRequires:  libtheora-devel, libvorbis-devel


%description
recordMyDesktop is a desktop session recorder for linux that attempts to be 
easy to use, yet also effective at it's primary task.

As such, the program is separated in two parts; a simple command line tool that
performs the basic tasks of capturing and encoding and an interface that 
exposes the program functionality in a usable way.

%description -l zh_CN.UTF-8
带有视频和音频的桌面会话记录器。

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -c -p"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README ChangeLog
%{_bindir}/*
%{_mandir}/man?/*


%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.3.8.1-6
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.3.8.1-5
- 为 Magic 3.0 重建

* Sat Sep 12 2015 Liu Di <liudidi@gmail.com> - 0.3.8.1-4
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.3.8.1-3
- 为 Magic 3.0 重建

* Fri Dec 09 2011 Liu Di <liudidi@gmail.com> - 0.3.8.1-2
- 为 Magic 3.0 重建


