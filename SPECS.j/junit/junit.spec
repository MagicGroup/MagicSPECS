Name:           junit
Epoch:          1
Version:        4.11
Release:        20%{?dist}
Summary:        Java regression test package
License:        CPL
URL:            http://www.junit.org/
BuildArch:      noarch

# ./clean-tarball.sh %{version}
Source0:        %{name}-%{version}-clean.tar.gz
Source2:        junit-OSGi-MANIFEST.MF
Source3:        create-tarball.sh

# Removing hamcrest source jar references (not available and/or necessary)
Patch0:         %{name}-no-hamcrest-src.patch

BuildRequires:  ant
BuildRequires:  ant-contrib
BuildRequires:  java-devel
BuildRequires:  hamcrest
BuildRequires:  perl(Digest::MD5)

Requires:       hamcrest
Requires:       java-headless

%description
JUnit is a regression testing framework written by Erich Gamma and Kent Beck. 
It is used by the developer who implements unit tests in Java. JUnit is Open
Source Software, released under the Common Public License Version 1.0 and 
hosted on GitHub.

%package manual
Summary:        Manual for %{name}

%description manual
Documentation for %{name}.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%package demo
Summary:        Demos for %{name}
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description demo
Demonstrations and samples for %{name}.

%prep
%setup -q -n %{name}-r%{version}
%patch0 -p1

cp build/maven/junit-pom-template.xml pom.xml
# fix placeholder version in pom
%pom_xpath_set pom:project/pom:version "%{version}"

ln -s $(build-classpath hamcrest/core) lib/hamcrest-core-1.3.jar

# InaccessibleBaseClassTest fails with Java 8
sed -i /InaccessibleBaseClassTest/d src/test/java/org/junit/tests/AllTests.java

%build
ant dist -Dversion-status=

