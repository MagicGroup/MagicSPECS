Name:		obconf
Version:	2.0.4
Release:	4%{?dist}
Summary:	A graphical configuration editor for the Openbox window manager

Group:		User Interface/X
License:	GPLv2+
URL:		http://icculus.org/openbox/index.php/ObConf:About
Source0:	http://icculus.org/openbox/obconf/%{name}-%{version}.tar.gz

BuildRequires:	openbox-devel >= 3.5.2
BuildRequires:	libglade2-devel
BuildRequires:	startup-notification-devel
BuildRequires:	pkgconfig
BuildRequires:	desktop-file-utils
BuildRequires:	libSM-devel
BuildRequires:	gettext-devel
BuildRequires:	libtool

%description
ObConf is a graphical configuration editor for the Openbox window manager. 


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
%find_lang %{name}
desktop-file-install \
	--dir %{buildroot}%{_datadir}/applications	\
	--add-category	X-Fedora	\
	--delete-original	\
	%{buildroot}%{_datadir}/applications/%{name}.desktop


%post
update-desktop-database %{_datadir}/applications &> /dev/null || :
touch --no-create %{_datadir}/mime/packages &> /dev/null || :

%postun
update-desktop-database %{_datadir}/applications &> /dev/null || :
if [ $1 -eq 0 ]; then
touch --no-create %{_datadir}/mime/packages &> /dev/null || :
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
fi

%posttrans
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :


%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_bindir}/%{name}
%{_datadir}/%{name}/  
%{_datadir}/applications/*%{name}.desktop
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/mimelnk/
%{_datadir}/pixmaps/%{name}.png


%changelog
* Thu Oct 02 2014 Rex Dieter <rdieter@fedoraproject.org> 2.0.4-4
- update mime scriptlets

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug 15 2013 Miroslav Lichvar <mlichvar@redhat.com> - 2.0.4-1
- update to 2.0.4

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-14.20121006gitcfde28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 28 2013 Miroslav Lichvar <mlichvar@redhat.com> - 2.0.3-13.20121006gitcfde28
- update to 20121006gitcfde28
- buildrequire libtool
- remove obsolete macros

* Mon Apr 29 2013 Jon Ciesla <limburgher@gmail.com> - 2.0.3-12.20100212gitb04658
- Drop desktop vendor tag.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-11.20100212gitb04658
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-10.20100212gitb04658
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-9.20100212gitb04658
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 30 2011 Miroslav Lichvar <mlichvar@redhat.com> - 2.0.3-8.20100212gitb04658
- fix config file loading (#739973)

* Fri Aug 05 2011 Miroslav Lichvar <mlichvar@redhat.com> - 2.0.3-7.20100212gitb04658
- update to 20100212gitb04658 for openbox-3.5

* Mon May 02 2011 Miroslav Lichvar <mlichvar@redhat.com> - 2.0.3-6.20091221gitc8ac23
- update to 20091221gitc8ac23 (#700937)
- include Hungarian and Romanian translations (#665584)
- don't set the theme preview if a null is returned (#692549)
- don't use a non-zero page size for some spinners (#694044)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Apr 17 2008 Miroslav Lichvar <mlichvar@redhat.com> - 2.0.3-2
- Rebuild for new openbox

* Sun Feb 03 2008 Miroslav Lichvar <mlichvar@redhat.com> - 2.0.3-1
- Update to 2.0.3

* Wed Aug 22 2007 Miroslav Lichvar <mlichvar@redhat.com> - 2.0.2-2
- Update license tag

* Mon Jul 23 2007 Miroslav Lichvar <mlichvar@redhat.com> - 2.0.2-1
- Update to 2.0.2

* Thu Jun 14 2007 Miroslav Lichvar <mlichvar@redhat.com> - 2.0.1-1
- Update to 2.0.1

* Sun Aug 27 2006 Peter Gordon <peter@thecodergeek.com> - 1.6-3
- Mass FC6 rebuild

* Thu Jul 13 2006 Peter Gordon <peter@thecodergeek.com> - 1.6-2
- Add BR: libSM-devel to fix build issue.

* Fri Jun 09 2006 Peter Gordon <peter@thecodergeek.com> - 1.6-1
- Initial packaging. 
