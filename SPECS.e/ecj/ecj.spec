Epoch: 1

%global qualifier R-4.4.1-201409250400

Summary: Eclipse Compiler for Java
Name: ecj
Version: 4.4.1
Release: 2%{?dist}
URL: http://www.eclipse.org
License: EPL
Group: Development/Languages
Source0: http://download.eclipse.org/eclipse/downloads/drops4/%{qualifier}/%{name}src-%{version}.jar
Source1: ecj.sh.in
#Patched from http://central.maven.org/maven2/org/eclipse/jdt/core/compiler/ecj/4.4/ecj-4.4.pom 
# No dependencies are needed for ecj, dependencies are for using of jdt.core which makes no sense outside of eclipse
Source3: ecj-4.4.1.pom
Source4: ecj.1
Source5: http://git.eclipse.org/c/jdt/eclipse.jdt.core.git/plain/org.eclipse.jdt.core/scripts/binary/META-INF/MANIFEST.MF
# Always generate debug info when building RPMs (Andrew Haley)
Patch0: %{name}-rpmdebuginfo.patch
# build.xml fails to include a necessary .props file in the built ecj.jar
Patch1: %{name}-include-props.patch

BuildArch: noarch

BuildRequires: gzip
BuildRequires: ant
BuildRequires: java-devel >= 1:1.7.0 

Provides: eclipse-ecj = %{epoch}:%{version}-%{release}
Obsoletes: eclipse-ecj < 1:3.4.2-4

Obsoletes: %{name}-native < 1:4.2.1-10

%description
ECJ is the Java bytecode compiler of the Eclipse Platform.  It is also known as
the JDT Core batch compiler.

%prep
%setup -q -c
%patch0 -p1
%patch1 -b .sav

sed -i -e 's|debuglevel=\"lines,source\"|debug=\"yes\"|g' build.xml
sed -i -e "s/Xlint:none/Xlint:none -encoding cp1252/g" build.xml

cp %{SOURCE3} pom.xml
mkdir -p scripts/binary/META-INF/
cp %{SOURCE5} scripts/binary/META-INF/MANIFEST.MF

# JDTCompilerAdapter isn't used by the batch compiler
rm -f org/eclipse/jdt/core/JDTCompilerAdapter.java
cp %{SOURCE4} ecj.1

%build
ant 
gzip ecj.1

%install
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -a *.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
pushd $RPM_BUILD_ROOT%{_javadir}
ln -s %{name}.jar eclipse-%{name}.jar
ln -s %{name}.jar jdtcore.jar
popd

# Install the ecj wrapper script
install -p -D -m0755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/ecj
sed --in-place "s:@JAVADIR@:%{_javadir}:" $RPM_BUILD_ROOT%{_bindir}/ecj

# Install manpage
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -m 644 -p ecj.1.gz $RPM_BUILD_ROOT%{_mandir}/man1/ecj.1.gz

# poms
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom

%add_maven_depmap -a "org.eclipse.tycho:org.eclipse.jdt.core,org.eclipse.jdt:core,org.eclipse.jdt:org.eclipse.jdt.core" JPP-%{name}.pom %{name}.jar

%files -f .mfiles
%doc about.html
%{_bindir}/%{name}
%{_javadir}/eclipse-%{name}.jar
%{_javadir}/jdtcore.jar
%{_mandir}/man1/ecj.1.gz

%changelog
* Thu Feb 26 2015 Liu Di <liudidi@gmail.com> - 1:4.4.1-2
- 为 Magic 3.0 重建

* Thu Jan 8 2015 Alexander Kurtakov <akurtako@redhat.com> 1:4.4.1-1
- Update to 4.4.1.

* Thu Jul 3 2014 Alexander Kurtakov <akurtako@redhat.com> 1:4.4.0-1
- Update to 4.4 final.
- Drop gcj patches as gcj is not in Fedora anymore and ecj now requires 1.6.

* Thu Jun 12 2014 Alexander Kurtakov <akurtako@redhat.com> 1:4.4.0-0.4.git20140430
- Add additional depmap for maven.

* Mon Jun 9 2014 Alexander Kurtakov <akurtako@redhat.com> 1:4.4.0-0.3.git20140430
- Fix FTBFS.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.4.0-0.2.git20140430
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 1 2014 Alexander Kurtakov <akurtako@redhat.com> 1:4.4.0-0.1.git20140430
- Update to 4.4.0 I-build to make it cope with Java 8.

* Mon Apr 14 2014 Mat Booth <mat.booth@redhat.com> - 1:4.2.1-10
- Drop gcj AOT-compilation support.
- Obsolete -native sub-package.

* Wed Oct 09 2013 gil cattaneo <puntogil@libero.it> 1:4.2.1-9
- enable build of org/eclipse/jdt/internal/compiler/[apt,tool]
  (ant build mode only), required by querydsl
- remove some rpmlint problems (invalid date)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 21 2013 Jon VanAlten <jon.vanalten@redhat.com> - 4.2.1-7
- Add manpage for ecj executable
- Resolves: rhbz#948442

* Tue Apr  9 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.1-6
- Add depmap for org.eclipse.jdt.core.compiler:ecj
- Resolves: rhbz#949938

