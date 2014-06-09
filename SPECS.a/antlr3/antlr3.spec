#%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%global with_bootstrap 0

%global antlr_version 3.4
#%global python_runtime_version 3.1.3
%global javascript_runtime_version 3.1

Summary:            ANother Tool for Language Recognition
Name:               antlr3
Version:            %{antlr_version}
Release:            15%{?dist}
URL:                http://www.antlr.org/
Source0:            http://www.antlr.org/download/antlr-%{antlr_version}.tar.gz
Source1:            http://www.antlr.org/download/C/libantlr3c-%{antlr_version}.tar.gz
Source2:            http://www.antlr.org/download/Python/antlr_python_runtime-%{python_runtime_version}.tar.gz
Source3:            http://www.antlr.org/download/antlr-javascript-runtime-%{javascript_runtime_version}.zip
Source5:            antlr3
%if %{with_bootstrap}
Source6:            settings.xml
Source7:            http://www.antlr.org/download/antlr-%{antlr_version}.jar
Source8:            http://mirrors.ibiblio.org/pub/mirrors/maven2/org/antlr/antlr3-maven-plugin/%{antlr_version}/antlr3-maven-plugin-%{antlr_version}.jar
%endif
Source9:            antlr-runtime-MANIFEST.MF
License:            BSD
Group:              Development/Libraries
BuildRequires:      java-devel >= 1:1.6.0
BuildRequires:      jpackage-utils
BuildRequires:      maven-local
BuildRequires:      maven-enforcer-plugin
BuildRequires:      maven-plugin-bundle
BuildRequires:      maven-assembly-plugin
BuildRequires:      maven-shared-reporting-impl
BuildRequires:      maven-surefire-provider-junit4
BuildRequires:      maven-install-plugin
BuildRequires:      buildnumber-maven-plugin
BuildRequires:      junit
BuildRequires:      tomcat-servlet-3.0-api
BuildRequires:      stringtemplate4
BuildRequires:      stringtemplate
BuildRequires:      felix-parent
BuildRequires:      zip
%if ! %{with_bootstrap}
BuildRequires:      antlr3-tool >= 3.2
%endif

# we don't build it now
Obsoletes:       antlr3-gunit < 3.2-15

%description
ANother Tool for Language Recognition, is a language tool
that provides a framework for constructing recognizers,
interpreters, compilers, and translators from grammatical
descriptions containing actions in a variety of target languages.

%package     tool
Group:       Development/Libraries
Summary:     ANother Tool for Language Recognition
BuildArch:   noarch
Requires:    jpackage-utils
Requires:    java >= 1:1.6.0
Provides:    %{name} = %{antlr_version}-%{release}
Obsoletes:   %{name} < %{antlr_version}-%{release}
Requires:    %{name}-java = %{antlr_version}-%{release}
Requires:    stringtemplate4

%description tool
ANother Tool for Language Recognition, is a language tool
that provides a framework for constructing recognizers,
interpreters, compilers, and translators from grammatical
descriptions containing actions in a variety of target languages.

%package     java
Group:       Development/Libraries
Summary:     Java run-time support for ANTLR-generated parsers
BuildArch:   noarch
Requires:    stringtemplate4
Requires:    stringtemplate
Requires:    jpackage-utils
Requires:    java >= 1:1.6.0

%description java
Java run-time support for ANTLR-generated parsers

%package      javascript
Group:        Development/Libraries
Summary:      Javascript run-time support for ANTLR-generated parsers
Version:      %{javascript_runtime_version}
BuildArch:    noarch

%description  javascript
Javascript run-time support for ANTLR-generated parsers

%package   C
Group:     Development/Libraries
Summary:   C run-time support for ANTLR-generated parsers

%description C
C run-time support for ANTLR-generated parsers

%package   C-devel
Group:     Development/Libraries
Summary:   Header files for the C bindings for ANTLR-generated parsers
Requires:  %{name}-C = %{antlr_version}-%{release}

%description C-devel
Header files for the C bindings for ANTLR-generated parsers

%package        C-docs
Group:          Documentation
Summary:        API documentation for the C run-time support for ANTLR-generated parsers
BuildArch:      noarch
BuildRequires:  graphviz
BuildRequires:  doxygen
Requires:       %{name}-C = %{antlr_version}-%{release}

%description    C-docs
This package contains doxygen documentation with instruction
on how to use the C target in ANTLR and complete API description of the
C run-time support for ANTLR-generated parsers.

