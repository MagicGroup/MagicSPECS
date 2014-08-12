# Note to packagers: When rebasing this to a later version, do not
# forget to ensure that sources 1 and 2 are up to date as well as
# the Requires list.

Name:           groovy
Version:        1.8.9
Release:        12%{?dist}
Summary:        Dynamic language for the Java Platform

# Some of the files are licensed under BSD and CPL terms, but the CPL has been superceded
# by the EPL. We include copies of both for completeness.
# groovyConsole uses CC-BY licensed icons
# (see: subprojects/groovy-console/target/tmp/groovydoc/groovy/ui/icons/credits.txt)
License:        ASL 2.0 and BSD and EPL and Public Domain and CC-BY
URL:            http://groovy.codehaus.org/

Source0:        http://dist.groovy.codehaus.org/distributions/%{name}-src-%{version}.zip
Source1:        groovy-script
Source2:        groovy-starter.conf
Source3:        groovy.desktop
Source4:        cpl-v10.txt
Source5:        epl-v10.txt
Source6:        http://www.apache.org/licenses/LICENSE-2.0.txt
# http://jira.codehaus.org/browse/GROOVY-6085
Patch0:         groovy-inner-interface-annotations.patch
Patch1:         groovy-build-with-java8.patch

BuildRequires:  ant
BuildRequires:  antlr-tool
BuildRequires:  ant-antlr
BuildRequires:  objectweb-asm3
BuildRequires:  bsf
BuildRequires:  apache-ivy
BuildRequires:  jansi
BuildRequires:  jline1
BuildRequires:  tomcat-jsp-2.2-api
BuildRequires:  junit
BuildRequires:  tomcat-servlet-3.0-api
BuildRequires:  xstream
BuildRequires:  java-devel >= 1.8
BuildRequires:  desktop-file-utils
BuildRequires:  jpackage-utils
BuildRequires:  apache-commons-cli
BuildRequires:  unzip
BuildRequires:  javapackages-local
BuildRequires:  mvn(org.apache.ant:ant-junit)
BuildRequires:  mvn(org.apache.ant:ant-launcher)
BuildRequires:  mvn(javax.servlet:servlet-api)
BuildRequires:  mvn(javax.servlet:jsp-api)

BuildArch:      noarch

%description
Groovy is an agile and dynamic language for the Java Virtual Machine,
built upon Java with features inspired by languages like Python, Ruby and
Smalltalk.  It seamlessly integrates with all existing Java objects and
libraries and compiles straight to Java bytecode so you can use it anywhere
you can use Java.


%package javadoc
Summary:        API Documentation for %{name}
%description javadoc
JavaDoc documentation for %{name}


%prep
%setup -q
cp %{SOURCE4} %{SOURCE5} %{SOURCE6} .
# Remove bundled JARs and classes
find \( -name *.jar -o -name *.class \) -delete

%patch0 -p1
%patch1 -p1

%pom_remove_dep org.codehaus.gpars:gpars
%pom_change_dep jline:jline jline:jline:1
%mvn_file : %{name}

%build
mkdir -p target/lib/{compile,tools}

# Construct classpath
build-jar-repository target/lib/compile servlet jsp \
        objectweb-asm3/asm-tree objectweb-asm3/asm \
        objectweb-asm3/asm-util objectweb-asm3/asm-analysis \
        antlr ant/ant-antlr antlr \
        bsf jline1 xstream ant junit ivy commons-cli \
        jansi

# Build
# TODO: Build at least tests, maybe examples
ant -DskipTests=on -DskipExamples=on -DskipFetch=on -DskipEmbeddable=on \
        createJars javadoc

%install
%mvn_artifact pom.xml target/dist/groovy.jar
%mvn_install -J target/html/api/

# Startup scripts
install -d $RPM_BUILD_ROOT%{_bindir}
install -p -m755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/groovy
for TOOL in grape groovyc groovyConsole java2groovy groovysh
do
        ln $RPM_BUILD_ROOT%{_bindir}/groovy \
                $RPM_BUILD_ROOT%{_bindir}/$TOOL
done

# Configuration
install -d $RPM_BUILD_ROOT%{_sysconfdir}
install -p -m644 %{SOURCE2} \
        $RPM_BUILD_ROOT%{_sysconfdir}/groovy-starter.conf

# Desktop icon
install -d $RPM_BUILD_ROOT%{_datadir}/pixmaps
install -d $RPM_BUILD_ROOT%{_datadir}/applications
install -p -m644 src/main/groovy/ui/ConsoleIcon.png \
        $RPM_BUILD_ROOT%{_datadir}/pixmaps/groovy.png
desktop-file-install --dir $RPM_BUILD_ROOT%{_datadir}/applications \
        %{SOURCE3}

