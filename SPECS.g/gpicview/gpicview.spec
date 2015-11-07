Name:           gpicview
Version:	0.2.4
Release:        2%{?dist}
Summary:        Simple and fast Image Viewer for X
Summary(zh_CN.UTF-8): X 下简单快速的图形查看器

Group:          Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
License:        GPLv2+
URL:            http://lxde.sourceforge.net/gpicview/
Source0:        http://downloads.sourceforge.net/project/lxde/GPicView%20%28image%20Viewer%29/GpicView%20%{version}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libjpeg-devel, gtk2-devel, desktop-file-utils, gettext, intltool
Requires:       xdg-utils

%description
Gpicview is an simple and image viewer with a simple and intuitive interface.
It's extremely lightweight and fast with low memory usage. This makes it 
very suitable as default image viewer of desktop system. Although it is 
developed as the primary image viewer of LXDE, the Lightweight X11 Desktop 
Environment, it only requires GTK+ and can be used in any desktop environment.

%description -l zh_CN.UTF-8
X 下简单快速的图形查看器。虽然主要是为 LXDE 开发的，但可以在任何桌面环境下使用。

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

desktop-file-install --vendor="fedora"   --delete-original      \
  --dir=${RPM_BUILD_ROOT}%{_datadir}/applications               \
  --remove-category=Application                                 \
  --remove-category=Utility                                     \
  --remove-category=Photography                                 \
   $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop
magic_rpm_clean.sh
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT


%post
update-desktop-database &> /dev/null || :


%postun
update-desktop-database &> /dev/null || :



%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING AUTHORS
%{_bindir}/gpicview
%{_datadir}/applications/fedora-gpicview.desktop
%{_datadir}/gpicview/
%{_datadir}/icons/hicolor/*/apps/gpicview.png

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 0.2.4-2
- 为 Magic 3.0 重建

* Fri Apr 11 2014 Liu Di <liudidi@gmail.com> - 0.2.4-1
- 更新到 0.2.4

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 0.2.1-8
- rebuild against new libjpeg

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.2.1-5
- Rebuild for new libpng

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 17 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.1-3
- Add patch to fix DSO linking (#564627)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 29 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.1-1
- Update to 0.2.1

* Sun May 31 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.0-1
- Update to 0.2.0

* Sun May 17 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.99-1
- Update to 0.1.99 (0.2.0 Beta)
- Require xdg-utils
- Fix URL of Source0
- Run update-desktop-database in %%post and %%postun

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 20 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.1.11-1
- New upstream release

* Tue Dec 2 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.1.10-2
- Rebuild of gpicview after updates from Patrice. Thanks and credit
 go to Patrice.

* Sun Sep 14 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.1.10-1
- New upstream release

* Sat Feb 23 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.1.9-1
- New upstream release

* Sat Feb 2 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.1.8-1
- New upstream release

* Fri Jan 11 2008 parag <paragn@fedoraproject.org> - 0.1.7-3
- Spec cleanup

* Thu Jan 10 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.1.7-2
- Removed zero size files
- added lang in spec file

* Thu Jan 10 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.1.7-1
- Initial release
