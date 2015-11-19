Name:           aqute-bnd
Version:        2.4.1
Release:        2%{?dist}
Summary:        BND Tool
License:        ASL 2.0
URL:            http://www.aqute.biz/Bnd/Bnd
BuildArch:      noarch

Source0:        https://github.com/bndtools/bnd/archive/%{version}.REL.tar.gz
# Auxiliary parent pom, packager-written
Source1:        parent.pom
Source2:        https://repo1.maven.org/maven2/biz/aQute/bnd/biz.aQute.bnd/%{version}/biz.aQute.bnd-%{version}.pom
Source3:        https://repo1.maven.org/maven2/biz/aQute/bnd/biz.aQute.bndlib/%{version}/biz.aQute.bndlib-%{version}.pom

Patch0:         0001-Port-to-Java-8.patch
Patch1:         0002-Inline-namespace-constants.patch
Patch2:         0003-Use-equinox-s-annotations.patch

BuildRequires:  maven-local
BuildRequires:  mvn(ant:ant)
BuildRequires:  mvn(org.eclipse.osgi:org.eclipse.osgi)
BuildRequires:  mvn(org.eclipse.osgi:org.eclipse.osgi.services)

%description
The bnd tool helps you create and diagnose OSGi bundles.
The key functions are:
- Show the manifest and JAR contents of a bundle
- Wrap a JAR so that it becomes a bundle
- Create a Bundle from a specification and a class path
- Verify the validity of the manifest entries
The tool is capable of acting as:
- Command line tool
- File format
- Directives
- Use of macros

%package -n aqute-bndlib
Summary:        BND library

%description -n aqute-bndlib
%{summary}.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n bnd-%{version}.REL

rm gradlew*
find -name '*.jar' -delete
find -name '*.class' -delete

%patch0 -p1
%patch1 -p1
%patch2 -p1

# reference to Base64 is ambiguous
find -name '*.java' -not -name 'Base64.java' | xargs sed -i 's/\<Base64\>/aQute.lib.base64.Base64/g'

cp -p %{SOURCE1} pom.xml

build_section='
<build>
    <sourceDirectory>src</sourceDirectory>
    <resources>
        <resource>
            <directory>src/</directory>
            <excludes>
                <exclude>**/*.java</exclude>
                <exclude>**/packageinfo</exclude>
            </excludes>
        </resource>
    </resources>
</build>'

pushd biz.aQute.bnd
cp -p %{SOURCE2} pom.xml
%pom_add_parent biz.aQute.bnd:parent:%{version}
%pom_xpath_inject /pom:project "$build_section"

%pom_add_dep ant:ant
%pom_add_dep biz.aQute.bnd:biz.aQute.bndlib:%{version}
%pom_add_dep org.eclipse.osgi:org.eclipse.osgi
%pom_add_dep org.eclipse.osgi:org.eclipse.osgi.services
# The common library is expected to be included in all artifacts
cp -r ../aQute.libg/src/* src/
popd

pushd biz.aQute.bndlib
cp -p %{SOURCE3} pom.xml
%pom_add_parent biz.aQute.bnd:parent:%{version}
%pom_xpath_inject /pom:project "$build_section"

%pom_add_dep org.eclipse.osgi:org.eclipse.osgi
%pom_add_dep org.eclipse.osgi:org.eclipse.osgi.services
# The common library is expected to be included in all artifacts
cp -r ../aQute.libg/src/* src/

sed -i 's|${Bundle-Version}|%{version}|' src/aQute/bnd/osgi/bnd.info

# We don't have metatype-annotations and I haven't found any proper release of it
rm -r src/aQute/bnd/metatype

popd

%mvn_alias biz.aQute.bnd:biz.aQute.bnd :bnd biz.aQute:bnd
%mvn_alias biz.aQute.bnd:biz.aQute.bndlib :bndlib biz.aQute:bndlib

%mvn_package biz.aQute.bnd:biz.aQute.bndlib bndlib
%mvn_package biz.aQute.bnd:parent __noinstall

%build
%mvn_build -- -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

%jpackage_script bnd "" "" aqute-bnd bnd 1

%files -f .mfiles
%doc biz.aQute.bnd/LICENSE
%{_bindir}/bnd

%files -n aqute-bndlib -f .mfiles-bndlib
%doc biz.aQute.bnd/LICENSE

%files javadoc -f .mfiles-javadoc
%doc biz.aQute.bnd/LICENSE

%changelog
* Fri Jul 17 2015 Michael Simacek <msimacek@redhat.com> - 2.4.1-2
- Fix Tool header generation

* Wed Jul 08 2015 Michael Simacek <msimacek@redhat.com> - 2.4.1-1
- Update to upstream version 2.4.1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.363-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.0.363-15
- Disable javadoc doclint

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.363-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.0.363-13
- Use .mfiles generated during build

* Fri May 09 2014 Jaromir Capik <jcapik@redhat.com> - 0.0.363-12
- Fixing ambiguous base64 class

* Fri May 09 2014 Gil Cattaneo <puntogil@libero.it> 0.0.363-11
- fix rhbz#991985
- add source compatibility with ant 1.9
- remove and rebuild from source aQute.runtime.jar
- update to current packaging guidelines

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.0.363-10
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.363-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.363-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.363-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 25 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.0.363-6
- Get rid of unusable eclipse plugins to simplify dependencies

* Fri Mar 02 2012 Jaromir Capik <jcapik@redhat.com> - 0.0.363-5
- Fixing build failures on f16 and later

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.363-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 22 2011 Jaromir Capik <jcapik@redhat.com> - 0.0.363-3
- Resurrection of bundled non-class files

* Thu Sep 22 2011 Jaromir Capik <jcapik@redhat.com> - 0.0.363-2
- Bundled classes removed
- jpackage-utils dependency added to the javadoc subpackage

* Wed Sep 21 2011 Jaromir Capik <jcapik@redhat.com> - 0.0.363-1
- Initial version (cloned from aqute-bndlib 0.0.363)
