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

Summary:        Java XPath, XSLT 2.0 and XQuery implementation
Name:           saxon
Version:        9.3.0.4
Release:        16%{?dist}
# net.sf.saxon.om.XMLChar is from ASL-licensed Xerces
# net/sf/saxon/option/jdom/ is MPLv1.1
# net/sf/saxon/serialize/codenorm/ is UCD
# net/sf/saxon/expr/sort/GenericSorter.java is MIT
# net/sf/saxon/expr/Tokenizer.java and few other bits are BSD
License:        MPLv1.0 and MPLv1.1 and ASL 1.1 and UCD and MIT
URL:            http://saxon.sourceforge.net/
Source0:        https://downloads.sourceforge.net/project/saxon/Saxon-HE/9.3/saxon9-3-0-4source.zip
Source1:        %{name}.saxon.script
Source2:        %{name}.saxonq.script
Source3:        %{name}.build.script
Source4:        %{name}.1
Source5:        %{name}q.1
Source6:        https://downloads.sourceforge.net/project/saxon/Saxon-HE/9.3/saxon-resources9-3.zip
Source7:        saxon-%{version}.pom
Source8:        http://www.mozilla.org/MPL/1.0/index.txt#/mpl-1.0.txt
Source9:        http://www.mozilla.org/MPL/1.0/index.txt#/mpl-1.1.txt
BuildRequires:  unzip
BuildRequires:  java-devel >= 1:1.6.0
BuildRequires:  ant
BuildRequires:  javapackages-local
BuildRequires:  bea-stax-api
BuildRequires:  xml-commons-apis
BuildRequires:  xom
BuildRequires:  jdom >= 0:1.0-0.b7
BuildRequires:  java-javadoc
BuildRequires:  jdom-javadoc >= 0:1.0-0.b9.3jpp
BuildRequires:  dom4j
Requires:       bea-stax-api
Requires:       bea-stax
Requires:       chkconfig
Provides:       jaxp_transform_impl = %{version}-%{release}

# Older versions were split into multile packages
Obsoletes:  %{name}-xpath < %{version}-%{release}
Obsoletes:  %{name}-xom < %{version}-%{release}
Obsoletes:  %{name}-sql < %{version}-%{release}
Obsoletes:  %{name}-jdom < %{version}-%{release}
Obsoletes:  %{name}-dom < %{version}-%{release}

BuildArch:      noarch

%description
Saxon HE is Saxonica's non-schema-aware implementation of the XPath 2.0,
XSLT 2.0, and XQuery 1.0 specifications aligned with the W3C Candidate
Recommendation published on 3 November 2005. It is a complete and
conformant implementation, providing all the mandatory features of
those specifications and nearly all the optional features.

%package        manual
Summary:        Manual for %{name}

%description    manual
Manual for %{name}.

%package        javadoc
Summary:        Javadoc for %{name}

%description    javadoc
Javadoc for %{name}.

%package        demo
Summary:        Demos for %{name}
Requires:       %{name} = %{version}-%{release}

%description    demo
Demonstrations and samples for %{name}.

%package        scripts
Summary:        Utility scripts for %{name}
Requires:       %{name} = %{version}-%{release}

%description    scripts
Utility scripts for %{name}.


%prep
%setup -q -c

unzip -q %{SOURCE6}
cp -p %{SOURCE3} ./build.xml

# deadNET
rm -rf net/sf/saxon/dotnet samples/cs

# Depends on XQJ (javax.xml.xquery)
rm -rf net/sf/saxon/xqj

# This requires a EE edition feature (com.saxonica.xsltextn)
rm -rf net/sf/saxon/option/sql/SQLElementFactory.java

# cleanup unnecessary stuff we'll build ourselves
rm -rf docs/api
find . \( -name "*.jar" -name "*.pyc" \) -delete

cp %{SOURCE8} %{SOURCE9} .

%build
mkdir -p build/classes
cat >build/classes/edition.properties <<EOF
config=net.sf.saxon.Configuration
platform=net.sf.saxon.java.JavaPlatform
EOF

export CLASSPATH=%(build-classpath xml-commons-apis jdom xom bea-stax-api dom4j)
ant \
  -Dj2se.javadoc=%{_javadocdir}/java \
  -Djdom.javadoc=%{_javadocdir}/jdom

%mvn_artifact %{SOURCE7} build/lib/saxon.jar
%mvn_alias : net.sf.saxon:saxon::dom:

