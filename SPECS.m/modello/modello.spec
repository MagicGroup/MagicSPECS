Name:           modello
Version:        1.8.1
Release:        7%{?dist}
Epoch:          0
Summary:        Modello Data Model toolkit
Summary(zh_CN.UTF-8): 模型数据模型工具包
# The majority of files are under MIT license, but some of them are
# ASL 2.0 or BSD-licensed.
License:        ASL 2.0 and BSD and MIT
URL:            http://modello.codehaus.org/
Source0:        http://repo2.maven.org/maven2/org/codehaus/%{name}/%{name}/%{version}/%{name}-%{version}-source-release.zip
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt

Patch0001:      0001-MODELLO-284-Fix-handling-of-Boolean-fields-in-StAX-r.patch
Patch0002:      0002-MODELLO-285-Fix-StAX-reader-in-case-no-field-adder-i.patch

BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(com.fasterxml.jackson.core:jackson-annotations)
BuildRequires:  mvn(com.fasterxml.jackson.core:jackson-core)
BuildRequires:  mvn(com.fasterxml.jackson.core:jackson-databind)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.plugins:maven-dependency-plugin)
BuildRequires:  mvn(org.apache.maven:maven-model)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.apache.maven:maven-project)
BuildRequires:  mvn(org.codehaus.plexus:plexus-compiler-api)
BuildRequires:  mvn(org.codehaus.plexus:plexus-compiler-javac)
BuildRequires:  mvn(org.codehaus.plexus:plexus-container-default)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.sonatype.plexus:plexus-build-api)
BuildRequires:  mvn(org.yaml:snakeyaml)

Provides:       modello-maven-plugin = %{epoch}:%{version}-%{release}
Obsoletes:      modello-maven-plugin < 0:1.0-0.a8.3jpp

%description
Modello is a Data Model toolkit in use by the Apache Maven Project.

Modello is a framework for code generation from a simple model.
Modello generates code from a simple model format based on a plugin
architecture, various types of code and descriptors can be generated
from the single model, including Java POJOs, XML
marshallers/unmarshallers, XSD and documentation.

%description -l zh_CN.UTF-8
模型数据模型工具包。

%package javadoc
Summary:        Javadoc for %{name}
Summary(zh_CN.UTF-8): %{name} 的 Javadoc

%description javadoc
API documentation for %{name}.

%description javadoc -l zh_CN.UTF-8
%{name} 的 API 文档。

%prep
%setup -q
%patch0001 -p1
%patch0002 -p1
cp -p %{SOURCE1} LICENSE
# We don't generate site; don't pull extra dependencies.
%pom_remove_plugin :maven-site-plugin
# Avoid using Maven 2.x APIs
sed -i s/maven-project/maven-core/ modello-maven-plugin/pom.xml

%build
# skip tests because we have too old xmlunit in Fedora now (1.0.8)
%mvn_build -f -- -Dmaven.version=3.1.1

%install
%mvn_install

%jpackage_script org.codehaus.modello.ModelloCli "" "" modello:plexus-containers/plexus-container-default:plexus/classworlds:plexus/utils:plexus/plexus-build-api:xbean/xbean-reflect:guava %{name} true

%files -f .mfiles
%dir %{_javadir}/%{name}
%doc LICENSE
%{_bindir}/*

%files javadoc -f .mfiles-javadoc
%doc LICENSE

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 0:1.8.1-7
- 为 Magic 3.0 重建

* Thu Aug 14 2014 Liu Di <liudidi@gmail.com> - 0:1.8.1-6
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.8.1-4
- Use Requires: java-headless rebuild (#1067528)

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.8.1-3
- Backport upstream patches for MODELLO-284 and MODELLO-285

* Mon Jan 27 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.8.1-2
- Use Maven 3.x APIs

* Mon Aug 19 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.8.1-1
- Update to upstream version 1.8.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Apr 19 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7-2
- Build with xmvn
- Use better description
- Simplify build-requires
- Update to current packaging guidelines

* Thu Feb 21 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7-1
- Update to upstream version 1.7

* Mon Feb 18 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.6-1
- Update to upstream version 1.6

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0:1.5-6
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Nov 15 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.5-5
- Add JPP depmap for maven-project to override versionless depmap
- Add missing BR/R: maven-project
- Remove unneeded BR: jpa_api

* Thu Nov 15 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.5-4
- Fix license tag
- Install text of Apache license

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 8 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.5-1
- Update to upstream 1.5.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.4.1-1
- Update to upstream 1.4.1.

* Wed Dec  1 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.4-3
- Fix pom filenames (remove poms of integration tests) Resolves rhbz#655818
- Use jpackage_script macro to generate script

* Thu Aug 26 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.4-2
- Remove dtdparser BR/R

* Tue Jul 20 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.4-1
- Update to latest upstream version
- Re-enable javadoc generation
- Remove old workarounds/patches

* Mon May 24 2010 Yong Yang <yyang@redhat.com> 1.1-2
- Fix JPP pom name
- Disable javadoc:javadoc due to the failure of maven-doxia

* Mon May 24 2010 Yong Yang <yyang@redhat.com> 1.1-1
- Upgrade to 1.1

* Fri May 21 2010 Yong Yang <yyang@redhat.com> 1.0.1-1
- Upgrade to 1.0.1

* Thu Aug 20 2009 Andrew Overholt <overholt@redhat.com> 1.0-0.4.a15.0.1
- Update to alpha 15 courtesy Deepak Bhole

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.3.a8.4.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.2.a8.4.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.0-0.1.a8.4.4
- drop repotag

* Tue Mar 20 2007 Matt Wringe <wringe@redhat.com> 0:1.0-0.1.a8.4jpp.3
- disable gcj support

* Tue Mar 13 2007 Matt Wringe <mwringe@redhat.com> 0:1.0-0.1.a8.4jpp.2
- Change license to MIT to reflex the actual license specified in the
  source headers.
- fix various rpmlint issues

* Mon Feb 26 2007 Tania Bento <tbento@redhat.com> 0:1.0-0.1.a8.4jpp.1
- Fixed %%Release.
- Fixed %%License.
- Fixed %%BuildRoot.
- Removed %%Vendor.
- Removed %%Distribution.
- Defined _with_gcj_support and gcj_support.
- Fixed instructions on how to generate the source drop.

* Fri Dec 01 2006 Deepak Bhole <dbhole@redhat.com> 1.0-0.a8.4jpp
- Added an obsoletes for older versions of the plugin

* Thu Oct 19 2006 Deepak Bhole <dbhole@redhat.com> 1.0-0.a8.3jpp
- Update for maven2 9jpp
- Merge maven-plugin subpackage into the main one

* Mon Sep 11 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.a8.2jpp
- Add gcj_support option
- Add post/postun Requires for javadoc
- Don't omit maven-plugin upload

* Fri Jun 23 2006 Deepak Bhole <dbhole@redhat.com> - 0:1.0-0.a8.1jpp
- Upgrade to 1.0-alpha-8
- Remove ant build, add maven2 build

* Thu Jun 01 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.0-0.a4.2jpp
- First JPP 1.7 build

* Mon Nov 07 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.a4.1jpp
- First JPackage build
