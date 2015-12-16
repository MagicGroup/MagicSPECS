%define pkg_version     11b
%define with_bootstrap  0

Name:           java_cup
Version:        0.11b
Release:        1%{?dist}
Epoch:          1
Summary:        LALR parser generator for Java
License:        MIT
URL:            http://www2.cs.tum.edu/projects/cup/
BuildArch:      noarch

# svn export -r 65 https://www2.in.tum.de/repos/cup/develop/ java_cup-0.11b
# tar cjf java_cup-0.11b.tar.bz2 java_cup-0.11b/
Source0:        java_cup-%{version}.tar.bz2
Source1:        java_cup-pom.xml
# Add OSGi manifests
Source2:        %{name}-MANIFEST.MF
Source4:        %{name}-runtime-MANIFEST.MF

Patch0:         %{name}-build.patch

BuildRequires:  ant
BuildRequires:  java-devel
BuildRequires:  jpackage-utils >= 0:1.5
BuildRequires:  jflex
%if ! %{with_bootstrap}
BuildRequires:  java_cup >= 1:0.11a
%endif
BuildRequires:  zip

Requires:       java-headless


%description
java_cup is a LALR Parser Generator for Java

%package javadoc
Summary:       Javadoc for java_cup

%description javadoc
Javadoc for java_cup

%package manual
Summary:        Documentation for java_cup

%description manual
Documentation for java_cup.

%prep
%setup -q 
%patch0 -b .build
cp %{SOURCE1} pom.xml

# remove all binary files
find -name "*.class" -delete

%if ! %{with_bootstrap}
# remove prebuilt JFlex
rm -rf java_cup-%{version}/bin/JFlex.jar

# remove prebuilt java_cup, if not bootstrapping
rm -rf java_cup-%{version}/bin/java-cup-11.jar
%endif

%build
%if ! %{with_bootstrap}
export CLASSPATH=$(build-classpath java_cup java_cup-runtime jflex)
%endif

ant -Dcupversion=20150326 -Dsvnversion=65
find -name parser.cup -delete
ant javadoc

%install
# inject OSGi manifests
mkdir -p META-INF
cp -p %{SOURCE2} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u dist/java-cup-%{pkg_version}.jar META-INF/MANIFEST.MF
cp -p %{SOURCE4} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u dist/java-cup-%{pkg_version}-runtime.jar META-INF/MANIFEST.MF

