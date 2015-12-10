Summary: Command line tool for setting up authentication from network services
Summary(zh_CN.UTF-8): 从网络服务上设置认证的命令行工具
Name: authconfig
Version: 6.2.10
Release: 3%{?dist}
License: GPLv2+
ExclusiveOS: Linux
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
URL: https://fedorahosted.org/authconfig
Source: https://fedorahosted.org/releases/a/u/%{name}/%{name}-%{version}.tar.bz2
Requires: newt-python, pam >= 0.99.10.0, python
Conflicts: pam_krb5 < 1.49, samba-common < 3.0, samba-client < 3.0
Conflicts: nss_ldap < 254, sssd < 0.99.1
BuildRequires: glib2-devel, python >= 2.6, python-devel
BuildRequires: desktop-file-utils, intltool, gettext, perl-XML-Parser

%description 
Authconfig is a command line utility which can configure a workstation
to use shadow (more secure) passwords.  Authconfig can also configure a
system to be a client for certain networked user information and
authentication schemes.

%description -l zh_CN.UTF-8
这是一个可以配置工作站使用影子密码的命令行工具。

%package gtk
Summary: Graphical tool for setting up authentication from network services
Summary(zh_CN.UTF-8): %{name} 的 gtk 前端
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
Requires: %{name} = %{version}-%{release}, pygtk2-libglade >= 2.14.0
Requires: usermode-gtk, hicolor-icon-theme

%description gtk
Authconfig-gtk is a GUI program which can configure a workstation
to use shadow (more secure) passwords.  Authconfig-gtk can also configure
a system to be a client for certain networked user information and
authentication schemes.

%description gtk -l zh_CN.UTF-8
%{name} 的 gtk 前端。

%prep
%setup -q -n %{name}-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS -fPIC"; export CFLAGS
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{python_sitearch}/acutil.*a
rm $RPM_BUILD_ROOT/%{_datadir}/%{name}/authconfig-tui.py
ln -s authconfig.py $RPM_BUILD_ROOT/%{_datadir}/%{name}/authconfig-tui.py
magic_rpm_clean.sh
%find_lang %{name}
find $RPM_BUILD_ROOT%{_datadir} -name "*.mo" | xargs ./utf8ify-mo

%clean
rm -rf $RPM_BUILD_ROOT

%post gtk
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun gtk
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans gtk
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%triggerin -- authconfig <= 5.4.9
authconfig --update --nostart >/dev/null 2>&1 || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING NOTES TODO README.samba3
%ghost %config(noreplace) %{_sysconfdir}/sysconfig/authconfig
%ghost %config(noreplace) %{_sysconfdir}/pam.d/system-auth-ac
%ghost %config(noreplace) %{_sysconfdir}/pam.d/password-auth-ac
%ghost %config(noreplace) %{_sysconfdir}/pam.d/fingerprint-auth-ac
%ghost %config(noreplace) %{_sysconfdir}/pam.d/smartcard-auth-ac
%ghost %config(noreplace) %{_sysconfdir}/pam.d/postlogin-ac
%{_sbindir}/cacertdir_rehash
%{_sbindir}/authconfig
%{_sbindir}/authconfig-tui
%exclude %{_mandir}/man8/system-config-authentication.*
%exclude %{_mandir}/man8/authconfig-gtk.*
%{_mandir}/man8/*
%{_mandir}/man5/*
%{_libdir}/python*/site-packages/acutil.so
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/authconfig.py*
%{_datadir}/%{name}/authconfig-tui.py*
%{_datadir}/%{name}/authinfo.py*
%{_datadir}/%{name}/shvfile.py*
%{_datadir}/%{name}/dnsclient.py*
%{_datadir}/%{name}/msgarea.py*
%attr(700,root,root) %dir %{_localstatedir}/lib/%{name}

%files gtk
%defattr(-,root,root,-)
%{_bindir}/authconfig
%{_bindir}/authconfig-tui
%{_bindir}/authconfig-gtk
%{_bindir}/system-config-authentication
%{_sbindir}/authconfig-gtk
%{_sbindir}/system-config-authentication
%{_mandir}/man8/system-config-authentication.*
%{_mandir}/man8/authconfig-gtk.*
%{_datadir}/%{name}/authconfig.glade
%{_datadir}/%{name}/authconfig-gtk.py*
%config(noreplace) %{_sysconfdir}/pam.d/authconfig-gtk
%config(noreplace) %{_sysconfdir}/pam.d/system-config-authentication
%config(noreplace) %{_sysconfdir}/security/console.apps/authconfig-gtk
%config(noreplace) %{_sysconfdir}/security/console.apps/system-config-authentication
%config(noreplace) %{_sysconfdir}/pam.d/authconfig
%config(noreplace) %{_sysconfdir}/pam.d/authconfig-tui
%config(noreplace) %{_sysconfdir}/security/console.apps/authconfig
%config(noreplace) %{_sysconfdir}/security/console.apps/authconfig-tui
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/16x16/apps/system-config-authentication.*
%{_datadir}/icons/hicolor/22x22/apps/system-config-authentication.*
%{_datadir}/icons/hicolor/24x24/apps/system-config-authentication.*
%{_datadir}/icons/hicolor/32x32/apps/system-config-authentication.*
%{_datadir}/icons/hicolor/48x48/apps/system-config-authentication.*
%{_datadir}/icons/hicolor/256x256/apps/system-config-authentication.*

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 6.2.10-3
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 6.2.10-2
- 更新到 6.2.10

* Sun Mar 02 2014 Liu Di <liudidi@gmail.com> - 6.2.8-1
- 更新到 6.2.8

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 6.1.16-2
- 为 Magic 3.0 重建

* Tue Nov 01 2011 Liu Di <liudidi@gmail.com> - 6.1.16-1
- 为 Magic 3.0 重建

