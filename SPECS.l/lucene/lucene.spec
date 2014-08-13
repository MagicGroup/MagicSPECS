# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%{?scl:%scl_package lucene}
%{!?scl:%global pkg_name %{name}}

Summary:        High-performance, full-featured text search engine
Name:           %{?scl_prefix}lucene
Version:        4.8.1
Release:        3%{?dist}
Epoch:          0
License:        ASL 2.0
URL:            http://lucene.apache.org/
Source0:        http://www.apache.org/dist/lucene/java/%{version}/lucene-%{version}-src.tgz
Source1:        lucene-%{version}-core-OSGi-MANIFEST.MF
Source2:        lucene-%{version}-analysis-OSGi-MANIFEST.MF
Source3:        lucene-%{version}-queryparser-OSGi-MANIFEST.MF
#svn export http://svn.apache.org/repos/asf/lucene/dev/tags/lucene_solr_4_8_1/dev-tools/
#tar caf dev-tools-4.8.1.tar.xz dev-tools/
Source4:        dev-tools-%{version}.tar.xz

Patch0:         0001-disable-ivy-settings.patch
Patch1:         0001-dependency-generation.patch

BuildRequires:  git
BuildRequires:  ant
%{!?scl:BuildRequires:  ivy-local}
%{?scl:BuildRequires:  apache-ivy}
BuildRequires:  %{?scl_prefix}icu4j
BuildRequires:  httpcomponents-client
BuildRequires:  jetty-continuation
BuildRequires:  jetty-http
BuildRequires:  jetty-io
BuildRequires:  jetty-server
BuildRequires:  jetty-servlet
BuildRequires:  jetty-util
BuildRequires:  morfologik-stemming
BuildRequires:  uimaj
BuildRequires:  uima-addons
BuildRequires:  spatial4j
BuildRequires:  nekohtml
BuildRequires:  xerces-j2
BuildRequires:  mvn(javax.servlet:servlet-api)
BuildRequires:  mvn(org.antlr:antlr-runtime)
BuildRequires:  maven-local

# test-framework deps
BuildRequires:  junit
BuildRequires:  randomizedtesting-junit4-ant
BuildRequires:  randomizedtesting-runner

%{?scl:Requires: %scl_runtime}

Provides:       %{name}-core = %{epoch}:%{version}-%{release}
# previously used by eclipse but no longer needed
Obsoletes:      %{name}-devel < %{epoch}:%{version}-%{release}
Obsoletes:      %{name}-demo  < %{epoch}:%{version}-%{release}
# previously distributed separately, but merged into main package
Provides:       %{name}-contrib = %{version}-%{release}
Obsoletes:      %{name}-contrib < %{version}-%{release}

BuildArch:      noarch

%description
Apache Lucene is a high-performance, full-featured text search
engine library written entirely in Java. It is a technology suitable
for nearly any application that requires full-text search, especially
cross-platform.

%package parent
Summary:      Parent POM for Lucene

%description parent
Parent POM for Lucene.

%package solr-grandparent
Summary:      Lucene Solr grandparent POM

%description solr-grandparent
Lucene Solr grandparent POM.

%package benchmark
Summary:      Lucene Benchmarking Module

%description benchmark
Lucene Benchmarking Module.

%package replicator
Summary:      Lucene Replicator Module

%description replicator
Lucene Replicator Module.

%package grouping
Summary:      Lucene Grouping Module

%description grouping
Lucene Grouping Module.

%package highlighter
Summary:      Lucene Highlighter Module

%description highlighter
Lucene Highlighter Module.

%package misc
Summary:      Miscellaneous Lucene extensions

%description misc
Miscellaneous Lucene extensions.

%package test-framework
Summary:      Apache Lucene Java Test Framework

%description test-framework
Apache Lucene Java Test Framework.

%package memory
Summary:      Lucene Memory Module

%description memory
High-performance single-document index to compare against Query.