# jar
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 dist/java-cup-%{pkg_version}.jar %{buildroot}%{_javadir}/%{name}.jar
install -m 644 dist/java-cup-%{pkg_version}-runtime.jar %{buildroot}%{_javadir}/%{name}-runtime.jar

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr dist/javadoc/* %{buildroot}%{_javadocdir}/%{name}

%files -f .mfiles
%doc changelog.txt
%{_javadir}/*
%license licence.txt

%files manual
%doc manual.html
%license licence.txt

%files javadoc
%license licence.txt
%{_javadocdir}/%{name}

%changelog
* Tue Jun 23 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.11b-1
- Update to upstream version 0.11b

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.11a-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Feb 06 2015 gil cattaneo <puntogil@libero.it> 1:0.11a-19
- introduce license macro

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.11a-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.11a-17
- Use .mfiles generated during build

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1:0.11a-16
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 31 2013 Mat Booth <fedora@matbooth.co.uk> - 1:0.11a-15
- Inject OSGi manifests into both jars.

* Fri Aug 30 2013 Mat Booth <fedora@matbooth.co.uk> - 1:0.11a-14
- Patch so that generated action methods do not exceed the 65535 byte JVM
  method size limit. Supplied by eclipse-pdt project.
- Drop rpm bug workaround scriptlet.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.11a-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.11a-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 gil cattaneo <puntogil@libero.it> 1:0.11a-11
- adapt to current guideline
- add %%pre javadoc script

* Tue Nov 13 2012 Tom Callaway <spot@fedoraproject.org> - 1:0.11a-10
- include copy of LICENSE, correct License tag

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.11a-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 24 2012 Gerard Ryan <galileo@fedoraproject.org> - 1:0.11a-8
- Inject OSGI Manifest for java-cup-runtime.jar

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.11a-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.11a-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Dec 04 2010 Lubomir Rintel <lkundrak@v3.sk> 1:0.11a-5
- Require appropriate packages for depmap maintenance in scriptlets
- Remove classpath from jar manifest

* Mon Feb 15 2010 Alexander Kurtakov <akurtako@redhat.com> 1:0.11a-4
- Add maven pom and depmap.

* Wed Jan 20 2010 Alexander Kurtakov <akurtako@redhat.com> 1:0.11a-3
- Fix bootstrap.

* Sun Jan 17 2010 Miloš Jakubíček <xjakub@fi.muni.cz> - 1:0.11a-2
- Rebuilt in non-bootstrap mode (removed all prebuilt jars).
- Added BR: jflex and java_cup >= 1:0.11a for non-bootstrap mode
- Remove unnecessary R(post,postun): coreutils

* Fri Jan 8 2010 Alexander Kurtakov <akurtako@redhat.com> 1:0.11a-1
- Update to 0.11a.
- Drop gcj_support.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.10k-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.10k-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 15 2008 Lubomir Rintel <lkundrak@v3.sk> - 1:0.10k-1
- Fix the version to match upstream, so that FEver can be used

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:0.10-0.k.6.3
- drop repotag

* Sun Feb 17 2008 Lubomir Kundrak <lkundrak@redhat.com> - 1:0.10-0.k.6jpp.2
- Ant task
- Clean up to satisfy QA script and rpmlint

* Fri Aug 04 2006 Vivek Lakshmanan <vivekl@redhat.com> - 1:0.10-0.k.6jpp.1
- Re-sync with latest version from JPP.
- Partially adopt new naming convention.

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 1:0.10-0.k.5jpp_2fc
- Rebuilt

* Thu Jul 20 2006 Vivek Lakshmanan <vivekl@redhat.com> - 1:0.10-0.k.5jpp_1fc
- Re-sync with latest version from JPP.

* Wed Jul 19 2006 Vivek Lakshmanan <vivekl@redhat.com> - 1:0.10-0.k.4jpp_1fc
- Conditional native compilation for GCJ.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:0.10-0.k.1jpp_10fc
- rebuild

* Mon Mar  6 2006 Jeremy Katz <katzj@redhat.com> - 1:0.10-0.k.1jpp_9fc
- stop scriptlet spew

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:0.10-0.k.1jpp_8fc
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:0.10-0.k.1jpp_7fc
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan  3 2006 Jesse Keating <jkeating@redhat.com> 1:0.10-0.k.1jpp_6fc
- rebuilt again

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Jul 19 2005 Gary Benson <gbenson@redhat.com> 1:0.10-0.k.1jpp_5fc
- Build on ia64, ppc64, s390 and s390x.
- Switch to aot-compile-rpm.

* Tue Jun 28 2005 Gary Benson <gbenson@redhat.com> 1:0.10-0.k.1jpp_4fc
- BC-compile.

* Tue Jun 21 2005 Gary Benson <gbenson@redhat.com> 1:0.10-0.k.1jpp_3fc
- Remove classes from the tarball.

* Thu Nov  4 2004 Gary Benson <gbenson@redhat.com> 1:0.10-0.k.1jpp_2fc
- Build into Fedora.

* Thu Mar  4 2004 Frank Ch. Eigler <fche@redhat.com> 1:0.10-0.k.1jpp_1rh
- RH vacuuming

* Thu Jan 22 2004 David Walluck <david@anti-microsoft.org> 1:0.10-0.k.1jpp
- fix version/release (bump epoch)
- change License tag from Free to BSD-style
- add Distribution tag
- really update for JPackage 1.5

* Wed Mar 26 2003 Paul Nasrat <pauln@truemesh.com> 0.10k-1jpp
- for jpackage-utils 1.5
- New spec reverse engineered from binary rpms
