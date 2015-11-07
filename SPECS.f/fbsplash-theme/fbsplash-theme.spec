%define THEME_NAME butter
%define THEME_VER 0.0.1
%define THEME_REL 4%{?dist}

Name:				fbsplash-theme-%{THEME_NAME}
Version:			%{THEME_VER}
Release:			%{THEME_REL}.2
BuildArch:			noarch

Source:				%{THEME_NAME}.tar.bz2


Summary:			%{name} - Fbsplash theme
Summary(zh_CN.UTF-8):			%{name} - 一个 Fbsplash 的主题

#URL:				http://

Group:				Applications/Graphics
Group(zh_CN.UTF-8):			应用程序/图形

Packager:			Jiang Tao <jiangtao9999@163.com>

Distribution:			Magic Linux 2.1
License:			AS-IS
BuildRoot:			%{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)

%description
It is a Fbsplash theme.

%description -l zh_CN.UTF-8
一个 Fbsplash 的主题。

%prep

%setup -q -n %{THEME_NAME}
mkdir -p %{buildroot}/etc/splash/%{THEME_NAME}
cp -fr * %{buildroot}/etc/splash/%{THEME_NAME}
cd %{buildroot}/etc/splash
#ln -s %{THEME_NAME} default

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root)
/etc/splash/*

