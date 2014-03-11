# $Id: apt.spec 3053 2005-03-24 17:16:13Z dag $
# Authority: axel
# Upstream: Gustavo Niemeyer <niemeyer$conectiva,com>

%{?dist: %{expand: %%define %dist 1}}
%define LIBVER 3.3
%define magic_ver 3.0

Summary: Config used by apt-get
Summary(zh_CN.UTF-8): apt-get 的配置文件
Name: apt-config
Version: 0.5.15lorg3.95
Release: 1%{?dist}
License: GPL
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
URL: https://apt-rpm.org

Packager: Liu Di <liudidi@gmail.com>
Vendor: MagicGroup

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

Requires: apt >= %{version}

%description
config file used by apt-get.

%description -l zh_CN.UTF-8
apt-get 使用的配置文件。

%prep

%{__cat} <<EOF >magic.%{_target_cpu}.list
# Name: aptrpms
# URL: http://auvtech.com/~xinzhen/downloads/apt/

### MagicLinux %{magic_ver}

rpm http://apt.magiclinux.org:81/magic/%{magic_ver} %{_target_cpu} 3 9 a b c d e f g h i j k l lib m n o p q r s t texlive trinity u v w x y z A C D F G I J M N O P R S T W X
rpm-src http://apt.magiclinux.org:81/magic/%magic_ver} %{_target_cpu} 3 9 a b c d e f g h i j k l lib m n o p q r s t texlive trinity u v w x y z A C D F G I J M N O P R S T W X

rpm http://www.321211.net/apt/magic/%{magic_ver}  %{_target_cpu} 3 9 a b c d e f g h i j k l lib m n o p q r s t texlive trinity u v w x y z A C D F G I J M N O P R S T W X
rpm-src http://www.321211.net/apt/magic/%{magic_ver}  %{_target_cpu} 3 9 a b c d e f g h i j k l lib m n o p q r s t texlive trinity u v w x y z A C D F G I J M N O P R S T W X

rpm http://apt.linuxfans.org/magic/%{magic_ver}  %{_target_cpu} 3 9 a b c d e f g h i j k l lib m n o p q r s t texlive trinity u v w x y z A C D F G I J M N O P R S T W X
rpm-src http://apt.linuxfans.org/magic/%{magic_ver}  %{_target_cpu} 3 9 a b c d e f g h i j k l lib m n o p q r s t texlive trinity u v w x y z A C D F G I J M N O P R S T W X

EOF

%{__cat} <<'EOF' >apt.conf
APT {
	Clean-Installed "false";
	Get {
		Assume-Yes "false";
		Download-Only "false";
		Show-Upgraded "true";
		Fix-Broken "false";
		Ignore-Missing "false";
		Compile "false";
	};
};

Acquire {
	Retries "0";
	HTTP {
		Proxy ""; // http://user:pass@host:port/
	};
};

RPM {
	Ignore { };
	Hold { };
	Options { };
	Install-Options "";
	Erase-Options "";
//	Pre-Install-Pkgs { "/usr/bin/apt-sigchecker"; };
	Source {
		Build-Command "rpmbuild --rebuild";
	};
	Allow-Duplicated {
		"^kernel$";
		"^kernel-";
		"^gpg-pubkey$";
		"^jdk$";
	};
};
EOF

%build
%{__rm} -rf %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/apt/sources.list.d/
%{__install} -p -m0644 apt.conf %{buildroot}%{_sysconfdir}/apt/
%{__install} -p -m0644 magic.%{_target_cpu}.list %{buildroot}%{_sysconfdir}/apt/sources.list.d/

%post

%postun

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%config(noreplace) %{_sysconfdir}/apt/apt.conf
%config(noreplace) %{_sysconfdir}/apt/sources.list.d/

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.5.15lorg3.95-0.2
- 为 Magic 3.0 重建

* Sun Oct 30 2011 Liu Di <liudidi@gmail.com> - 0.5.15lorg3.94-6
- 升级到 Magic 3.0

* Fri Apr 06 2007 Liu Di <liudidi@gmail.com> - 0.5.15lorg3.90-3mgc
- Initial package. 