* Wed Mar 06 2013 Karsten Hopp <karsten@redhat.com> 1:4.2.1-5
- add BR java-devel for !with_gcjbootstrap

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 29 2012 Jon VanAlten <jon.vanalten@redhat.com> 1:4.2.1-3
- Patch GCCMain to avoid dummy symbols.

* Wed Oct 10 2012 Krzysztof Daniel <kdaniel@redhat.com> 1:4.2.1-2
- Add depmap satysfying Tycho req.

* Sun Jul 29 2012 Jon VanAlten <jon.vanalten@redhat.com> 1:4.2.1-1
- Update to 4.2.1 upstream version.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.4.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 18 2012 Alexander Kurtakov <akurtako@redhat.com> 1:3.4.2-13
- Add missing epoch to native subpackage requires.

* Tue Apr 17 2012 Alexander Kurtakov <akurtako@redhat.com> 1:3.4.2-12
- Separate gcj in subpackage.

* Mon Jan 16 2012 Alexander Kurtakov <akurtako@redhat.com> 1:3.4.2-11
- Patch pom file to better represent ecj and not jdt.core .
- Guidelines fixes.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.4.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.4.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 26 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1:3.4.2-8
- Fix add_to_maven_depmap call (Resolves rhbz#655796)

* Mon Dec 21 2009 Deepak Bhole <dbhole@redhat.com> - 1:3.4.2-7
- Fix RHBZ# 490936. If CLASSPATH is not set, add . to default classpath.

* Wed Sep 9 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.4.2-6
- Add maven pom and depmaps.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar 11 2009 Deepak Bhole <dbhole@redhat.com> 1:3.4.2-4
- Add patch to generate full debuginfo for ecj itself

* Tue Mar 10 2009 Deepak Bhole <dbhole@redhat.com> 1:3.4.2-3
- Add BR for aot-compile-rpm

* Tue Mar 10 2009 Deepak Bhole <dbhole@redhat.com> 1:3.4.2-2
- Add BR for ant

* Fri Mar 6 2009 Andrew Overholt <overholt@redhat.com> 1:3.4.2-1
- 3.4.2

* Tue Dec 9 2008 Andrew Overholt <overholt@redhat.com> 1:3.4.1-1
- 3.4.1
- Don't conditionalize building of gcj AOT bits (we're only building
  this for gcj and IcedTea bootstrapping).

* Mon Jan 22 2007 Andrew Overholt <overholt@redhat.com> 3.2.1-1
- Add eclipse-ecj-gcj.patch.

* Fri Jan 12 2007 Andrew Overholt <overholt@redhat.com> 3.2.1-1
- First version for Fedora 7.
- Add BR: java-devel for jar.

* Thu Nov 02 2006 Andrew Overholt <overholt@redhat.com> 1:3.2.1-1jpp
- First version for JPackage.

* Mon Jul 24 2006 Andrew Overholt <overholt@redhat.com> 1:3.2.0-1
- Add versionless ecj.jar symlink in /usr/share/java.

* Wed Jul 19 2006 Andrew Overholt <overholt@redhat.com> 1:3.2.0-1
- 3.2.0.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Mar 07 2005 Andrew Overholt <overholt@redhat.com> 1:3.1.0.M4.9
- Don't build for ppc or ia64.

* Sun Feb 20 2005 Andrew Overholt <overholt@redhat.com> 1:3.1.0.M4.6
- Upgrade back to 3.1M4.
- Don't build for i386 and x86_64.
- Provide eclipse-ecj until we can deprecate this package.

* Fri Jan 14 2005 Andrew Overholt <overholt@redhat.com> 3.1.0.M4.4
- build for all but x86

* Thu Jan 13 2005 Andrew Overholt <overholt@redhat.com> 3.1.0.M4.3
- build for ppc exclusively

* Wed Jan 12 2005 Andrew Overholt <overholt@redhat.com> 3.1.0.M4.2
- Add RPM_OPT_FLAGS workaround.

* Tue Jan 11 2005 Andrew Overholt <overholt@redhat.com> 3.1.0.M4.1
- New version.

* Mon Sep 27 2004 Gary Benson <gbenson@redhat.com> 2.1.3-5
- Rebuild with new katana.

* Thu Jul 22 2004 Gary Benson <gbenson@redhat.com> 2.1.3-4
- Build without bootstrap-ant.
- Split out lib-org-eclipse-jdt-internal-compiler.so.

* Tue Jul  6 2004 Gary Benson <gbenson@redhat.com> 2.1.3-3
- Fix ecj-devel's dependencies.

* Wed Jun  9 2004 Gary Benson <gbenson@redhat.com> 2.1.3-2
- Work around an optimiser failure somewhere in ecj or gcj (#125613).

* Fri May 28 2004 Gary Benson <gbenson@redhat.com>
- Build with katana.

* Mon May 24 2004 Gary Benson <gbenson@redhat.com> 2.1.3-1
- Initial Red Hat Linux build.

* Mon May 24 2004 Gary Benson <gbenson@redhat.com>
- Upgraded to latest version.

* Sun Jul 20 2003 Anthony Green <green@redhat.com>
- Add %%doc

* Fri Jul 18 2003 Anthony Green <green@redhat.com>
- Initial RHUG build.