%package expressions
Summary:      Lucene Expressions Module

%description expressions
Dynamically computed values to sort/facet/search on based on a pluggable
grammar.

%package demo
Summary:      Lucene Demo Module

%description demo
Demo for Apache Lucene Java.

%package classification
Summary:      Lucene Classification Module

%description classification
Lucene Classification Module.

%package join
Summary:      Lucene Join Module

%description join
Lucene Join Module.

%package suggest
Summary:      Lucene Suggest Module

%description suggest
Lucene Suggest Module.

%package facet
Summary:      Lucene Facets Module

%description facet
Package for Faceted Indexing and Search.

%package analysis
Summary:      Lucene Common Analyzers

%description analysis
Lucene Common Analyzers.

%package sandbox
Summary:      Lucene Sandbox Module

%description sandbox
Lucene Sandbox Module.

%package queries
Summary:      Lucene Queries Module

%description queries
Lucene Queries Module.

%package spatial
Summary:      Spatial Strategies for Apache Lucene

%description spatial
Spatial Strategies for Apache Lucene.

%package codecs
Summary:      Codecs and postings formats for Apache Lucene

%description codecs
Codecs and postings formats for Apache Lucene.

%package queryparser
Summary:      Lucene QueryParsers Module

%description queryparser
Lucene QueryParsers Module.

%package analyzers-smartcn
Summary:      Smart Chinese Analyzer

%description analyzers-smartcn
Lucene Smart Chinese Analyzer.

%package analyzers-phonetic
Summary:      Lucene Phonetic Filters

%description analyzers-phonetic
Provides phonetic encoding via Commons Codec.

%package analyzers-icu
Summary:      Lucene ICU Analysis Components

%description analyzers-icu
Provides integration with ICU (International Components for Unicode) for
stronger Unicode and internationalization support.

%package analyzers-morfologik
Summary:      Lucene Morfologik Polish Lemmatizer

%description analyzers-morfologik
A dictionary-driven lemmatizer for Polish (includes morphosyntactic
annotations).

%package analyzers-uima
Summary:      Lucene UIMA Analysis Components

%description analyzers-uima
Lucene Integration with UIMA for extracting metadata from arbitrary (text)
fields and enrich document with features extracted from UIMA types (language,
sentences, concepts, named entities, etc.).

%package analyzers-kuromoji
Summary:      Lucene Kuromoji Japanese Morphological Analyzer

%description analyzers-kuromoji
Lucene Kuromoji Japanese Morphological Analyzer.

%package analyzers-stempel
Summary:      Lucene Stempel Analyzer

%description analyzers-stempel
Lucene Stempel Analyzer.


%package javadoc
Summary:        Javadoc for Lucene

%description javadoc
%{summary}.

%prep
%autosetup -n %{pkg_name}-%{version} -S git

# dependency generator expects that the directory name is just lucene
mkdir %{pkg_name}
find -maxdepth 1 ! -name CHANGES.txt ! -name LICENSE.txt ! -name README.txt \
    ! -name NOTICE.txt ! -name MIGRATE.txt  ! -name ivy-settings.xml \
    ! -path %{pkg_name} -exec mv \{} %{pkg_name}/ \;

tar xf %{SOURCE4}

pushd %{pkg_name}

# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;

rm sandbox/src/test/org/apache/lucene/sandbox/queries/regex/TestJakartaRegexpCapabilities.java