# inject OSGi manifest
mkdir -p META-INF
cp -p %{SOURCE2} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -v %{name}%{version}/%{name}-%{version}.jar META-INF/MANIFEST.MF

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 %{name}%{version}/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -m 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr %{name}%{version}/javadoc/* %{buildroot}%{_javadocdir}/%{name}

# demo
install -d -m 755 %{buildroot}%{_datadir}/%{name}/demo/%{name} 

cp -pr %{name}%{version}/%{name}/* %{buildroot}%{_datadir}/%{name}/demo/%{name}


%files -f .mfiles
%doc LICENSE README CODING_STYLE

%files demo
%doc LICENSE
%{_datadir}/%{name}

%files javadoc
%doc LICENSE
%doc %{_javadocdir}/%{name}

%files manual
%doc LICENSE README CODING_STYLE
%doc junit%{version}/doc/*

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 1:4.11-20
- 为 Magic 3.0 重建

* Tue Aug 12 2014 Liu Di <liudidi@gmail.com> - 1:4.11-19
- 为 Magic 3.0 重建

* Tue Aug 12 2014 Liu Di <liudidi@gmail.com> - 1:4.11-16
- 为 Magic 3.0 重建

* Tue Aug 12 2014 Liu Di <liudidi@gmail.com> - 1:4.11-15
- 为 Magic 3.0 重建

* Mon Jun  9 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:4.11-14
- Add epoch as workaround for a bug in koji-shadow

* Mon Jun  9 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.11-13
- Remove epoch

* Sun Jun  8 2014 Peter Robinson <pbrobinson@fedoraproject.org> 4.11-12
- Re-add Epoch. Once you have it you can't remove it as it breaks upgrade paths

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.11-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Alexander Kurtakov <akurtako@redhat.com> 4.11-10
- Update OSGi manifest to state 4.11.

* Wed May 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.11-9
- Update to current packaging guidelines
- Drop old Obsoletes/Provides for junit4 rename
- Disable test which fails with Java 8

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:4.11-8
- Use Requires: java-headless rebuild (#1067528)

* Fri Aug 23 2013 Michal Srb <msrb@redhat.com> - 0:4.11-7
- Drop "-SNAPSHOT" from version ID
- See: https://lists.fedoraproject.org/pipermail/java-devel/2013-August/004923.html

* Mon Aug 19 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:4.11-6
- Fix version in pom.xml (#998266)

* Fri Aug 02 2013 Michal Srb <msrb@redhat.com> - 0:4.11-5
- Add create-tarball.sh script to SRPM

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:4.11-4
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Fri Jun 21 2013 Michal Srb <msrb@redhat.com> - 0:4.11-3
- Build from clean tarball

* Mon May 06 2013 Tomas Radej <tradej@redhat.com> - 0:4.11-2
- Removed uneeded dependencies

* Thu Mar 21 2013 Tomas Radej <tradej@redhat.com> - 0:4.11-1
- Updated to latest upstream version

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec 18 2012 Michal Srb <msrb@redhat.com> - 0:4.10-7
- Build-time dependency perl-MD5 replaced with perl(Digest::MD5)
- Description cleanup (Resolves: #888389)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 30 2012 Krzysztof Daniel <kdaniel@redhat.com> 0:4.10-5
- Update OSGi metadata to match 4.10.0 release.

* Thu Feb 09 2012 Harald Hoyer <harald@redhat.com> 4.10-4
- removed Conflicts with itsself

* Thu Jan 26 2012 Roland Grunberg <rgrunber@redhat.com> 0:4.8.2-3
- Add OSGi metadata to junit.jar manifest.

* Thu Jan 26 2012 Tomas Radej <tradej@redhat.com> - 0:4.10-2
- Fixed versioning

* Wed Jan 25 2012 Tomas Radej <tradej@redhat.com> - 0:4.10-1
- Updated to upstream 4.10
- Obsoleted junit4
- Epoch added

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 7 2010 Alexander Kurtakov <akurtako@redhat.com> 3.8.2-7
- Drop gcj support.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.2-6.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.2-5.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.8.2-4.4
- drop repotag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.8.2-4jpp.3
- Autorebuild for GCC 4.3

* Thu Sep 20 2007 Deepak Bhole <dbhole@redhat.com> - 3.8.2-3jpp.3
- Fix location of stylesheet for javadocs

* Thu Sep 20 2007 Deepak Bhole <dbhole@redhat.com> - 3.8.2-3jpp.2
- Rebuild for ppc32 execmem issue and new build-id

* Mon Feb 12 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 3.8.2-3jpp.1.fc7
- Add dist tag

* Mon Feb 12 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 3.8.2-3jpp.1
- Committed on behalf of Tania Bento <tbento@redhat.com>
- Update per Fedora review process
- Resolves rhbz#225954

* Thu Aug 10 2006 Deepak Bhole <dbhole@redhat.com> -  0:3.8.2-3jpp.1
- Added missing requirements.

* Thu Aug 10 2006 Karsten Hopp <karsten@redhat.de> 0:3.8.2-2jpp_3fc
- Require(post/postun): coreutils

* Fri Jun 23 2006 Deepak Bhole <dbhole@redhat.com> -  0:3.8.2-2jpp_2fc
- Rebuilt.

* Thu Jun 22 2006 Deepak Bhole <dbhole@redhat.com> -  0:3.8.2-2jpp_1fc
- Upgrade to 3.8.2
- Added conditional native compilation.
- Fix path where demo is located.

* Fri Mar 03 2006 Ralph Apel <r.apel at r-apel.de> - 0:3.8.2-1jpp
- First JPP-1.7 release

* Mon Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:3.8.1-4jpp
- Rebuild with ant-1.6.2
* Fri May 09 2003 David Walluck <david@anti-microsoft.org> 0:3.8.1-3jpp
- update for JPackage 1.5

* Fri Mar 21 2003 Nicolas Mailhot <Nicolas.Mailhot (at) JPackage.org> 3.8.1-2jpp
- For jpackage-utils 1.5

* Fri Sep 06 2002 Henri Gomez <hgomez@users.sourceforge.net> 3.8.1-1jpp
- 3.8.1

* Sun Sep 01 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.8-2jpp 
- used original zip file

* Thu Aug 29 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.8-1jpp 
- 3.8
- group, vendor and distribution tags

* Sat Jan 19 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.7-6jpp
- versioned dir for javadoc
- no dependencies for manual and javadoc packages
- stricter dependency for demo package
- additional sources in individual archives
- section macro

* Sat Dec 1 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.7-5jpp
- javadoc in javadoc package

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 3.7-4jpp
- fixed previous releases ...grrr

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 3.7-3jpp
- added jpp extension
- removed packager tag

* Sun Sep 30 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.7-2jpp
- first unified release
- s/jPackage/JPackage

* Mon Sep 17 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.7-1mdk
- 3.7
- vendor tag
- packager tag
- s/Copyright/License/
- truncated description to 72 columns in spec
- spec cleanup
- used versioned jar
- moved demo files to %%{_datadir}/%%{name}

* Sat Feb 17 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 3.5-1mdk
- first Mandrake release