%files -f .mfiles
%defattr(-,root,root,-)
%{_bindir}/*
%{_datadir}/pixmaps/*
%{_datadir}/applications/*
%config(noreplace) %{_sysconfdir}/*
%doc README.md
%doc LICENSE.txt LICENSE-2.0.txt NOTICE.txt cpl-v10.txt epl-v10.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt LICENSE-2.0.txt NOTICE.txt cpl-v10.txt epl-v10.txt

%changelog
* Sun Jun 22 2014 Michal Srb - 1.8.9-12
- Migrate to %%mvn_artifact
- Fix dep on jline1 in run script

* Mon Jun 16 2014 Michal Srb <msrb@redhat.com> - 1.8.9-11
- Fix FTBFS

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.8.9-9
- Use .mfiles generated during build

* Mon Jan 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.8.9-8
- Add Requires on java-devel
- Resolves: rhbz#736753

* Fri Dec 06 2013 Michal Srb <msrb@redhat.com> - 1.8.9-7
- Groovy needs asm3

* Thu Oct 24 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.8.9-6
- Migrate from jline to jline1
- Resolves: rhbz#1022969

* Sat Aug 18 2013 Matt Spaulding <mspaulding06@gmail.com> - 1.8.9-5
- Fix setting classpath (RHBZ#982378)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 10 2013 Michal Srb <msrb@redhat.com> - 1.8.9-3
- Fix license tag (+CC-BY)

* Thu Jun  6 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.8.9-2
- Remove bundled JARs and classes
- Add workaround for rhbz#971483
- Add Public Domain to licenses
- Install ASL 2.0 license text, resolves: rhbz#858257

* Sat Apr 20 2013 gil cattaneo <puntogil@libero.it> - 1.8.9-1
- Update to 1.8.9

* Thu Apr 11 2013 Matt Spaulding <mspaulding06@gmail.com> - 1.8.8-4
- Now accepts classpath argument (RHBZ #810885)

* Mon Apr  8 2013 Andy Grimm <agrimm@gmail.com> - 1.8.8-3
- Apply patch for GROOVY-6085 (RHBZ #949352) 

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Tom Callaway <spot@fedoraproject.org> - 1.8.8-1
- Update to 1.8.8
- Fix licensing issues

* Wed Jul 25 2012 Johannes Lips <hannes@fedoraproject.org> - 1.8.7-1
- Update to 1.8.7

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 21 2012 Alexander Kurtakov <akurtako@redhat.com> 1.8.6-4
- Move to tomcat v7 apis.
- Guideline fixes.

* Fri Mar 09 2012 Johannes Lips <hannes@fedoraproject.org> - 1.8.6-3
- fixed the path of jvm in the startup script 

* Sat Mar 03 2012 Johannes Lips <hannes@fedoraproject.org> - 1.8.6-2
- fixed the startup script by adding jansi as dep

* Wed Feb 22 2012 Johannes Lips <hannes@fedoraproject.org> - 1.8.6-1
- Update to 1.8.6

* Tue Jan 03 2012 Johannes Lips <hannes@fedoraproject.org> - 1.8.5-1
- Update to 1.8.5

* Sun Nov 20 2011 Johannes Lips <hannes@fedoraproject.org> - 1.8.4-1
- Update to 1.8.4

* Thu Oct 13 2011 Johannes Lips <hannes@fedoraproject.org> - 1.8.3-2
- remove the nojansi patch since jansi is in fedora

* Thu Oct 13 2011 Johannes Lips <hannes@fedoraproject.org> - 1.8.3-1
- Update to 1.8.3

* Tue Sep 06 2011 Johannes Lips <hannes@fedoraproject.org> - 1.8.2-1
- Update to 1.8.2

* Sat Aug 13 2011 Johannes Lips <hannes@fedoraproject.org> - 1.8.1-3
- adjusted the maven pom dir

* Sat Aug 13 2011 Johannes Lips <hannes@fedoraproject.org> - 1.8.1-2
- updated the nojansi patch

* Sat Aug 13 2011 Johannes Lips <hannes@fedoraproject.org> - 1.8.1-1
- Update to 1.8.1

* Wed May 04 2011 Johannes Lips <hannes@fedoraproject.org> - 1.8.0-2
- Minor changes to reflect changes to packaging guidelines

* Fri Apr 29 2011 Johannes Lips <hannes@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Nov 6 2010 Alexander Kurtakov <akurtako@redhat.com> 1.7.2-3
- Build with servlet and jsp apis from tomcat6.

* Thu Jun 17 2010 Lubomir Rintel <lkundrak@v3.sk> - 1.7.2-2
- Fix a typo

* Tue Apr 20 2010 Lubomir Rintel <lkundrak@v3.sk> - 1.7.2-1
- Bump version

* Fri Apr 02 2010 Lubomir Rintel <lkundrak@v3.sk> - 1.7.1-1
- Bump version
- Revert addition of jansi dependency

* Fri Apr 02 2010 Lubomir Rintel <lkundrak@v3.sk> - 1.7.0-2
- Add maven depmap

* Wed Feb 17 2010 Lubomir Rintel <lkundrak@v3.sk> - 1.7.0-1
- New upstream version
- Use asm 3.1 instead of asm2

* Wed Dec 04 2009 Lubomir Rintel <lkundrak@v3.sk> - 1.6.7-1
- New upstream version
- Make Jochen happy

* Thu Dec 03 2009 Lubomir Rintel <lkundrak@v3.sk> - 1.6.6-2
- Build with OpenJDK

* Mon Nov 30 2009 Lubomir Rintel <lkundrak@v3.sk> - 1.6.6-1
- Bump to 1.6.6
- Don't mistakenly require itself (Jochen Schmitt, #534168#c3)

* Fri Nov 27 2009 Lubomir Rintel <lkundrak@v3.sk> - 1.6.5-2
- Hopefully fix mockbuild

* Mon Nov 09 2009 Lubomir Rintel <lkundrak@v3.sk> - 1.6.5-1
- Initial Fedora packaging