#%package        python
#Group:          Development/Libraries
#Summary:        Python run-time support for ANTLR-generated parsers
#BuildRequires:  python-devel
#BuildRequires:  python-setuptools-devel
#BuildArch:      noarch
#Version:        %{python_runtime_version}
#
#%description    python
#Python run-time support for ANTLR-generated parsers

%prep
%setup -q -n antlr-%{antlr_version} -a 1 -a 2 -a 3
%if %{with_bootstrap}
cp %{SOURCE6} settings.xml
%endif
sed -i "s,\${buildNumber},`cat %{_sysconfdir}/fedora-release` `date`," tool/src/main/resources/org/antlr/antlr.properties

sed -i 's:<module>antlr3-maven-archetype</module>::' pom.xml
sed -i 's:<module>gunit</module>::' pom.xml
sed -i 's:<module>gunit-maven-plugin</module>::' pom.xml

# compile for target 1.6, see BZ#842572
sed -i 's/jsr14/1.6/' antlr3-maven-archetype/src/main/resources/archetype-resources/pom.xml \
                      antlr3-maven-plugin/pom.xml \
					  gunit/pom.xml \
					  gunit-maven-plugin/pom.xml \
					  pom.xml \
					  runtime/Java/pom.xml \
					  tool/pom.xml

# remove corrupted files:
rm antlr3-maven-plugin/src/main/java/org/antlr/mojo/antlr3/._*
rm gunit-maven-plugin/src/main/java/org/antlr/mojo/antlr3/._GUnitExecuteMojo.java


%build

export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

%if %{with_bootstrap}
# we need antlr3-maven-plugin in place
sed -i -e \
"s|<url>__JPP_URL_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" \
  settings.xml
  sed -i -e \
  "s|<url>__JAVADIR_PLACEHOLDER__</url>|<url>file://`pwd`/external_repo</url>|g" \
  settings.xml
  sed -i -e \
  "s|<url>__MAVENREPO_DIR_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" \
  settings.xml
  sed -i -e \
  "s|<url>__MAVENDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/maven2/plugins</url>|g" \
  settings.xml

mkdir -p $MAVEN_REPO_LOCAL/JPP/maven2/default_poms/
mkdir -p $MAVEN_REPO_LOCAL/org.antlr/
cp antlr3-maven-plugin/pom.xml $MAVEN_REPO_LOCAL/JPP/maven2/default_poms/JPP-antlr3-maven-plugin.pom
# install prebuilt antlr and antlr3-maven-plugin into repository
# Man, this is hackish. Hold your nose.
cp %{SOURCE7} $MAVEN_REPO_LOCAL/org.antlr/antlr.jar
cp %{SOURCE8} $MAVEN_REPO_LOCAL/org.antlr/antlr3-maven-plugin.jar
%endif

# Build antlr
%if %{with_bootstrap}
mvn-rpmbuild -s $(pwd)/settings.xml -Dmaven.repo.local=$MAVEN_REPO_LOCAL -Dmaven.test.skip=true -Dmaven.compile.target=1.6 install
%else
mvn-rpmbuild -Dmaven.repo.local=$MAVEN_REPO_LOCAL -Dmaven.test.skip=true -Dmaven.compile.target=1.6 install
%endif

# Build the plugin
pushd antlr3-maven-plugin
mvn-rpmbuild -Dmaven.repo.local=$MAVEN_REPO_LOCAL -Dmaven.compile.target=1.6 install javadoc:javadoc
popd

## Build the python runtime
#pushd antlr_python_runtime-%{python_runtime_version}
#%{__python} setup.py build
#popd

# Build the C runtime
pushd libantlr3c-%{antlr_version}-beta4

%configure --disable-abiflags --enable-debuginfo \
%ifarch x86_64 ppc64 s390x sparc64
    --enable-64bit
%else
    %{nil}
%endif

sed -i "s/CFLAGS = .*/CFLAGS = $RPM_OPT_FLAGS/" Makefile
make %{?_smp_mflags}
doxygen -u # update doxygen configuration file
doxygen # build doxygen documentation
popd

# inject OSGi manifests
mkdir -p META-INF
cp -p %{SOURCE9} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u runtime/Java/target/antlr-runtime-%{antlr_version}.jar META-INF/MANIFEST.MF

%install
mkdir -p $RPM_BUILD_ROOT{%{_javadir},%{_mavenpomdir},%{_bindir},%{_datadir}/antlr,%{_mandir}}

