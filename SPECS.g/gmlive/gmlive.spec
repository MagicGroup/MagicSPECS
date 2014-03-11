Name:		gmlive
Group:		Applications/Internet
Group(zh_CN.UTF-8):   应用程序/互联网
Version:	0.22.3
Release:	2%{?dist}
License:	GPL
Summary:	A P2P Stream program
Summary(zh_CN.UTF-8): P2P流媒体程序
URL:		http://code.google.com/p/gmlive
Source0:	http://gmlive.googlecode.com/files/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	gtkmm24-devel

Requires:	sopcast
#已失效，等待更新
#Requires:	xpplive
#Requires:	xpps

%description
A P2P Stream program

%description -l zh_CN.UTF-8
P2P流媒体程序的前端，支持 sopcast, pplive, ppstream。

%prep
rm -rf $RPM_BUILD_ROOT
%setup -q 

%build
%configure
%{__make} %{?_smp_mflags}

%install
%makeinstall
magic_rpm_clean.sh
pushd %{buildroot}%{_bindir}
mv %{name} %{name}.utf8
cat > %name << EOF
#!/bin/bash
LANG=zh_CN.UTF-8 %{name}.utf8
EOF
chmod 755 %{name}
popd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-,root,root)
%{_bindir}/%{name}*
%{_datadir}/applications/gmlive.desktop
%{_datadir}/%{name}/*
%{_datadir}/locale/*
%{_datadir}/pixmaps/gmlive.png

%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 0.22.3-2
- 为 Magic 3.0 重建


