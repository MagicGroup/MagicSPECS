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

Name:           checkstyle
Version:        5.7
Release:        3%{?dist}
Summary:        Java source code checker
URL:            http://checkstyle.sourceforge.net/
# src/checkstyle/com/puppycrawl/tools/checkstyle/grammars/java.g is GPLv2+
# Most of the files in contrib/usage/src/checkstyle/com/puppycrawl/tools/checkstyle/checks/usage/transmogrify/ are BSD
License:        LGPLv2+ and GPLv2+ and BSD
Group:          Development/Tools
Source0:        http://download.sf.net/checkstyle/checkstyle-%{version}-src.tar.gz
Source2:        %{name}.catalog

BuildRequires:  java-devel >= 1:1.6.0
BuildRequires:  antlr-maven-plugin
BuildRequires:  apache-commons-beanutils
BuildRequires:  apache-commons-cli
BuildRequires:  apache-commons-logging
BuildRequires:  guava
BuildRequires:  junit
BuildRequires:  maven-local
BuildRequires:  maven-antrun-plugin
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-enforcer-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-site-plugin
BuildRequires:  maven-surefire-plugin

BuildArch:      noarch

Obsoletes:      %{name}-optional < %{version}-%{release}
# revisit later, maybe manual will come back when change from ant to
# maven build system will settle down
Obsoletes:      %{name}-manual < %{version}-%{release}

%description
A tool for checking Java source code for adherence to a set of rules.

%package        demo
Group:          Development/Tools
Summary:        Demos for %{name}
Requires:       %{name} = %{version}-%{release}

%description    demo
Demonstrations and samples for %{name}.

%package        javadoc
Group:          Documentation
Summary:        Javadoc for %{name}

%description    javadoc
API documentation for %{name}.

%prep
%setup -q -n %{name}-%{version}

%pom_remove_parent

sed -i s/guava-jdk5/guava/ pom.xml

# not needed for package build
%pom_remove_plugin :maven-eclipse-plugin

# these are only needed for upstream QA
%pom_remove_plugin :cobertura-maven-plugin
%pom_remove_plugin :exec-maven-plugin
%pom_remove_plugin :maven-linkcheck-plugin

# get rid of system scope
%pom_remove_dep com.sun:tools
%pom_add_dep com.sun:tools

