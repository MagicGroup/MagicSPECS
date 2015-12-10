%global vertag M3

Summary:        Extract class/interface/method definitions from sources
Summary(zh_CN.UTF-8): 从源码中提取类/接口/方法定义
Name:           qdox
Version:        2.0
Release:        0.8.%{vertag}%{?dist}
Epoch:          0
License:        ASL 2.0
URL:            https://github.com/paul-hammant/qdox
BuildArch:      noarch

Source0:        http://repo2.maven.org/maven2/com/thoughtworks/qdox/qdox/%{version}-%{vertag}/%{name}-%{version}-%{vertag}-project.tar.gz
Source1:        qdox-MANIFEST.MF

BuildRequires:  byaccj
BuildRequires:  jflex
BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.maven.plugins:maven-assembly-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-invoker-plugin)
BuildRequires:  mvn(org.codehaus:codehaus-parent:pom:)
BuildRequires:  mvn(org.codehaus.mojo:exec-maven-plugin)
BuildRequires:  mvn(org.mockito:mockito-core)


%description
QDox is a high speed, small footprint parser
for extracting class/interface/method definitions
from source files complete with JavaDoc @tags.
It is designed to be used by active code
generators or documentation tools.

%description -l zh_CN.UTF-8
从源码中提取类/接口/方法定义。

%package javadoc
Summary:        Javadoc for %{name}
Summary(zh_CN.UTF-8): %{name} 的 javadoc

%description javadoc
API docs for %{name}.

%description javadoc -l zh_CN.UTF-8
%{name} 的 javadoc。

%prep
%setup -q -n %{name}-%{version}-%{vertag}
find -name *.jar -delete
rm -rf bootstrap

# We don't need these plugins
%pom_remove_plugin :animal-sniffer-maven-plugin
%pom_remove_plugin :maven-failsafe-plugin
%pom_remove_plugin :maven-jflex-plugin
%pom_xpath_remove pom:build/pom:extensions

%mvn_file : %{name}
%mvn_alias : qdox:qdox

%pom_xpath_set pom:workingDirectory '${basedir}/src/main/java/com/thoughtworks/qdox/parser/impl'

%build
# Generate scanners (upstream does this with maven-jflex-plugin)
jflex --inputstreamctor -d src/main/java/com/thoughtworks/qdox/parser/impl src/grammar/lexer.flex
jflex --inputstreamctor -d src/main/java/com/thoughtworks/qdox/parser/impl src/grammar/commentlexer.flex

# Build artifact
%mvn_build -f -- -Dqdox.byaccj.executable=byaccj

# Inject OSGi manifests
mkdir -p META-INF
cp -p %{SOURCE1} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u target/%{name}-%{version}.jar META-INF/MANIFEST.MF

%install
%mvn_install
magic_rpm_clean.sh

%files -f .mfiles
%doc LICENSE.txt README.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0:2.0-0.8.M3
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0:2.0-0.7.M3
- 为 Magic 3.0 重建

* Wed Sep 09 2015 Liu Di <liudidi@gmail.com> - 0:2.0-0.6.M3
- 为 Magic 3.0 重建

* Fri Jul 24 2015 Liu Di <liudidi@gmail.com> - 0:2.0-0.5.M3
- 为 Magic 3.0 重建

* Mon Jun 22 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.0-0.4.M3
- Update to upstream version 2.0-M3

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.0-0.3.M2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 24 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.0-0.2.M2
- Regenerate build-requires
- Remove obsoletes on qdox-manual

* Mon Oct 27 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.0-1.M2
- Update to upstream version 2.0-M2

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.12.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.12.1-9
- Build with %%mvn_build

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.12.1-8
- Use Requires: java-headless rebuild (#1067528)

* Mon Aug 12 2013 akurtakov <akurtakov@localhost.localdomain> 0:1.12.1-7
- Fix FTBFS bug#993187 .

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.12.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Feb 23 2013 Alexander Kurtakov <akurtako@redhat.com> 0:1.12.1-5
- Remove wagon-webdav extension.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.12.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0:1.12.1-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Jan  9 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.12.1-2
- Run jflex manually before Maven build is started
- Resolves: rhbz#879653

* Tue Dec 11 2012 Alexander Kurtakov <akurtako@redhat.com> 0:1.12.1-1
- Update to latest upstream release.

* Tue Nov 13 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.12-7
- Add license to javadoc subpackage

* Wed Aug 1 2012 Alexander Kurtakov <akurtako@redhat.com> 0:1.12-6
- Inject osgi metadata from eclipse orbit.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 10 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.12-3
- Build with maven 3.x.
- Adapt to current guidelines.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 5 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.12-1
- Update to new version.

* Mon Jun 7 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.11-3
- Make sure to remove all yacc executables.

* Mon Jun 7 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.11-2
- Symlink byaccj to both yacc.linux and yacc.linux.x86_64 to keep it building as noarch.

* Mon Mar 15 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.11-1
- Update to 1.11.

* Mon Feb 15 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.10.1-2
- Rebuild for rhbz#565013.

* Thu Jan 14 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.10.1-1
- Update to upstream 1.10.1.

* Sat Sep 19 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.9.2-2
- Remove not needed sources.

* Tue Aug 18 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.9.2-1
- Update to 1.9.2.

* Fri Apr 03 2009 Ralph Apel <r.apel at r-apel.de> 0:1.8-1.jpp5
- 1.8 as qdox18 because of qdox frozen at 1.6.1 in JPP-5

* Tue Jul 01 2008 Ralph Apel <r.apel at r-apel.de> 0:1.6.3-5.jpp5
- Restore to devel
- Drop mockobjects BR

* Fri Jun 13 2008 Ralph Apel <r.apel at r-apel.de> 0:1.6.3-4.jpp5
- Add com.thoughtworks.qdox groupId to depmap frag

* Tue Feb 26 2008 Ralph Apel <r.apel at r-apel.de> 0:1.6.3-3jpp
- Add settings file
- Fix pom marking jmock dependency as of scope test
- Fix -jpp-depmap.xml for asm2-parent

* Mon Nov 26 2007 Ralph Apel <r.apel at r-apel.de> 0:1.6.3-2jpp
- Fix maven macro value

* Thu Nov 22 2007 Ralph Apel <r.apel at r-apel.de> 0:1.6.3-1jpp
- Upgrade to 1.6.3

* Wed May 30 2007 Ralph Apel <r.apel at r-apel.de> 0:1.6.2-1jpp
- Upgrade to 1.6.2
- Activate tests while building with ant
- Make Vendor, Distribution based on macro
- Install depmap frags, poms

* Thu Mar 22 2007 Vivek Lakshmanan <vivekl@redhat.com> 0:1.6.1-1jpp.ep1.4
- Rebuild with fixed component-info.xml

* Fri Feb 23 2007 Ralph Apel <r.apel at r-apel.de> 0:1.5-3jpp
- Add option to build without maven
- Omit tests when building without maven
- Add gcj_support option

* Mon Feb 20 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.5-2jpp
- Rebuild for JPP-1.7, adapting to maven-1.1

* Wed Nov 16 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.5-1jpp
- Upgrade to 1.5
- Build is now done with maven and requires jflex and byaccj

* Wed Aug 25 2004 Fernando Nasser <fnasser@redhat.com> - 0:1.4-3jpp
- Rebuild with Ant 1.6.2

* Fri Aug 06 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.4-2jpp
- Upgrade to ant-1.6.X

* Mon Jun 07 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.4-1jpp
- Upgrade to 1.4
- Drop Requires: mockobjects (Build/Test only)

* Tue Feb 24 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.3-1jpp
- First JPackage release
