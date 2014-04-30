Name: kdocker
Summary: Dock any application in the system tray
Summary(zh_CN): 将任何程序停靠在系统托盘
Version: 1.3
Release: 2%{?dist}
Group: User Interface/Desktops
Group(zh_CN): 用户界面/桌面
License: GPL
Source0: http://dl.sourceforge.net/sourceforge/kdocker/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
URL: http://kdocker.sourceforge.net/
Packager: Ni Hui <shuizhuyuanluo@126.com>
BuildRequires: qt-devel

# 调整安装路径的补丁
Patch1: kdocker-1.3-paths.patch

%description
KDocker will help you dock any application in the system tray. This means you
can dock openoffice, xmms, firefox, thunderbolt, eclipse, anything!

KDocker supports the KDE System Tray Protocol and the System Tray Protocol from
freedesktop.org

It works for KDE, GNOME, XFCE, and probably many more.

%description -l zh_CN
KDocker 帮助您停靠任何程序至系统托盘。这意味着您可以停靠 openoffice、xmms、firefox、thunderbolt、eclipse 和任何东西！

KDocker 支持 KDE 系统托盘协议和来自 freedesktop.org 的系统托盘

它能够在 KDE、GNOME、XFCE 桌面下运行，或许更多。

%prep
%setup -q -n %{name}

%patch1 -p1 -b .paths

%build
. /etc/profile.d/qt.sh

%{_bindir}/qmake
# Not smp safe
%{__make}

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install

desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --vendor="" \
  %{buildroot}%{_datadir}/applications/*.desktop

# remove dup'd docs
%{__rm} -rf %{buildroot}%{_datadir}/kdocker/docs
ln -s %{_docdir}/%{name}-%{version} %{buildroot}%{_datadir}/kdocker/docs

# %lang'ify i18n bits
echo "%dir %{_datadir}/kdocker/i18n/" >> %{name}.lang
for lang_bit in %{buildroot}%{_datadir}/kdocker/i18n/*.qm ; do
  if [ -f $lang_bit ]; then
    lang_file=$(basename $lang_bit)
    lang=$(echo $lang_file .qm | cut -d_ -f2)
    echo "%lang($lang) %{_datadir}/kdocker/i18n/$lang_file" >> %{name}.lang
  fi
done

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS BUGS COPYING CREDITS ChangeLog HACKING README TODO VERSION
%{_bindir}/*
%dir %{_datadir}/kdocker/
%{_datadir}/kdocker/docs
%{_datadir}/kdocker/icons/
%{_datadir}/applications/*.desktop

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.3-2
- 为 Magic 3.0 重建

* Fri Aug 10 2007 Ni Hui <shuizhuyuanluo@126.com> - 1.3-0.1mgc
- initialize the first spec file for MagicLinux-2.1
