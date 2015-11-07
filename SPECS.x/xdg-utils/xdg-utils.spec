
#define vcsdate %{nil}
#define pre rc1

Summary: Basic desktop integration functions 
Summary(zh_CN.UTF-8): 基本的桌面集成功能
Name:    xdg-utils
Version:	1.1.1
Release:	2%{?dist}

URL:     http://portland.freedesktop.org/ 
%if 0%{?vcsdate:1}
Source0: xdg-utils-%{version}-%{vcsdate}git.tar.gz
Source1: xdg-utils-git_checkout.sh
%else
Source0: http://portland.freedesktop.org/download/xdg-utils-%{version}%{?pre:-%{pre}}.tar.gz
%endif
License: MIT 
Group:   System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

%if 0%{?vcsdate}
BuildRequires: gawk
BuildRequires: xmlto
%endif

Requires: coreutils
Requires: desktop-file-utils
Requires: which

%description
The %{name} package is a set of simple scripts that provide basic
desktop integration functions for any Free Desktop, such as Linux.
They are intended to provide a set of defacto standards.  
This means that:
*  Third party software developers can rely on these xdg-utils
   for all of their simple integration needs.
*  Developers of desktop environments can make sure that their
   environments are well supported
*  Distribution vendors can provide custom versions of these utilities

The following scripts are provided at this time:
* xdg-desktop-icon      Install icons to the desktop
* xdg-desktop-menu      Install desktop menu items
* xdg-email             Send mail using the user's preferred e-mail composer
* xdg-icon-resource     Install icon resources
* xdg-mime              Query information about file type handling and
                        install descriptions for new file types
* xdg-open              Open a file or URL in the user's preferred application
* xdg-screensaver       Control the screensaver
* xdg-settings          Get various settings from the desktop environment

%description -l zh_CN.UTF-8
基本的桌面集成功能。

%prep
%setup -q -n %{name}-%{version}%{?pre:-%{pre}}


%build
%configure

%if 0%{?vcsdate:1}
make scripts-clean -C scripts 
make man scripts %{?_smp_mflags} -C scripts
%endif
make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}
magic_rpm_clean.sh

%files
%defattr(-,root,root,-)
%doc ChangeLog LICENSE README TODO
%{_bindir}/xdg-desktop-icon
%{_bindir}/xdg-desktop-menu
%{_bindir}/xdg-email
%{_bindir}/xdg-icon-resource
%{_bindir}/xdg-mime
%{_bindir}/xdg-open
%{_bindir}/xdg-screensaver
%{_bindir}/xdg-settings
%{_mandir}/man1/xdg-desktop-icon.1*
%{_mandir}/man1/xdg-desktop-menu.1*
%{_mandir}/man1/xdg-email.1*
%{_mandir}/man1/xdg-icon-resource.1*
%{_mandir}/man1/xdg-mime.1*
%{_mandir}/man1/xdg-open.1*
%{_mandir}/man1/xdg-screensaver.1*
%{_mandir}/man1/xdg-settings.1*


%clean
rm -rf %{buildroot}


%changelog
* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 1.1.1-2
- 为 Magic 3.0 重建

* Thu Oct 22 2015 Liu Di <liudidi@gmail.com> - 1.1.1-1
- 更新到 1.1.1

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.1.0-0.12.20111207
- 为 Magic 3.0 重建


