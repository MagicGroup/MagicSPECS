Name:           915resolution
Version:        0.5.3
Release:        7%{?dist}
Summary:        Intel video BIOS hack to support certain resolutions 
Summary(zh_CN.UTF-8): Intel视频BIOS改进以支持特定分辨率

Group:          User Interface/X Hardware Support 
Group(zh_CN.UTF-8): 	用户界面/X 硬件支持
License:        Public Domain 
URL:            http://915resolution.mango-lang.org
#此地址被墙
#Source0:        http://915resolution.mango-lang.org//%{name}-%{version}.tar.gz
Source0:	%{name}-%{version}.tar.gz
Source1:        %{name}.service
Source2:        %{name}-config
Source3:        %{name}-pm-hook

# 支持更多的芯片组
Patch0:         965GM.patch
Patch1:         E7221.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# this doesn't make much sense on ppc.  That, and it fails to build :)
ExcludeArch:    ppc ppc64 mips mips64el

# 简单介绍
Source100:      README.magic

# 添加和移除服务需要
Requires(post):   /sbin/chkconfig
Requires(preun):  /sbin/chkconfig
Requires(preun):  /sbin/service


%description
915resolution is a tool to modify the video BIOS of the 800 and 900 series
Intel graphics chipsets. This includes the 845G, 855G, and 865G chipsets, as
well as 915G, 915GM, and 945G chipsets. This modification is necessary to
allow the display of certain graphics resolutions for an Xorg or XFree86
graphics server.

915resolution's modifications of the BIOS are transient. There is no risk of
permanent modification of the BIOS. This also means that 915resolution must be
run every time the computer boots inorder for it's changes to take effect.

915resolution is derived from the tool 855resolution. However, the code
differs substantially. 915resolution's code base is much simpler.
915resolution also allows the modification of bits per pixel. 

%description -l zh_CN.UTF-8
915resolution是一个修改Intel 800和900系列显卡BIOS的工具。这包括845G, 855G和
865G芯片及915G, 915GM和945G芯片。这些修改对于Xorg或XFree86显示特定的分辨率
是必需的。
 
915resolution对BIOS的修改是暂时的，没有永久修改BIOS的风险。这也意味着必须在
每次计算机启动的时候都运行915resolution以使更改生效。
 
915resolution是源自855resolution。然而，代码已经充分不同了。915resolution的
代码更简化。
 
915resolution也允许修改显示色深。

%prep
%setup -q 
%patch0 -p1
%patch1 -p1

# keep rpmlint from complaining....
chmod -x dump_bios

cp %{SOURCE100} .

%build
make clean
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sbindir}
cp %{name} %{buildroot}%{_sbindir}

# ...and the associated support bits
mkdir -p %{buildroot}%{_unitdir}
install -m 0755 -T %{SOURCE1} \
    %{buildroot}%{_unitdir}/915resolution.service
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 0644 -T %{SOURCE2} \
    %{buildroot}%{_sysconfdir}/sysconfig/915resolution
mkdir -p %{buildroot}%{_sysconfdir}/pm/sleep.d
install -m 0755 -T %{SOURCE3} \
    %{buildroot}%{_sysconfdir}/pm/sleep.d/99resolution

magic_rpm_clean.sh
%clean
rm -rf %{buildroot}


%post
# This adds the proper /etc/rc*.d links for the script
/usr/bin/systemctl enable 915resolution.service


%preun
if [ $1 = 0 ]; then
    /usr/bin/systemctl stop 915resolution  || :
    /usr/bin/systemctl disable 915resolution.service
fi

# no postun scriptlet is provided to "restart" the service on upgrade as this
# doesn't seem entirely appropriate.  explanations as to why this is wrong are
# welcome :)

%files
%defattr(-,root,root,-)
%doc LICENSE.txt README* changes.log chipset_info.txt dump_bios
%{_sbindir}/*
%{_unitdir}/*
%{_sysconfdir}/pm/sleep.d/*
%config(noreplace) %{_sysconfdir}/sysconfig/*


%changelog
* Sat May 11 2013 Liu Di <liudidi@gmail.com> - 0.5.3-6
- 重新编译

* Sat May 11 2013 Liu Di <liudidi@gmail.com> - 0.5.3-5
- 重新编译

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.5.3-4
- 为 Magic 3.0 重建

* Tue Oct 18 2011 Liu Di <liudidi@gmail.com> - 0.5.3-3
- 修改 spec 编码为 UTF-8
- 修改软件网址，已被墙。

* Thu Oct 30 2008 Liu Di <liudidi@gmail.com> - 0.5.3-1mgc
- 更新到 0.5.3

* Mon Oct 09 2006 Liu Di <liudidi@gmail.com> - 0.5.2-1mgc
- Initial package.