# old API
rm -r replicator/src/test/*

# Because ivy-local is not available before F21
%{?scl:ln -s %{_sysconfdir}/ivy/ivysettings.xml}

popd

%mvn_package ":%{pkg_name}-analysis-modules-aggregator" %{pkg_name}-analysis
%mvn_package ":%{pkg_name}-analyzers-common" %{pkg_name}-analysis
%mvn_package ":{*}-aggregator" @1


%build
pushd %{pkg_name}
# generate dependencies
ant filter-pom-templates -Divy.mode=local -Dversion=%{version}

# fix source dir + move to expected place
for pom in `find build/poms/%{pkg_name} -name pom.xml`; do
    sed 's/\${module-path}/${basedir}/g' "$pom" > "${pom##build/poms/%{pkg_name}/}"
done

for module in benchmark misc test-framework demo core/src/java facet \
        analysis/stempel codecs/src/java codecs/src/test queryparser \
        core/src/test memory .; do
    %pom_remove_plugin :forbiddenapis ${module}
done

%pom_disable_module src/test core
%pom_disable_module src/test codecs

# test deps
%pom_add_dep org.ow2.asm:asm::test demo
%pom_add_dep org.ow2.asm:asm-commons::test demo
%pom_add_dep org.antlr:antlr-runtime::test demo

popd

mv lucene/build/poms/pom.xml .

%pom_disable_module solr
%pom_remove_plugin :gmaven-plugin
%pom_remove_plugin :forbiddenapis

%{?scl:scl enable %{scl} - <<"EOF"}
# For some reason TestHtmlParser.testTurkish fails when building inside SCLs
%mvn_build -s %{?scl:-- -Dmaven.test.failure.ignore=true}
%{?scl:EOF}

pushd %{pkg_name}

# add missing OSGi metadata to manifests
mkdir META-INF
unzip -o core/src/java/target/lucene-core-%{version}.jar META-INF/MANIFEST.MF
cat %{SOURCE1} >> META-INF/MANIFEST.MF
sed -i '/^\r$/d' META-INF/MANIFEST.MF
zip -u core/src/java/target/lucene-core-%{version}.jar META-INF/MANIFEST.MF

unzip -o analysis/common/target/lucene-analyzers-common-%{version}.jar META-INF/MANIFEST.MF
cat %{SOURCE2} >> META-INF/MANIFEST.MF
sed -i '/^\r$/d' META-INF/MANIFEST.MF
zip -u analysis/common/target/lucene-analyzers-common-%{version}.jar META-INF/MANIFEST.MF

unzip -o queryparser/target/lucene-queryparser-%{version}.jar META-INF/MANIFEST.MF
cat %{SOURCE3} >> META-INF/MANIFEST.MF
sed -i '/^\r$/d' META-INF/MANIFEST.MF
zip -u queryparser/target/lucene-queryparser-%{version}.jar META-INF/MANIFEST.MF

popd

%install
%{?scl:scl enable %{scl} - <<"EOF"}

# suggest provides spellchecker
%mvn_alias :%{pkg_name}-suggest :%{pkg_name}-spellchecker

# compatibility with existing packages
%mvn_alias :%{pkg_name}-analyzers-common :%{pkg_name}-analyzers

%mvn_install
%{?scl:EOF}

%files -f .mfiles-%{pkg_name}-core
%dir %{_javadir}/%{pkg_name}
%doc CHANGES.txt LICENSE.txt README.txt NOTICE.txt MIGRATE.txt

%files parent -f .mfiles-%{pkg_name}-parent
%files solr-grandparent -f .mfiles-%{pkg_name}-solr-grandparent
%files benchmark -f .mfiles-%{pkg_name}-benchmark
%files replicator -f .mfiles-%{pkg_name}-replicator
%files grouping -f .mfiles-%{pkg_name}-grouping
%files highlighter -f .mfiles-%{pkg_name}-highlighter
%files misc -f .mfiles-%{pkg_name}-misc
%files test-framework -f .mfiles-%{pkg_name}-test-framework
%files memory -f .mfiles-%{pkg_name}-memory
%files expressions -f .mfiles-%{pkg_name}-expressions
%files demo -f .mfiles-%{pkg_name}-demo
%files classification -f .mfiles-%{pkg_name}-classification
%files join -f .mfiles-%{pkg_name}-join
%files suggest -f .mfiles-%{pkg_name}-suggest
%files facet -f .mfiles-%{pkg_name}-facet
%files analysis -f .mfiles-%{pkg_name}-analysis
%files sandbox -f .mfiles-%{pkg_name}-sandbox
%files queries -f .mfiles-%{pkg_name}-queries
%files spatial -f .mfiles-%{pkg_name}-spatial
%files codecs -f .mfiles-%{pkg_name}-codecs
%files queryparser -f .mfiles-%{pkg_name}-queryparser
%files analyzers-smartcn -f .mfiles-%{pkg_name}-analyzers-smartcn
%files analyzers-phonetic -f .mfiles-%{pkg_name}-analyzers-phonetic
%files analyzers-icu -f .mfiles-%{pkg_name}-analyzers-icu
%files analyzers-morfologik -f .mfiles-%{pkg_name}-analyzers-morfologik
%files analyzers-uima -f .mfiles-%{pkg_name}-analyzers-uima
%files analyzers-kuromoji -f .mfiles-%{pkg_name}-analyzers-kuromoji
%files analyzers-stempel -f .mfiles-%{pkg_name}-analyzers-stempel

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:4.8.1-2
- Rebuild to regenerate Maven auto-requires

* Thu May 22 2014 Alexander Kurtakov <akurtako@redhat.com> 0:4.8.1-1
- Update to 4.8.1.

* Fri May 02 2014 Mat Booth <mat.booth@redhat.com> - 0:4.8.0-2
- SCL-ize package

* Fri May 02 2014 Michael Simacek <msimacek@redhat.com> - 0:4.8.0-1
- Update to upstream release 4.8.0

* Fri May 2 2014 Alexander Kurtakov <akurtako@redhat.com> 0:4.8.0-0.1
- Initial 4.8.0 effort.

* Thu Apr 17 2014 Alexander Kurtakov <akurtako@redhat.com> 0:4.7.2-1
- Update to 4.7.2 upstream release.

* Thu Apr 3 2014 Alexander Kurtakov <akurtako@redhat.com> 0:4.7.1-1
- Update to 4.7.1 upstream release.

* Tue Mar 25 2014 Michael Simacek <msimacek@redhat.com> - 0:4.7.0-8
- Enable tests that required newer icu4j and nekohtml

* Fri Mar 14 2014 Michael Simacek <msimacek@redhat.com> - 0:4.7.0-7
- Generate dependencies for POMs
- Revert to using POM files for build and installation (ivy files don't specify
  interproject dependencies)
- Split into subpackages
- Clean up BR's
- Remove unused patches
- Enable tests

* Thu Mar 13 2014 Alexander Kurtakov <akurtako@redhat.com> 0:4.7.0-6
- Don't export package that is not in queryparser.

* Wed Mar 12 2014 Alexander Kurtakov <akurtako@redhat.com> 0:4.7.0-5
- Add queryparser osgi metadata properly.
- Export lucene.analysys.standard too.

* Wed Mar 12 2014 Alexander Kurtakov <akurtako@redhat.com> 0:4.7.0-4
- Export queryParser and queryParser.classic packages for OSGi.

* Thu Mar 06 2014 Severin Gehwolf <sgehwolf@redhat.com> - 0:4.7.0-3
- Fix analyzers-common OSGi metadata: Export o.a.l.a.core and
  fix Require-Bundle header.
- Resolves: RHBZ#1073073

* Wed Mar 05 2014 Roland Grunberg <rgrunber@redhat.com> - 0:4.7.0-2
- Fix Bundle-RequiredExecutionEnvironment for manifests. (rhbz#1072985)

* Tue Mar 04 2014 Michael Simacek <msimacek@redhat.com> - 0:4.7.0-1
- Update to upstream version 4.7.0

* Mon Feb 10 2014 Michael Simacek <msimacek@redhat.com> - 0:4.6.1-1
- Update to upstream version 4.6.1
- Use XMvn to resolve ivy artifacts and for installation
- Remove contrib subpackage (was merged into main package)

* Wed Nov 06 2013 Severin Gehwolf <sgehwolf@redhat.com> 0:3.6.2-4
- Remove unneeded BR jline. Resolves RHBZ#1023015.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 1 2013 Krzysztof Daniel <kdaniel@redhat.com> 0:3.6.2-2
- 830762: lucene ships POMs with uninitialized version properties

* Tue Feb 26 2013 Severin Gehwolf <sgehwolf@redhat.com> 0:3.6.2-1
- Update to upstream release 3.6.2
- Fix build errors related to icu4j v50 incompatibility.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.6.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 5 2012 Severin Gehwolf <sgehwolf@redhat.com> 0:3.6.0-11
- Remove patches which weren't applied (rpmlint warnings).

* Mon Dec 3 2012 Severin Gehwolf <sgehwolf@redhat.com> 0:3.6.0-10
- Upload new tarball for dev-tools as checksum could not be
  reproduced with given commands listed in comment.

* Tue Nov 27 2012 Severin Gehwolf <sgehwolf@redhat.com> 0:3.6.0-9
- Always install grand-parent pom as well.

* Tue Nov 27 2012 Severin Gehwolf <sgehwolf@redhat.com> 0:3.6.0-8
- Always install lucene-parent pom.

* Mon Nov 26 2012 Severin Gehwolf <sgehwolf@redhat.com> 0:3.6.0-7
- Only build lucene-contrib for Fedora.
- This removes BR on icu4j on rhel.

* Fri Nov 23 2012 Severin Gehwolf <sgehwolf@redhat.com> 0:3.6.0-6
- Fix OSGi medatada. In particular:
- Missing import javax.management (lucene-core)
- Missing import javax.xml.parsers and org.xml.sax.helpers
  (lucene-analysis)
- BundleVersion updated to 3.6.0 (lucene-core & lucene-analysis)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 5 2012 Alexander Kurtakov <akurtako@redhat.com> 0:3.6.0-4
- Properly install analyzers.

* Wed Jul 4 2012 Alexander Kurtakov <akurtako@redhat.com> 0:3.6.0-3
- Really fix manifests.

* Wed Jul 4 2012 Alexander Kurtakov <akurtako@redhat.com> 0:3.6.0-2
- Remove duplicated manifest entries.

* Tue Jul 3 2012 Alexander Kurtakov <akurtako@redhat.com> 0:3.6.0-1
- Update to upstream 3.6.0.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.9.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 12 2011 Alexander Kurtakov <akurtako@redhat.com> 0:2.9.4-7
- Fix duplicate Manifes-version warnings.

* Mon Jun 27 2011 Alexander Kurtakov <akurtako@redhat.com> 0:2.9.4-6
- BR zip - fixes FTBFS.

* Tue May 3 2011 Alexander Kurtakov <akurtako@redhat.com> 0:2.9.4-5
- Update OSGi manifests.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.9.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb  8 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.9.4-3
- Fix empty lucene-analyzers (rhbz#675950)

* Wed Feb  2 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.9.4-2
- Add maven metadata (rhbz#566775)

* Mon Jan 31 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.9.4-1
- Update to latest 2.x version (3.x is not API compatible)
- Add new modules
- Enable tests again
- Versionless jars & javadocs

* Wed Oct 13 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.4.1-7
- BR java 1.6.0.

* Wed Oct 13 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.4.1-6
- Fix merge review comments (rhbz#226110).

* Fri Oct 01 2010 Caolán McNamara <caolanm@redhat.com> 0:2.4.1-5
- remove empty lines from MANIFEST.MF

* Fri Oct 01 2010 Caolán McNamara <caolanm@redhat.com> 0:2.4.1-4
- Resolves: rhbz#615609 custom MANIFEST.MF in lucene drops
  "Specification-Version"

* Mon Jun 7 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.4.1-3
- Fix build.
- FIx various rpmlint warnings.

* Fri Mar 5 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.4.1-2
- Drop gcj_support.

* Tue Dec  1 2009 Orion Poplawski <orion@cora.nwra.com> - 0:2.4.1-1
- Update to 2.4.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.3.1-5.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 30 2009 Deepak Bhole <dbhole@redhat.com> - 0:2.3.1-4.5
- rhbz #465344: Fix Implementation-Version and remove Class-Path from manifest

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.3.1-4.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jul 14 2008 Andrew Overholt <overholt@redhat.com> 0:2.3.1-3.4
- Update OSGi manifest data for Eclipse SDK 3.4

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:2.3.1-3.2
- drop repotag

* Wed May 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:2.3.1-3jpp.1
- fix license tag

* Mon May 19 2008 Lubomir Rintel <lkundrak@v3.sk> - 0:2.3.1-3jpp.0
- Correct gcj-compat dependencies, so that this builds on RHEL
- Use --without gcj to disable gcj aot compilation

* Mon May 5 2008 Lubomir Rintel <lkundrak@v3.sk> - 0:2.3.1-2jpp.0
- Unbreak build by repacing the version patch with and -Dversion

* Mon May 5 2008 Lubomir Rintel <lkundrak@v3.sk> - 0:2.3.1-1jpp.0
- 2.3.1, bugfixes only

* Tue Feb 19 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0:2.3.0-1jpp.0
- 2.3.0 (#228141)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.9.1-2jpp.5
- Autorebuild for GCC 4.3

* Fri Sep 21 2007 Deepak Bhole <dbhole@redhat.com> 1.9.1-1jpp.5
- Disable tests due to random hangs (see FIXME comment above ant call)

* Thu Sep 20 2007 Deepak Bhole <dbhole@redhat.com> 0:1.9.1-1jpp.4
- Rebuild for ppc32 execmem issue and new build-id

* Thu Aug 02 2007 Ben Konrath <bkonrath@redhat.com> 0:1.9.1-1jpp.3
- Cleanup packaging of OSGi manifests.

* Tue Jul 31 2007 Ben Konrath <bkonrath@redhat.com> 0:1.9.1-1jpp.2
- Use OSGi manifests from eclipse 3.3.0 instead of merged manifests.
- Resolves: #250221.

* Tue Jul 17 2007 Ben Konrath <bkonrath@redhat.com> 0:1.9.1-1jpp.1
- Disable db sub-package.
- Disable generating test report.
- Add OSGi manifest.
- Obsolete lucene-devel.

* Wed Mar 29 2006 Ralph Apel <r.apel@r-apel.de> 0:1.9.1-1jpp
- Upgrade to 1.9.1

* Tue Apr 26 2005 Ville Skyttä <scop at jpackage.org> - 0:1.4.3-2jpp
- Add unversioned javadoc dir symlink.
- Crosslink with local JDK javadocs.
- Convert specfile to UTF-8.
- Fix URLs.

* Mon Jan 10 2005 Kaj J. Niemi <kajtzu@fi.basen.net> 0:1.4.3
- 1.4.3

* Mon Aug 23 2004 Fernando Nasser <fnasser at redhat.com> - 0:1.3-3jpp
- Rebuild with Ant 1.6.2

* Tue Jun 01 2004 Randy Watler <rwatler at finali.com> - 0:1.3-2jpp
- Upgrade to Ant 1.6.X

* Wed Jan 21 2004 David Walluck <david@anti-microsoft.org> 0:1.3-1jpp
- 1.3

* Wed Mar 26 2003 Ville Skyttä <scop at jpackage.org> - 0:1.2-2jpp
- Rebuilt for JPackage 1.5.

* Thu Mar  6 2003 Ville Skyttä <scop at jpackage.org> - 1.2-1jpp
- First JPackage release.
