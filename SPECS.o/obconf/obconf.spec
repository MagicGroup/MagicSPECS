Name:		obconf
Version:	2.0.3
Release:	10.20100212gitb04658%{?dist}
Summary:	A graphical configuration editor for the Openbox window manager

Group:		User Interface/X
License:	GPLv2+
URL:		http://icculus.org/openbox/index.php/ObConf:About
#Source0:	http://icculus.org/openbox/obconf/%{name}-%{version}.tar.gz
Source0:	obconf-20100212gitb04658.tar.gz
Patch0:		obconf-trans.patch
Patch1:		obconf-loadconf.patch
Patch2:		obconf-spinner.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	openbox-devel >= 3.4
BuildRequires:	libglade2-devel
BuildRequires:	startup-notification-devel
BuildRequires:	pkgconfig
BuildRequires:	desktop-file-utils
BuildRequires:	libSM-devel
BuildRequires:	gettext-devel

%description
ObConf is a graphical configuration editor for the Openbox window manager. 


%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1 -b .loadconf
%patch2 -p1 -b .spinner


%build
./bootstrap
%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
%find_lang %{name}
desktop-file-install --vendor fedora	\
	--dir %{buildroot}%{_datadir}/applications	\
	--add-category	X-Fedora	\
	--delete-original	\
	%{buildroot}%{_datadir}/applications/%{name}.desktop


%clean
rm -rf %{buildroot}


%post
update-mime-database %{_datadir}/mime &> /dev/null
update-desktop-database %{_datadir}/applications &> /dev/null
:


%postun
update-mime-database %{_datadir}/mime &> /dev/null
update-desktop-database %{_datadir}/applications &> /dev/null
:


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_bindir}/%{name}
%{_datadir}/%{name}/  
%{_datadir}/applications/fedora-%{name}.desktop
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/mimelnk/
%{_datadir}/pixmaps/%{name}.png


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 2.0.3-10.20100212gitb04658
- 为 Magic 3.0 重建

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
