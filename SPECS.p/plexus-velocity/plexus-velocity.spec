%define parent plexus
%define subname velocity

Name:           plexus-velocity
Version:        1.1.8
Release:        18%{?dist}
Summary:        Plexus Velocity Component
License:        ASL 2.0
URL:            http://plexus.codehaus.org/
BuildArch:      noarch

# svn export http://svn.codehaus.org/plexus/plexus-components/tags/plexus-velocity-1.1.8/
# tar czf plexus-velocity-1.1.8-src.tar.gz plexus-velocity-1.1.8/
Source0:        plexus-velocity-%{version}-src.tar.gz
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt

BuildRequires:  maven-local
BuildRequires:  mvn(commons-collections:commons-collections)
BuildRequires:  mvn(org.codehaus.plexus:plexus-components:pom:)
BuildRequires:  mvn(org.codehaus.plexus:plexus-container-default)
BuildRequires:  mvn(velocity:velocity)

%description
The Plexus project seeks to create end-to-end developer tools for
writing applications. At the core is the container, which can be
embedded or for a full scale application server. There are many
reusable components for hibernate, form processing, jndi, i18n,
velocity, etc. Plexus also includes an application server which
is like a J2EE application server, without all the baggage.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n plexus-velocity-%{version}
cp -p %{SOURCE1} LICENSE
for j in $(find . -name "*.jar"); do
        mv $j $j.no
done

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE

%files javadoc -f .mfiles-javadoc
%doc LICENSE

%changelog
* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 1.1.8-18
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.8-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1.8-16
- Update to current packaging guidelines

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.8-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.8-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0:1.1.8-13
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Nov 22 2012 Jaromir Capik <jcapik@redhat.com> - 0:1.1.8-12
- Migration to plexus-containers-container-default

* Wed Nov 21 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.1.8-11
- Install LICENSE file
- Resolves: rhbz#878833

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Sep 7 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.1.8-8
- Drop ant build.
- Further cleanups.

* Thu Jul 28 2011 Jaromir Capik <jcapik@redhat.com> - 0:1.1.8-7
- Migration to maven3
- Removal of plexus-maven-plugin (not needed)
- Minor spec file changes according to the latest guidelines

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 22 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.1.8-5
- BR java-devel 1.6.

* Tue Dec 22 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.1.8-4
- BR maven-surefire-provider-junit.

* Tue Dec 22 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.1.8-3
- BR maven-doxia-sitetools.

* Tue Dec 22 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.1.8-2
- BR plexus-maven-plugin.

* Tue Dec 22 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.1.8-1
- Update to upstream 1.1.8.

* Fri Aug 21 2009 Andrew Overholt <overholt@redhat.com> 1.1.7-3.3
- Add ant-nodeps BR

* Fri Aug 21 2009 Andrew Overholt <overholt@redhat.com> 1.1.7-3.2
- Add ant-contrib BR

* Fri Aug 21 2009 Andrew Overholt <overholt@redhat.com> 0:1.1.7-3.1
- Import from Deepak Bhole's work (import from JPackage, update to 1.1.7)
- Remove gcj support

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.2-5.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.2-4.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.1.2-3.2
- drop repotag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.1.2-3jpp.1
- Autorebuild for GCC 4.3

* Sat Mar 24 2007 Ralph Apel <r.apel at r-apel.de> - 0:1.1.2-3jpp
- Build with maven2 by default
- Add gcj_support options

* Fri Feb 16 2007 Tania Bento <tbento@redhat.com> - 0:1.1.2-2jpp.1
- Fixed %%License.
- Fixed %%BuildRoot.
- Fixed %%Release.
- Removed the %%post and %%postun for javadoc.
- Removed %%Vendor.
- Removed %%Distribution.
- Removed "%%define section free".
- Added the gcj support option.
- Added BR for jakarta-commons-logging.

* Wed May 17 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.1.2-2jpp
- First JPP-1.7 release

* Mon Nov 07 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.1.2-1jpp
- First JPackage build