# install maven POMs
install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-antlr3-master.pom
%add_maven_depmap JPP-antlr3-master.pom

install -pm 644 runtime/Java/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-antlr3-runtime.pom
install -pm 644 tool/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-antlr3.pom
install -pm 644 antlr3-maven-plugin/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-antlr3-maven-plugin.pom
install -pm 644 gunit-maven-plugin/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-maven-gunit-plugin.pom

# install jars
install -m 644 runtime/Java/target/antlr-runtime-*.jar \
        $RPM_BUILD_ROOT%{_datadir}/java/antlr3-runtime.jar
%add_maven_depmap JPP-antlr3-runtime.pom antlr3-runtime.jar

install -m 644 tool/target/antlr-*.jar \
        $RPM_BUILD_ROOT%{_datadir}/java/antlr3.jar
%add_maven_depmap JPP-antlr3.pom antlr3.jar

install -m 644 antlr3-maven-plugin/target/%{name}-maven-plugin-%{antlr_version}.jar \
        $RPM_BUILD_ROOT%{_datadir}/java/%{name}-maven-plugin.jar
%add_maven_depmap JPP-%{name}-maven-plugin.pom %{name}-maven-plugin.jar

# We disable gunit because it currently fails to build, maybe after upgrade?
#install gunit/target/gunit-%{antlr_version}.jar \
#        $RPM_BUILD_ROOT%{_datadir}/java/gunit.jar

#install -m 644 gunit-maven-plugin/target/maven-gunit-plugin-%{antlr_version}.jar \
#        $RPM_BUILD_ROOT%{_datadir}/java/maven-gunit-plugin.jar
#%%add_maven_depmap JPP-maven-gunit-plugin.pom maven-gunit.plugin.jar


# install wrapper script
install -m 755 %{SOURCE5} $RPM_BUILD_ROOT%{_bindir}/antlr3

## install python runtime
#pushd antlr_python_runtime-%{python_runtime_version}
#%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
#chmod a+x $RPM_BUILD_ROOT%{python_sitelib}/antlr_python_runtime-*
#popd

# install C runtime
pushd libantlr3c-%{antlr_version}-beta4
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/libantlr3c.{a,la}
pushd api/man/man3
for file in `ls -1 * | grep -vi "^antlr3"`; do
    mv $file antlr3-$file
done
sed -i -e 's,^\.so man3/pANTLR3,.so man3/antlr3-pANTLR3,' `grep -rl 'man3/pANTLR3' .`
gzip *
popd
mv api/man/man3 $RPM_BUILD_ROOT%{_mandir}/
rmdir api/man
popd

# install javascript runtime
pushd antlr-javascript-runtime-%{javascript_runtime_version}
install -pm 644 *.js $RPM_BUILD_ROOT%{_datadir}/antlr/
popd

%post C -p /sbin/ldconfig

%postun C -p /sbin/ldconfig

%files tool
%doc tool/{README.txt,LICENSE.txt,CHANGES.txt}
%{_javadir}/antlr3.jar
%{_javadir}/antlr3-maven*.jar
%{_bindir}/antlr3

#%files python
#%doc tool/LICENSE.txt
#%{python_sitelib}/antlr3/*
#%{python_sitelib}/antlr_python_runtime-*

%files C
%doc tool/LICENSE.txt
%{_libdir}/libantlr3c.so

