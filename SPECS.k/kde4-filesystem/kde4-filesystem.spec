Summary: KDE filesystem layout
Summary(zh_CN.UTF-8): KDE4 的文件系统结构
Name: kde4-filesystem
Version: 4
Release: 47%{?dist}

Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
License: Public Domain
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: kde4-rpm-config
# noarch->arch transition
Obsoletes: kde-filesystem < 4-36

# teamnames (locales) borrowed from kde-i18n packaging
Source1: teamnames

Source3: applnk-hidden-directory

BuildRequires: gawk

Requires:  filesystem
Requires:  rpm

%description
This package provides some directories that are required/used by KDE. 

%description -l zh_CN.UTF-8
这个包提供了 KDE4 需要并使用的一些目录。

%prep


%build


%install
rm -f $RPM_BUILD_DIR/%{name}.list
rm -rf $RPM_BUILD_ROOT

# 不使用 KDE3 了，以 TDE 代替，有单独的 tde-filesystem
## KDE3 
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/kde/{env,shutdown,kdm}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/{applications/kde,applnk,apps,autostart,config,config.kcfg,emoticons,mimelnk,services,servicetypes,templates,source}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/apps/konqueror/servicemenus
# not sure who best should own locolor, so we'll included it here, for now. -- Rex
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/locolor/{16x16,22x22,32x32,48x48}/{actions,apps,mimetypes}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applnk/{.hidden,Applications,Edutainment,Graphics,Internet,Settings,System,Toys,Utilities}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/mimelnk/{all,application,audio,fonts,image,inode,interface,media,message,model,multipart,print,text,uri,video}
# do qt3 too?
# mkdir -p $RPM_BUILD_ROOT%{_prefix}/{lib,%{_lib}}/qt-3.3/plugins
mkdir -p $RPM_BUILD_ROOT%{_prefix}/{lib,%{_lib}}/kde3/plugins
mkdir -p $RPM_BUILD_ROOT%{_docdir}/HTML/en

for locale in $(grep '=' %{SOURCE1} | awk -F= '{print $1}') ; do
 mkdir -p $RPM_BUILD_ROOT%{_docdir}/HTML/${locale}/common
 # do docs/common too, but it could be argued that apps/pkgs using or
 # depending on is a bug -- Rex
 mkdir -p $RPM_BUILD_ROOT%{_docdir}/HTML/${locale}/docs/
 ln -s ../common $RPM_BUILD_ROOT%{_docdir}/HTML/${locale}/docs/common
 echo "%lang($locale) %{_docdir}/HTML/$locale/" >> %{name}.list
done

# internal services shouldn't be displayed in menu
install -p -m644 -D %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/applnk/.hidden/.directory

## KDE4
mkdir -p $RPM_BUILD_ROOT%{_kde4_sysconfdir}/kde/{env,shutdown,kdm} \
         $RPM_BUILD_ROOT%{_kde4_includedir} \
         $RPM_BUILD_ROOT%{_kde4_libexecdir} \
         $RPM_BUILD_ROOT%{_kde4_appsdir}/color-schemes \
         $RPM_BUILD_ROOT%{_kde4_datadir}/applications/kde4 \
         $RPM_BUILD_ROOT%{_kde4_datadir}/{autostart,wallpapers} \
         $RPM_BUILD_ROOT%{_kde4_configdir} \
         $RPM_BUILD_ROOT%{_kde4_sharedir}/config.kcfg \
         $RPM_BUILD_ROOT%{_kde4_sharedir}/emoticons \
         $RPM_BUILD_ROOT%{_kde4_sharedir}/kde4/services/ServiceMenus \
         $RPM_BUILD_ROOT%{_kde4_sharedir}/kde4/servicetypes \
         $RPM_BUILD_ROOT%{_kde4_sharedir}/templates/.source \
         $RPM_BUILD_ROOT%{_kde4_datadir}/icons/locolor/{16x16,22x22,32x32,48x48}/{actions,apps,mimetypes} \
         $RPM_BUILD_ROOT%{_kde4_docdir}/HTML/en/common
# do qt4 too?
# mkdir -p $RPM_BUILD_ROOT%{_prefix}/{lib,%{_lib}}/qt4/plugins
mkdir -p $RPM_BUILD_ROOT%{_kde4_prefix}/{lib,%{_lib}}/kde4/plugins/{gui_platform,styles}

for locale in $(grep '=' %{SOURCE1} | awk -F= '{print $1}') ; do
  mkdir -p $RPM_BUILD_ROOT%{_kde4_docdir}/HTML/${locale}/common
  echo "%lang($locale) %{_kde4_docdir}/HTML/$locale/" >> %{name}.list
done

%clean
rm -rf $RPM_BUILD_ROOT %{name}.list


%files -f %{name}.list
%defattr(-,root,root,-)

# KDE3
%{_sysconfdir}/kde/
%{_datadir}/applications/kde/
%{_datadir}/applnk/
%{_datadir}/apps/
%{_datadir}/autostart/
%{_datadir}/config/
%{_datadir}/config.kcfg/
%{_datadir}/emoticons/
%{_datadir}/icons/locolor
%{_datadir}/mimelnk/
%{_datadir}/services/
%{_datadir}/servicetypes/
%{_datadir}/templates/
%{_prefix}/lib/kde3/
%{_prefix}/%{_lib}/kde3/
%dir %{_docdir}/HTML/
%lang(en) %{_docdir}/HTML/en/

# KDE4
%{_kde4_sysconfdir}/kde/
%{_kde4_libexecdir}/
%{_kde4_includedir}/
%{_kde4_appsdir}/
%{_kde4_configdir}/
%{_kde4_sharedir}/config.kcfg/
%{_kde4_sharedir}/emoticons/
%{_kde4_sharedir}/kde4/
%{_kde4_sharedir}/templates/
%{_kde4_datadir}/applications/kde4/
%{_kde4_datadir}/autostart/
%{_kde4_datadir}/icons/locolor/
%{_kde4_datadir}/wallpapers/
%{_kde4_prefix}/lib/kde4/
%{_kde4_prefix}/%{_lib}/kde4/
%dir %{_kde4_docdir}/HTML/
%lang(en) %{_kde4_docdir}/HTML/en/


%changelog
* Fri May 23 2014 Liu Di <liudidi@gmail.com> - 4-47
- 为 Magic 3.0 重建


