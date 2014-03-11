Epoch: 1

%global qualifier 201209141800

%define with_gcjbootstrap %{!?_with_gcjbootstrap:0}%{?_with_gcjbootstrap:1}
%define without_gcjbootstrap %{?_with_gcjbootstrap:0}%{!?_with_gcjbootstrap:1}

Summary: Eclipse Compiler for Java
Name: ecj
Version: 4.2.1
Release: 3%{?dist}
URL: http://www.eclipse.org
License: EPL
Group: Development/Languages
Source0: http://download.eclipse.org/eclipse/downloads/drops4/R-%{version}-%{qualifier}/%{name}src-%{version}.jar
Source1: ecj.sh.in
# Use ECJ for GCJ
# cvs -d:pserver:anonymous@sourceware.org:/cvs/rhug \
# export -D 2009-09-28 eclipse-gcj
# tar cjf ecj-gcj.tar.bz2 eclipse-gcj
Source2: %{name}-gcj.tar.bz2
#Patched from http://repo2.maven.org/maven2/org/eclipse/jdt/core/3.3.0-v_771/core-3.3.0-v_771.pom 
# No dependencies are needed for ecj, dependencies are for using of jdt.core which makes no sense outside of eclipse
Source3: core-3.3.0-v_771.pom
# Always generate debug info when building RPMs (Andrew Haley)
Patch0: %{name}-rpmdebuginfo.patch
Patch1: %{name}-defaultto1.5.patch
Patch2: %{name}-generatedebuginfo.patch
# Patches Source2 for compatibility with newer ecj
Patch3: eclipse-gcj-compat4.2.1.patch
# build.xml fails to include a necessary .props file in the built ecj.jar
Patch4: %{name}-include-props.patch
Patch5: eclipse-gcj-nodummysymbol.patch

BuildRequires: gcc-java >= 4.0.0
BuildRequires: /usr/bin/aot-compile-rpm
BuildRequires: java-gcj-compat

%if ! %{with_gcjbootstrap}
BuildRequires: ant
%endif

Provides: eclipse-ecj = %{epoch}:%{version}-%{release}
Obsoletes: eclipse-ecj < 1:3.4.2-4

%description
ECJ is the Java bytecode compiler of the Eclipse Platform.  It is also known as
the JDT Core batch compiler.

%package native
Summary:	Native(gcj) bits for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires: libgcj >= 4.0.0
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat

%description native
AOT compiled ecj to speed up when running under GCJ.


%prep
%setup -q -c
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch4 -p1

cp %{SOURCE3} pom.xml
# Use ECJ for GCJ's bytecode compiler
tar jxf %{SOURCE2}
mv eclipse-gcj/org/eclipse/jdt/internal/compiler/batch/GCCMain.java \
  org/eclipse/jdt/internal/compiler/batch/
%patch3 -p1
%patch5 -p1
cat eclipse-gcj/gcc.properties >> \
  org/eclipse/jdt/internal/compiler/batch/messages.properties
rm -rf eclipse-gcj

# Remove bits of JDT Core we don't want to build
rm -r org/eclipse/jdt/internal/compiler/tool
rm -r org/eclipse/jdt/internal/compiler/apt
rm -f org/eclipse/jdt/core/BuildJarIndex.java

# JDTCompilerAdapter isn't used by the batch compiler
rm -f org/eclipse/jdt/core/JDTCompilerAdapter.java

%build
%if %{with_gcjbootstrap}
  for f in `find -name '*.java' | cut -c 3- | LC_ALL=C sort`; do
    gcj -Wno-deprecated -C $f
  done

  find -name '*.class' -or -name '*.properties' -or -name '*.rsc' |\
    xargs fastjar cf %{name}-%{version}.jar
%else
   ant
%endif

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

aot-compile-rpm

# poms
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom

%add_maven_depmap -a "org.eclipse.tycho:org.eclipse.jdt.core" JPP-%{name}.pom %{name}.jar

%post native
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi

%postun native
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi

%files
%doc about.html
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}
%{_bindir}/%{name}
%{_javadir}/%{name}.jar
%{_javadir}/eclipse-%{name}.jar
%{_javadir}/jdtcore.jar

%files native
%{_libdir}/gcj/%{name}

%changelog
* Mon Oct 29 2012 Jon VanAlten <jon.vanalten@redhat.com> 1:4.2.1-3
- Patch GCCMain to avoid dummy symbols.

* Wed Oct 10 2012 Krzysztof Daniel <kdaniel@redhat.com> 1:4.2.1-2
- Add depmap satysfying Tycho req.

* Wed Jul 31 2012 Jon VanAlten <jon.vanalten@redhat.com> 1:4.2.1-1
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

* Fri Jul 22 2004 Gary Benson <gbenson@redhat.com> 2.1.3-4
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
