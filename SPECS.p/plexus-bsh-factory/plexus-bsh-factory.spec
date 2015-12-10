%define parent plexus
%define subname bsh-factory

Name:           %{parent}-%{subname}
Version:        1.0
Release:        0.16.a7%{?dist}
Epoch:          0
Summary:        Plexus Bsh component factory
License:        MIT
URL:            http://plexus.codehaus.org/
BuildArch:      noarch
# svn export svn://svn.plexus.codehaus.org/plexus/tags/plexus-bsh-factory-1.0-alpha-7-SNAPSHOT plexus-bsh-factory/
# tar czf plexus-bsh-factory-src.tar.gz plexus-bsh-factory/
Source0:        %{name}-src.tar.gz
Source3:	plexus-bsh-factory-license.txt

Patch1:         %{name}-encodingfix.patch
Patch2:         0001-Migrate-to-plexus-containers-container-default.patch

BuildRequires:  maven-local
BuildRequires:  mvn(bsh:bsh)
BuildRequires:  mvn(classworlds:classworlds)
BuildRequires:  mvn(org.codehaus.plexus:plexus-container-default)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)

%description
Bsh component class creator for Plexus.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}

%patch1 -b .sav
%patch2 -p1
cp release-pom.xml pom.xml
cp -p %{SOURCE3} .

%build
%mvn_file  : %{parent}/%{subname}
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc plexus-bsh-factory-license.txt

%files javadoc -f .mfiles-javadoc
%doc plexus-bsh-factory-license.txt

%changelog
* Fri Nov 27 2015 Liu Di <liudidi@gmail.com> - 0:1.0-0.16.a7
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.15.a7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.14.a7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.13.a7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 29 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.0-0.12.a7
- Simplify build dependencies
- Update to current packaging guidelines

* Wed Apr 10 2013 Michal Srb <msrb@redhat.com> - 0:1.0-0.11.a7
- Port to plexus-containers-container-default

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0:1.0-0.10.a7
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Jan 23 2013 Michal Srb <msrb@redhat.com> - 0:1.0-0.9.a7
- Build with xmvn

* Thu Nov 22 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.0-0.8.a7
- Cleanup whole spec file (#878828)
- Build/install javadoc package (#878134, #878135)

* Thu Nov 15 2012 Tom Callaway <spot@fedoraproject.org> - 0:1.0-0.7.a7s.1.13
- fix incomplete license.txt

* Tue Aug 21 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.0-0.7.a7s.1.12
- Don't own _mavenfragdir

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.7.a7s.1.11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.6.a7s.1.11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.5.a7s.1.11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 12 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.4.a7s.1.11
- Drop gcj_support.
- Build with ant. Fixes rhbz#539101.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.4.a7s.1.10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 23 2009 Deepak Bhole <dbhole@redhat.com> - 1.0-0.3.a7s.1.10
- Rebuild with maven

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.3.a7s.1.9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Aug 13 2008 Deepak Bhole <dbhole@redhat.com> 1.0-0.2.a7s.1.9
- Build for ppc64

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.0-0.2.a7s.1.8
- add license information from upstream

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.0-0.2.a7s.1.7
- drop repotag
- label license as Unknown (hopefully, upstream will get back to us before the sun explodes)

* Thu Feb 28 2008 Deepak Bhole <dbhole@redhat.com> 1.0-0.2.a7s.1jpp.6
- Rebuild

* Fri Sep 21 2007 Deepak Bhole <dbhole@redhat.com> 1.0-0.1.a7s.2jpp.5
- ExcludeArch ppc64

* Mon Sep 10 2007 Deepak Bhole <dbhole@redhat.com> 1.0-0.1.a7s.2jpp.4
- Build with maven

* Fri Aug 31 2007 Deepak Bhole <dbhole@redhat.com> 1.0-0.1.a7s.2jpp.3
- Build without maven (to build on ppc)

* Tue Mar 20 2007 Deepak Bhole <dbhole@redhat.com> 1.0-0.1.a7s.2jpp.2
- Build with maven

* Fri Feb 23 2007 Tania Bento <tbento@redhat.com> 0:1.0-0.1.a7s.2jpp.1
- Fixed %%Release.
- Fixed %%BuildRoot.
- Fixed %%Vendor.
- Fixed %%Distribution.
- Fixed instructions on how to generate source drop.
- Removed %%post and %%postun sections for javadoc.
- Made sure lines had less than 80 characters.
- Changed to use cp -p to preserve timestamps.

* Tue Oct 17 2006 Deepak Bhole <dbhole@redhat.com> 1.0-0.a7s.2jpp
- Update for maven2 9jpp

* Thu Sep 07 2006 Deepak Bhole <dbhole@redhat.com> 1.0-0.a7s.1jpp
- Initial build
