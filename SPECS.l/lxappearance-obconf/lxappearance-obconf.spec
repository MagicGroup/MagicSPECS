# Review at https://bugzilla.redhat.com/show_bug.cgi?id=630184

%global git_snapshot 0
%global git_rev 5fad820707cdf6a565f909e483820b7a49bd4a36
%global git_date 20120304

%if 0%{?git_snapshot}
%global git_short %(echo %{git_rev} | cut -c-8)
%global git_version %{git_date}git%{git_short}
%endif

# Source0 was generated as follows:
# git clone git://lxde.git.sourceforge.net/gitroot/lxde/lxappearance-obconf
# cd lxappearance-obconf
# git archive --format=tar --prefix=lxappearance-obconf/ %{git_short} | bzip2 > lxappearance-obconf-%{?git_version}.tar.bz2

Name:           lxappearance-obconf
Version:        0.2.0
Release:        4%{?git_version:.%{?git_version}}%{?dist}
Summary:        Plugin to configure Openbox inside LXAppearance
Summary(zh_CN.UTF-8): 在 LXAppearance 配置 Openbox 的插件

Group:          User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
License:        GPLv2+
URL:            http://lxde.org/
#VCS: git:git://lxde.git.sourceforge.net/gitroot/lxde/lxappearance-obconf
%if 0%{?git_snapshot}
Source0:        %{name}-%{?git_version}.tar.bz2
%else
Source0:        http://downloads.sourceforge.net/sourceforge/lxde/%{name}-%{version}.tar.gz
%endif
#与 openbox 5.3.2 兼容
Patch1:		obconf-rrbutton.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel
BuildRequires:  openbox-devel >= 3.5.0
BuildRequires:  lxappearance-devel
BuildRequires:  libSM-devel
BuildRequires:  gettext
BuildRequires:  intltool
%{?git_snapshot:BuildRequires: libtool}
Requires:       lxappearance >= 0.5.0
Requires:       openbox >= 3.5.0

%description
This plugin adds an additional tab called "Window Border" to LXAppearance.
It is only visible when the plugin is installed and Openbox is in use.

%description -l zh_CN.UTF-8
在 LXAppearance 配置 Openbox 的插件。

%prep
%setup -q %{?git_version:-n %{name}}
%patch1 -p1

%build
%{?git_version:sh autogen.sh}
%configure --disable-static
make %{?_smp_mflags} V=1


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
# FIXME add NEWS and TODO if not empty
%doc AUTHORS CHANGELOG COPYING README
%{_libdir}/lxappearance/plugins/obconf.so
%{_datadir}/lxappearance/obconf/


%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.2.0-4
- 为 Magic 3.0 重建

* Tue Mar 03 2015 Liu Di <liudidi@gmail.com> - 0.2.0-3
- 为 Magic 3.0 重建

* Fri Jul 04 2014 Liu Di <liudidi@gmail.com> - 0.2.0-2
- 为 Magic 3.0 重建

* Sat Aug 04 2012 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.0-1
- Update to 0.2.0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Mar 04 2012 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.2-0.3.20120304git5fad8207
- Update to latest git to fix broken preview with Openbox 3.5

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-0.2.20110828git02aeaab2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Aug 28 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.2-0.1.20110828git02aeaab2
- Update to latest GIT snapshot to the package build with openbox >= 3.5.0

* Sun Aug 28 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.1-1
- Update to 0.1.1 (Note that upstream's 0.0.1 tarball is actually 0.1.1 in VCS)

* Wed Jul 14 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.0-0.1.20110714git3a0fd02d
- Update to latest GIT snapshot

* Fri Jan 28 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.0-0.1.20110128git710ba0e6
- Update to latest GIT snapshot

* Fri Sep 03 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.0-0.1.20100903git1769cdca
- Update to latest GIT snapshot

* Fri Aug 13 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.0-0.1.20100813git1bf017ee
- initial package
