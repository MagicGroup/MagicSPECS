Name: wqy-zenhei
Version: 0.9.45
Release: 2%{?dist}
Summary(zh_CN.UTF-8): 文泉驿正黑体
License: GPL
Group:         User Interface/X
Group(zh_CN.UTF-8): 用户界面/X
Source: http://jaist.dl.sourceforge.net/sourceforge/wqy/wqy-zenhei-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Url: http://wqy.sourceforge.net
Packager: haulm<haulm@126.com>
Autoreqprov: no
BuildArch: noarch

Provides: %{name}-fonts = %{version}

%description
wqy-zenhei-nightly_build
%description -l zh_CN.UTF-8
文泉驿正黑体

%prep
%setup -q -n %{name}

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/share/fonts/ttf/zh_CN
cp -p $RPM_BUILD_DIR/%{name}/wqy-zenhei.ttc $RPM_BUILD_ROOT/usr/share/fonts/ttf/zh_CN
mkdir -p $RPM_BUILD_ROOT/etc/fonts/conf.{avail,d}
cp -p $RPM_BUILD_DIR/%{name}/44-wqy-zenhei.conf $RPM_BUILD_ROOT/etc/fonts/conf.avail
cd $RPM_BUILD_ROOT/etc/fonts/conf.d
ln -s ../conf.avail/*.conf ./
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post
fc-cache -fv

%postun
fc-cache -fv

%files
%defattr(-,root,root)
%{_datadir}/fonts/ttf/zh_CN/wqy-zenhei.ttc
%{_sysconfdir}/fonts/conf.*/*.conf

%changelog
* Wed Nov 30 2011 Liu Di <liudidi@gmail.com> - 0.9.45-2
- 为 Magic 3.0 重建

* Wed Apr 02 2008 Liu Di <liudidi@gmail.com> - 0.5.23-1mgc
- update to 0.5.23

* Sun Feb 10 2008 haulm <haulm@126.com> - 0.4.23-1mgc
-  wyq-zhen-0.4.23 instead uming.ttf