# fix encoding issues in docs
sed -i 's/\r//' LICENSE LICENSE.apache20 README.textile RIGHTS.antlr \
         checkstyle_checks.xml sun_checks.xml suppressions.xml \
         contrib/hooks/*.pl src/site/resources/css/*css \
         java.header

# The following test needs network access, so it would fail on Koji
rm -f src/tests/com/puppycrawl/tools/checkstyle/filters/SuppressionsLoaderTest.java

%build
%mvn_file  : %{name}
%mvn_build


%install
%mvn_install

# script
%jpackage_script com.puppycrawl.tools.checkstyle.Main "" "" checkstyle:antlr:apache-commons-beanutils:apache-commons-cli:apache-commons-logging:guava checkstyle true

# dtds
install -Dm 644 %{SOURCE2} %{buildroot}%{_datadir}/xml/%{name}/catalog
cp -pa src/checkstyle/com/puppycrawl/tools/checkstyle/*.dtd \
  %{buildroot}%{_datadir}/xml/%{name}

# javadoc
install -dm 755  %{buildroot}%{_javadocdir}/%{name}
cp -par target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}

# demo
install -dm 755 %{buildroot}%{_datadir}/%{name}
cp -par contrib/* %{buildroot}%{_datadir}/%{name}

# ant.d
install -dm 755  %{buildroot}%{_sysconfdir}/ant.d
cat > %{buildroot}%{_sysconfdir}/ant.d/%{name} << EOF
checkstyle antlr apache-commons-beanutils apache-commons-cli apache-commons-logging guava
EOF

%post
# Note that we're using a fully versioned catalog, so this is always ok.
if [ -x %{_bindir}/install-catalog -a -d %{_sysconfdir}/sgml ]; then
  %{_bindir}/install-catalog --add \
    %{_sysconfdir}/sgml/%{name}-%{version}-%{release}.cat \
    %{_datadir}/xml/%{name}/catalog > /dev/null || :
fi

%postun
# Note that we're using a fully versioned catalog, so this is always ok.
if [ -x %{_bindir}/install-catalog -a -d %{_sysconfdir}/sgml ]; then
  %{_bindir}/install-catalog --remove \
    %{_sysconfdir}/sgml/%{name}-%{version}-%{release}.cat \
    %{_datadir}/xml/%{name}/catalog > /dev/null || :
fi

%files -f .mfiles
%doc LICENSE README.textile
%doc checkstyle_checks.xml java.header sun_checks.xml suppressions.xml
%{_datadir}/xml/%{name}
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/ant.d/%{name}

%files demo
%{_datadir}/%{name}

%files javadoc -f .mfiles-javadoc
%doc LICENSE


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.7-2
- Remove BuildRequires on maven-surefire-provider-junit4

* Mon May 12 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.7-1
- Update to upstream version 5.7

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 5.6-9
- Use Requires: java-headless rebuild (#1067528)

* Fri Jan 10 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 5.6-8
- Fix FTBFS after ant upgrade to 1.9.2 (#1049902)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 29 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 5.6-6
- Remove cobertura and plugin-exec BRs

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 5.6-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jan 17 2013 Michal Srb <msrb@redhat.com> - 5.6-3
- Build with xmvn

* Tue Dec  4 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.6-2
- Disable unit test that needs network access
- Remove rpm bug workaround

* Mon Dec  3 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.6-1
- Update to upstream version 5.6

* Mon Nov 26 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.5-5
- Install proper license files
- Resolves: rhbz#880272

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 18 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 5.5-3
- Patch eclipse plugin out to simplify BR
- Cleanup and sort requires

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 7 2011 Alexander Kurtakov <akurtako@redhat.com> 5.5-1
- Update to latest upstream (5.5).

* Wed Jul 20 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 5.4-1
- Update to latest upstream (5.4)

* Fri Jul  1 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 5.3-4
- Generate script using jpackage macro (#718039)
- Add missing guava Requires
- Build with maven3 and tweaks according to new guidelines

* Thu Apr 28 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 5.3-3
- Remove epoch from demo subpackage
- Fix script classpaths after jakarta->apache renames

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 21 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 5.3-1
- Use maven as build system (upstream change)
- Javadoc subpackage add Require on jpackage-utils
- Obsolete manual subpackage (not available with mvn)
- Cleanup BRs/Rs
- Remove old patches

* Wed Jun  9 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 5.1-1
- Rebase to new version
- Cleanup of whole spec file
- Enable emma (present in Fedora now)
- Drop epoch

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:4.1-5
- drop repotag
- fix license tag

* Mon Apr 07 2008 Deepak Bhole <dbhole@redhat.com> - 0:4.1-4jpp.3
- Require java-devel >= 1.6 for javadocs (bug in sinjdoc prevents building)

* Fri Apr 04 2008 Deepak Bhole <dbhole@redhat.com> - 0:4.1-4jpp.2
- Remove < 1.5 JVM requirement, and keep tests that need 1.5

* Thu Feb 24 2007 Deepak Bhole <dbhole@redhat.com> - 0:4.1-4jpp.1
- Update per Fedora spec
- Removed emma and excalibur-avalon-logkit dependencies

* Thu Mar 30 2006 Ralph Apel <r.apel@r-apel.de> 0:4.1-3jpp
- replace avalon-logkit by excalibur-avalon-logkit as BR

* Wed Feb 22 2006 Ralph Apel <r.apel@r-apel.de> 0:4.1-2jpp
- add exclude to javadoc task iot build with java-1.4.2-bea

* Wed Feb 15 2006 Ralph Apel <r.apel@r-apel.de> 0:4.1-1jpp
- update to 4.1 for JPP-1.7
- reduce dependencies

* Wed Feb 15 2006 Ralph Apel <r.apel@r-apel.de> 0:3.5-2jpp
- set locale iot avoid failure of GeneratedJava14LexerTest

* Mon Feb 21 2005 David Walluck <david@jpackage.org> 0:3.5-1jpp
- 0.3.5
- fix ant task with new ant
- add more files to %%doc

* Fri Aug 20 2004 Ralph Apel <r.apel at r-apel.de> - 0:3.4-4jpp
- Build with ant-1.6.2
- Runtime Req ant >= 0:1.6.2

* Fri Aug 06 2004 Ralph Apel <r.apel at r-apel.de> - 0:3.4-3jpp
- Void change

* Tue Jun 01 2004 Randy Watler <rwatler at finali.com> - 0:3.4-2jpp
- Upgrade to Ant 1.6.X

* Mon Apr 12 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:3.4-1jpp
- Update to 3.4.
- Make -optional depend on the main package.
- Update DTD catalog, move DTDs to %%{_datadir}/xml/%%{name}.
- New style versionless javadoc dir symlinking.
- Add -optional jar to classpath in startup script if available.

* Tue Jan 20 2004 David Walluck <david@anti-microsoft.org> 0:3.3-1jpp
- 3.3
- rediff patches
- add `optional' subpackage

* Fri Jul 11 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:3.1-2jpp
- Install DTDs into %%{_datadir}/sgml/%%{name}.
- Include catalog for DTDs, and install it if %%{_bindir}/install-catalog
  is available.
- Javadoc crosslinking.

* Wed Jun  4 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:3.1-1jpp
- Update to 3.1.
- Non-versioned javadoc symlinking.

* Fri Apr  4 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:3.0-2jpp
- Rebuild for JPackage 1.5.

* Sat Mar  1 2003 Ville Skyttä <ville.skytta at iki.fi> - 3.0-1jpp
- Update to 3.0.
- Run unit tests during build.
- Separate manual package.

* Sat Sep 14 2002 Ville Skyttä <ville.skytta at iki.fi> 2.4-1jpp
- 2.4.
- No RPM macros in source URL.
- Use (patched) ant build.bindist task to fix docs.

* Thu Jul 11 2002 Ville Skyttä <ville.skytta at iki.fi> 2.3-2jpp
- Unbreak build.
- Add shell script.

* Tue Jul  9 2002 Ville Skyttä <ville.skytta at iki.fi> 2.3-1jpp
- Updated to 2.3.
- Use sed instead of bash 2 extension when symlinking jars during build.
- BuildRequires ant-optional.

* Fri May 10 2002 Ville Skyttä <ville.skytta at iki.fi> 2.2-1jpp
- Updated to 2.2.
- Added versioned requirements.
- Fixed Distribution and Group tags.
- Added demo package.

* Sun Mar 03 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.1-1jpp
- first jpp release
