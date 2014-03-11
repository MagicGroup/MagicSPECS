Summary: Images for components included in Fedora
Name: comps-extras
Version: 20
Release: 4%{?dist}
URL: http://git.fedorahosted.org/git/?p=comps-extras.git;a=summary
Source0: http://fedorahosted.org/releases/c/o/comps-extras/%{name}-%{version}.tar.gz
# while GPL isn't normal for images, it is the case here
# No version specified.
# KDE logo is LGPL
# LXDE logo is GPLv2+
# Haskell logo is a variation on MIT/X11
# Sugar and Ruby logos are CC-BY-SA
# See COPYING for more details
License: GPL+ and LGPL+ and GPLv2+ and CC-BY-SA and MIT
Group: Applications/System
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

%description
This package contains images for the components included in Fedora.

%prep
%setup -q

%build
# nothing to do

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc comps.dtd comps-cleanup.xsl
%dir %{_datadir}/pixmaps/comps
%{_datadir}/pixmaps/comps/*

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 20-4
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Apr 23 2010 Bill Nottingham <notting@redhat.com> - 20-1
- update haskell icon (#583868)

* Fri Apr 16 2010 Bill Nottingham <notting@redhat.com> - 19-1
- resync against new icon theme

* Wed Feb  3 2010 Bill Nottingham <notting@redhat.com> - 18-1
- updates and tweaks

* Mon Oct 26 2009 Bill Nottingham <notitng@redhat.com> - 17-1
- add LXDE logo (#529792)
- add books, font-design icon symlinks

* Fri Dec  5 2008 Bill Nottingham <notting@redhat.com> - 16-1
- add a copy of the comps dtd & cleanup file (#204704)

* Thu Oct 23 2008 Bill Nottingham <notting@redhat.com> - 15-1
- revert back to non-echo icons
- add icons for Haskell, Ruby
 
* Wed Sep 24 2008 Bill Nottingham <notting@redhat.com> - 14-1
- make more echo-y

* Tue Jul 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 13-2
- fix license tag

* Tue Sep  4 2007 Bill Nottingham <notting@redhat.com> - 13-1
- add fonts icons, tweak sound & video, system tools

* Thu Apr 26 2007 Bill Nottingham <notting@redhat.com> - 12-1
- updates to match current icon theme

* Tue Apr 17 2007 Bill Nottingham <notting@redhat.com> - 11.3-1
- add icons: clustering, virt, window-managers, uncategorized

* Wed Feb  7 2007 Jeremy Katz <katzj@redhat.com> - 11.2-3
- and a few more

* Mon Feb  5 2007 Jeremy Katz <katzj@redhat.com> - 11.2-2
- tweaks from package review

* Tue Aug  1 2006 Bill Nottingham <notting@redhat.com> - 11.2-1
- tweak summary

* Thu Mar  2 2006 Bill Nottingham <notting@redhat.com> - 11.1-1
- new education icon from Diana Fong
- update XFCE icon

* Wed Mar  1 2006 Bill Nottingham <notting@redhat.com> - 11-1
- pirut/anaconda now use 24x24. update sizes
- various additions/removals
- python scripts aren't useful with current repositories, remove them

* Thu May  5 2005 Bill Nottingham <notting@redhat.com> - 10.3-1
- updated icons (<dfong@redhat.com>)

* Mon May  2 2005 Bill Nottingham <notting@redhat.com> - 10.2-1
- add some icons

* Sun Oct 17 2004 Bill Nottingham <notting@redhat.com> - 10.1-1
- fix xfce images (#136046)

* Thu Sep 30 2004 Jeremy Katz <katzj@redhat.com> - 10.0-1
- add xfce images

* Thu Apr 15 2004 Jeremy Katz <katzj@redhat.com> - 9.92-1
- image tweaks

* Sun Nov 23 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- change getnotincomps.py /usr/bin/python2.2 -> /usr/bin/python

* Thu Nov  6 2003 Jeremy Katz <katzj@redhat.com> 9.1-1
- make it so we can handle RedHat vs Fedora (run with basedir as the last
  argument)

* Wed Sep  3 2003 Jeremy Katz <katzj@redhat.com> 9.0.4-1
- copy comps icons for a few new groups

* Tue May 27 2003 Jeremy Katz <katzj@redhat.com> 9.0.3-1
- getfullcomps.py can go away now that anaconda does dep resolution in 
  realtime

* Fri Apr 11 2003 Jeremy Katz <katzj@redhat.com> 9.0.2-1
- update getfullcomps.py to not prefer devel packages

* Tue Apr  8 2003 Tim Powers <timp@redhat.com> 9.0.1-2
- made getfullcomps.py importable

* Tue Mar  4 2003 Jeremy Katz <katzj@redhat.com> 9.0.1-1
- add /usr/share/comps-extras/whichcd.py to find out which cd a given 
  package is on (#85343)

* Tue Dec 17 2002 Jeremy Katz <katzj@redhat.com>
- improve getfullcomps.py handling of multiple provides

* Wed Sep 04 2002 Jeremy Katz <katzj@redhat.com>
- update images again

* Wed Sep 04 2002 Michael Fulbright <msf@redhat.com>
- update images

* Thu Aug 29 2002 Jeremy Katz <katzj@redhat.com>
- update images

* Tue Jul 23 2002 Jeremy Katz <katzj@redhat.com>
- Initial build.