%files C-devel
%{_includedir}/antlr3*
%{_mandir}/man3/*

%files C-docs
%doc libantlr3c-%{antlr_version}-beta4/api/

%files java
%doc tool/LICENSE.txt
%{_javadir}/*runtime*.jar
%{_mavenpomdir}/*.pom
%config %{_mavendepmapfragdir}/antlr3

%files javascript
%doc tool/LICENSE.txt
%{_datadir}/antlr/

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 3.4-13
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sun Sep 09 2012 Miloš Jakubíček <xjakub@fi.muni.cz> - 3.4-12
- Fix wrong man page references (see BZ#855619)

* Tue Aug 21 2012 Miloš Jakubíček <xjakub@fi.muni.cz> - 3.4-11
- Now really compile for Java 1.6 everything

 *Sat Aug 18 2012 Miloš Jakubíček <xjakub@fi.muni.cz> - 3.4-10
- Explicitly compile for Java 1.5, to (maybe?) fix BZ#842572

* Mon Aug 6 2012 Alexander Kurtakov <akurtako@redhat.com> 3.4-9
- Inject org.antlr.runtime OSGi metadata.
- Update BRs to newer versions.

* Tue Jul 24 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.4-8
- Add back requires on stringtemplate for java subpackage

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Miloš Jakubíček <xjakub@fi.muni.cz> - 3.4-6
- Fixed missing stringtemplate4 in antlr3 generator classpath
- Cleanup of Requires and BuildRequires on antlr2

* Thu Feb 23 2012 Miloš Jakubíček <xjakub@fi.muni.cz> - 3.4-5
- Disable python runtime (incompatible with current antlr version)

* Wed Feb 22 2012 Miloš Jakubíček <xjakub@fi.muni.cz> - 3.4-4
- Fix permissions for egg-info dir (fixes BZ#790499)

* Thu Feb 16 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.4-3
- Use wildcards for installing jars (different results on different releases)

* Thu Feb 16 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.4-2
- Add builnumber plugin to buildrequires
- Tab/space cleanup

* Mon Jan 23 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.4-1
- Update antlr version to 3.4
- Move to maven3 build, update macros etc
- Remove gunit for now

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 09 2011 Dan Horák <dan[at]danny.cz> - 3.2-15
- fix build on other arches

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 14 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.2-13
- Add stringtemplate to Requires of java subpackage
- Use tomcat6 for building
- Use felix-parent and cleanup BRs on maven plugins

* Thu Nov 25 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.2-12
- Move all pom files into java subpackage
- Fix pom filenames (Resolves rhbz#655831)
- Add java subpackage Requires for gunit subpackage

* Wed Oct 13 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 3.2-11
- non-bootstrap build

* Wed Oct 13 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 3.2-10
- fix pom patch
- fix bootstrapping
- fix dependencies

* Wed Aug 11 2010 David Malcolm <dmalcolm@redhat.com> - 3.2-9
- recompiling .py files against Python 2.7 (rhbz#623269)

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jun 17 2010 Lubomir Rintel <lkundrak@v3.sk> - 3.2-7
- Add master and runtime poms (#605267)

* Sat May 01 2010 Miloš Jakubíček <xjakub@fi.muni.cz> - 3.2-6
- Patch the Python runtime to print just a warning in case of version mismatch
  instead of raising an exception (since there is a good change it will work).

* Thu Apr 22 2010 Miloš Jakubíček <xjakub@fi.muni.cz> - 3.2-5
- Build the C runtime with --enable-64bit on x86_64 to avoid undeterministic
  segfaults caused by possible invalid conversion of 64bit pointers to int32_t

* Mon Mar 08 2010 Miloš Jakubíček <xjakub@fi.muni.cz> - 3.2-4
- Patch Java runtime build to include OSGi meta-information in the manifest
  (thanks to Mat Booth)
- Add "antlr3" prefix to all man pages to prevent namespace conflicts with
  standard man pages included in the man-pages package
- Split headers and man pages into a C-devel subpackage
- Fix multiple file ownership of Java runtime and gunit by the tool package

* Tue Mar 02 2010 Miloš Jakubíček <xjakub@fi.muni.cz> - 3.2-3
- Rebuilt in non-bootstrap mode.

* Sun Jan 31 2010 Milos Jakubicek <xjakub@fi.muni.cz> - 3.2-2
- Build the doxygen documentation for the C target in a C-docs subpackage
- BuildRequires/Requires cleanup across subpackages

* Sat Jan 30 2010 Milos Jakubicek <xjakub@fi.muni.cz> - 3.2-1
- Update to 3.2, bootstrap build.
- Build bindings for C and JavaScript as well as gunit and maven plugin.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 17 2009 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> - 3.1.1-7
- Fix the name of the jar to antlr.jar

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 12 2009 Colin Walters <walters@redhat.com> - 3.1.1-5
- Add bcel to build path

* Mon Jan 12 2009 Colin Walters <walters@redhat.com> - 3.1.1-4
- Add bcel build dep to version jar name

* Mon Nov 10 2008 Colin Walters <walters@redhat.com> - 3.1.1-3
- Add antlr3 script

* Mon Nov  6 2008 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> - 3.1.1-2
- Fix the install of the jar (remove the version)

* Mon Nov  3 2008 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> - 3.1.1-1
- Update to version 3.1.1
- Add python runtime subpackage

* Fri Jun 27 2008 Colin Walters <walters@redhat.com> - 3.0.1-2
- Fix some BRs

* Sun Apr 06 2008 Colin Walters <walters@redhat.com> - 3.0.1-1
- First version
