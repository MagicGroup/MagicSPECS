%define name audacious-plugins
%define summary Audacious-Plugins
%define version 3.4.3
%define testver %{nil}
%if 0%{testver}
%define release 0.%{testver}.1%{?dist}.3
%else
%define release 1%{?dist}
%endif

%define plugindir %(pkg-config audacious --variable=plugin_dir)

Name:		%{name}
Summary:	%{summary}
Summary(zh_CN.UTF-8):	Audacious 的插件
Version:	%{version}
Release:	%{release}
%if 0%{testver}
Source:		http://distfiles.atheme.org/%{name}-%{version}-%{testver}.tar.bz2
%else
Source:		http://distfiles.audacious-media-player.org/audacious-plugins-%{version}.tar.bz2
%endif

Group:		Applications/Multimedia
Group(zh_CN.UTF-8):	应用程序/多媒体
URL:		http://www.audacious-media-player.org/
License:	GPL
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	audacious-devel = %{version}

Requires:	audacious = %{version}

%description
Offical Plugins of Audacious

%description -l zh_CN.UTF-8
Audacious 的官方插件包

%prep
%if 0%{testver}
%setup -q -n %{name}-%{version}-%{testver}
%else
%setup -q
%endif

%build
%configure CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" 
make  %{?_smp_mflags} OPTIMIZE="%{optflags}"

%install
rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=$RPM_BUILD_ROOT install
magic_rpm_clean.sh

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir} 

%files
%defattr(-, root, root)
%doc AUTHORS COPYING INSTALL
#%{_bindir}/aud*
%{plugindir}/*
%{_datadir}/audacious/*
%{_datadir}/locale/*

%changelog
* Sun Mar 02 2014 Liu Di <liudidi@gmail.com> - 3.4.3-1
- 更新到 3.4.3

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 3.3.2-1
- 为 Magic 3.0 重建

* Tue Dec 04 2012 Liu Di <liudidi@gmail.com> - 3.3.2-1
- 为 Magic 3.0 重建

* Mon Dec 03 2012 Liu Di <liudidi@gmail.com> - 3.3.2-1
- 为 Magic 3.0 重建

* Tue Nov 01 2011 Liu Di <liudidi@gmail.com> - 3.1-0.beta3.1
- 更新到 3.1 beta3

* Sun Mar  4 2007 Jiang Tao <jiangtao9999@163.com> - 1.3.0
- Create and build for MagicLinux
