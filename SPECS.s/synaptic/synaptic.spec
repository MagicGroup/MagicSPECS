%define desktop_vendor magic

%undefine _hardened_build

Summary: Graphical frontend for APT package manager.
Summary(zh_CN.UTF-8): APT 包管理器的图形界面
Name: synaptic
Version: 0.57.2
Release: 6%{?dist}

License: GPLv2+
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Source0: http://savannah.nongnu.org/download/synaptic/synaptic-%{version}.tar.gz
Patch0: synaptic-0.57-desktop.patch
Patch1: synaptic-0.57-firefox.patch
# Patches from apt-rpm maintainer for gcc 4.1 support, repomd support
# and progress meter fixes
Patch2: http://apt-rpm.org/patches/synaptic-0.57.2-gcc41.patch
Patch3: http://apt-rpm.org/patches/synaptic-0.57.2-repomd-1.patch
Patch4: http://apt-rpm.org/patches/synaptic-0.57.2-showprog.patch
Patch5: http://apt-rpm.org/patches/synaptic-0.57.2-progressapi-hack.patch
Patch6: synaptic-0.57.2-gcc43.patch
Patch7: synaptic-0.57.2-libx11.patch
Patch8: synaptic-0.57.2-gcc45.patch
Patch9: synaptic-0.57.2-format-security.patch
URL: http://www.nongnu.org/synaptic/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: usermode-gtk
Requires(post): scrollkeeper
Requires(postun): scrollkeeper
BuildRequires: apt-devel >= 0.5.15lorg3.92, rpm-devel >= 4.0
BuildRequires: gtk2-devel, libglade2-devel, desktop-file-utils
BuildRequires: libstdc++-devel, gettext
BuildRequires: xmlto, perl-XML-Parser
BuildRequires: scrollkeeper

%description
Synaptic is a graphical package management
program for apt. It provides the same features as the apt-get command line
utility with a GUI front-end based on Gtk+

%description -l zh_CN.UTF-8
Synaptic 是一个 apt 的图形化包管理程序。
它提供和命令行下 apt-get 工具一样的特性，基于 Gtk+。

%prep
%setup -q
%patch0 -p1 -b .dt
%patch1 -p1 -b .firefox
%patch2 -p1 -b .gcc41
%patch3 -p1 -b .repomd
%patch4 -p1 -b .showprog
%patch5 -p1 -b .progresshack
%patch6 -p1 -b .gcc43
%patch7 -p1
%patch8 -p1
%patch9 -p1

%build
%configure --disable-dependency-tracking
make %{?_smp_mflags}

%install
rm -fr $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
%find_lang %{name}

mkdir -p $RPM_BUILD_ROOT%{_bindir}
ln -s consolehelper $RPM_BUILD_ROOT%{_bindir}/synaptic

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps
cat << EOF > $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps/synaptic
USER=root
PROGRAM=%{_sbindir}/synaptic
SESSION=true
FALLBACK=false
EOF

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pam.d
cat << EOF > $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/synaptic
#%PAM-1.0
auth       sufficient   /%{_lib}/security/pam_rootok.so
auth       sufficient   /%{_lib}/security/pam_timestamp.so
auth       required     /%{_lib}/security/pam_console.so
session    required     /%{_lib}/security/pam_permit.so
session    optional     /%{_lib}/security/pam_xauth.so
session    optional     /%{_lib}/security/pam_timestamp.so
account    required     /%{_lib}/security/pam_permit.so
EOF
if [ -f /%{_lib}/security/pam_stack.so ] && \
   ! grep -q "Deprecated pam_stack module" /%{_lib}/security/pam_stack.so; then
  perl -pi -e's,include(\s*)(.*),required\1pam_stack.so service=\2,' $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/synaptic
fi

# Remove the default menu entries and install our own
rm -f $RPM_BUILD_ROOT%{_datadir}/applications/*
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/X11/sysconfig/synaptic.desktop

desktop-file-install --vendor fedora 		\
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --mode=0644					\
  --remove-key MultipleArgs			\
  --remove-category Application			\
  data/%{name}.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post
scrollkeeper-update -q ||:

%postun
scrollkeeper-update -q ||:

%files -f %{name}.lang
%defattr(-, root, root)
%doc AUTHORS COPYING NEWS README TODO
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}
%{_bindir}/%{name}
%{_sbindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/%{name}
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/gnome/help/%{name}
%{_datadir}/omf/%{name}
%{_mandir}/man8/%{name}.8*

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.57.2-6
- 为 Magic 3.0 重建

* Tue Sep 29 2015 Liu Di <liudidi@gmail.com> - 0.57.2-5
- 为 Magic 3.0 重建

* Sun Jan 06 2013 Liu Di <liudidi@gmail.com> - 0.57.2-4
- 为 Magic 3.0 重建

* Wed Feb 20 2008 Liu Di <liudidi@gmail.com> - 0.57.2-2mgc
- 重新打包