%install
%mvn_install

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr build/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# demo
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr samples/* $RPM_BUILD_ROOT%{_datadir}/%{name}

# scripts
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -p -m755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/%{name}
install -p -m755 %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/%{name}q
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -p -m644 %{SOURCE4} $RPM_BUILD_ROOT%{_mandir}/man1/%{name}.1
install -p -m644 %{SOURCE5} $RPM_BUILD_ROOT%{_mandir}/man1/%{name}q.1

# jaxp_transform_impl ghost symlink
ln -s %{_sysconfdir}/alternatives \
  $RPM_BUILD_ROOT%{_javadir}/jaxp_transform_impl.jar

%post
update-alternatives --install %{_javadir}/jaxp_transform_impl.jar \
  jaxp_transform_impl %{_javadir}/saxon/saxon.jar 25

%preun
{
  [ $1 -eq 0 ] || exit 0
  update-alternatives --remove jaxp_transform_impl %{_javadir}/saxon/saxon.jar
} >/dev/null 2>&1 || :

%files -f .mfiles
%doc mpl-1.0.txt mpl-1.1.txt
%dir %{_javadir}/%{name}
%ghost %{_javadir}/jaxp_transform_impl.jar

%files manual
%doc doc/*

%files javadoc
%doc mpl-1.0.txt mpl-1.1.txt
%{_javadocdir}/%{name}

%files demo
%{_datadir}/%{name}

%files scripts
%{_bindir}/%{name}
%{_bindir}/%{name}q
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}q.1*


%changelog
* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.3.0.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 15 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 9.3.0.4-15
- Remove C# samples

* Mon Jan 12 2015 Mat Booth <mat.booth@redhat.com> - 9.3.0.4-14
- Resolves: rhbz#1023753 - Fix script param handling.
- Update man pages.

* Thu Jun 12 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 9.3.0.4-13
- Restore removed Maven alias for net.sf.saxon:saxon::dom:

* Mon Jun 09 2014 Mat Booth <mat.booth@redhat.com> - 9.3.0.4-12
- Install with maven
- Drop ancient javadoc/rpm bug workaround
- Minor spec file cleanups for latest guidelines

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.3.0.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Jan 31 2014 Ville Skyttä <ville.skytta@iki.fi> - 9.3.0.4-10
- Add TransformerFactory and XPathFactory service providers to jar.

* Tue Oct 15 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 9.3.0.4-9
- Add alias with 'dom' classifier

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.3.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.3.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 15 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 9.3.0.4-6
- Fix license tag properly to include all pieces and add comments

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.3.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Andy Grimm <agrimm@gmail.com> - 9.3.0.4-4
- Fix option syntax in scripts when using xml-commons-resolver (#831631)

* Wed Feb 15 2012 Andy Grimm <agrimm@gmail.com> - 9.3.0.4-3
- Fix FTBFS (#791033)
- Add a simple POM file

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.3.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Feb 17 2011 Alexander Kurtakov <akurtako@redhat.com> 9.3.0.4-1
- Update to new upstream version.
- Adapt to current guidelines.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 03 2009 Lubomir Rintel <lkundrak@v3.sk> - 9.2.0.3-1
- New package, based on saxon8

* Tue Nov 03 2009 Lubomir Rintel <lkundrak@v3.sk> - 0:8.7-1
- Tidied up for Fedora

* Tue Mar 14 2006 Deepak Bhole <dbhole@redhat.com> - 0:B.8.7-1jpp
- Changed package name for compatibility
- Upgraded to 8.7
- Added saxonq script for queries
- Updated man pages

* Mon Jan 30 2006 Ralph Apel <r.apel@r-apel.de> - 0:8.6.1-1jpp
- Derive saxonb8 from saxon7

* Mon Sep 05 2005 Ralph Apel <r.apel@r-apel.de> - 0:7.9.1-1jpp
- Derive saxon7 from saxon
- no more aelfred nor fop subpackages

* Fri Sep 03 2004 Fernando Nasser <fnasser@redhat.com> - 0:6.5.3-3jpp
- Rebuilt with Ant 1.6.2

* Mon Jul 19 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:6.5.3-2jpp
- Apply two patches for known limitations from
  http://saxon.sourceforge.net/saxon6.5.3/limitations.html
- Make the command line script use xml-commons-resolver if it's available.
- Include man page for command line script.
- Add patch to fix command line option handling and document missing options.
- New style versionless javadoc dir symlinking.
- Crosslink with local J2SE javadocs.
- Add missing jdom-javadoc build dependency.

* Sun Aug 31 2003 Ville Skyttä <ville.skytta@iki.fi> - 0:6.5.3-1jpp
- Update to 6.5.3.
- Crosslink with local xml-commons-apis and fop javadocs.

* Tue Jun  3 2003 Ville Skyttä <ville.skytta@iki.fi> - 0:6.5.2-7jpp
- Non-versioned javadoc symlinking.
- Include Main-Class attribute in saxon.jar.
- Own (ghost) %%{_javadir}/jaxp_transform_impl.jar.
- Remove alternatives in preun instead of postun.

* Thu Apr 17 2003 Ville Skyttä <ville.skytta@iki.fi> - 6.5.2-6jpp
- Rebuild for JPackage 1.5.
- Split shell script to -scripts subpackage.
- Use non-versioned jar in jaxp_transform_impl alternative, and don't remove
  it on upgrade.
- Spec file cleanups.

* Thu Jul 25 2002 Ville Skyttä <ville.skytta@iki.fi> 6.5.2-5jpp
- Fix shell script (again).
- Rebuild with -Dbuild.compiler=modern (saxon-fop won't build with jikes).

* Fri Jul 19 2002 Ville Skyttä <ville.skytta@iki.fi> 6.5.2-4jpp
- First public JPackage release.
- Compile with build.xml by yours truly.
- AElfred no more provides jaxp_parser_impl; it's SAX only, no DOM.
- Fix shell script.

* Mon Jul  1 2002 Ville Skyttä <ville.skytta@iki.fi> 6.5.2-3jpp
- Provides jaxp_parser_impl.
- Requires xml-commons-apis.

* Sun Jun 30 2002 Ville Skyttä <ville.skytta@iki.fi> 6.5.2-2jpp
- Use sed instead of bash 2 extension when symlinking jars.
- Provides jaxp_transform_impl.

* Sat May 11 2002 Ville Skyttä <ville.skytta@iki.fi> 6.5.2-1jpp
- First JPackage release.
- Provides jaxp_parser2 though there's no DOM implementation in this AElfred.
