Name:    kyum
Version: 0.7.5
Release: 1%{?dist}

Summary: Graphical User Frontend (GUI) for yum
Summary(zh_CN.UTF-8): yum 的图形化前端

License: GPL
Group:   Applications/System
Group(zh_CN.UTF-8):	应用程序/系统
URL:     http://kde-apps.org/content/show.php?content=22185
Source:	 http://www-users.rwth-aachen.de/Steffen.Offermann/Download/%{name}-%{version}.tar.gz
Patch0: kyum-0.7.5-admin.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

Requires: yum >= 2.2.0
Requires: kdebase
Requires: python

BuildRequires: kdelibs-devel
BuildRequires: automake
BuildRequires: desktop-file-utils

%description
KYum is a graphical user frontend (GUI) for yum.
You can use it to modify your repository files and
to control the most common operations of yum.

This version is an emergency bug-fix for v0.7.4.

%description -l zh_CN.UTF-8
yum 的图形化前端。

%prep
%setup -q
%patch0 -p1
chmod 777 admin/*

%build
[ -n "$QTDIR" ] || . %{_sysconfdir}/profile.d/qt.sh
 
make -f Makefile.cvs
%configure --disable-rpath 
sed -i 's/fno-exceptions/fexceptions/g' src/Makefile
#临时措施
sed -i 's/\/include\/tqt/\/include\/tqt \-lqt\-mt \-ltdecore \-ltdeui \-ltdeprint \-lDCOP \-lkio/g' src/Makefile
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall 

# mkdir -p $RPM_BUILD_ROOT%{_datadir}/applnk/Utilities
desktop-file-install --delete-original \
  --vendor magic             \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications/kde  \
  --mode 0644                                    \
  $RPM_BUILD_ROOT%{_datadir}/app*/*/%{name}.desktop
 
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/*
%dir %{_datadir}/apps/kyum
%{_datadir}/apps/kyum/*/*
%{_datadir}/apps/kyum/kyum_sysinfo.p*
%{_datadir}/apps/kyum/kyumui.rc
%{_datadir}/icons/*/*/apps/kyum.png
%{_datadir}/applications/kde/magic-kyum.desktop
%lang(en) %doc %{_docdir}/HTML/en/kyum/*
%doc ChangeLog COPYING README AUTHORS

%changelog

