Name:          glassfish-fastinfoset
Version:       1.2.12
Release:       14%{?dist}
Summary:       Fast Infoset
License:       ASL 2.0
URL:           https://fi.dev.java.net
# svn export https://svn.java.net/svn/fi~svn/tags/1_2_12/ glassfish-fastinfoset-1.2.12
# find glassfish-fastinfoset-1.2.12/ -name '*.class' -delete
# find glassfish-fastinfoset-1.2.12/ -name '*.jar' -delete
# rm -rf glassfish-fastinfoset-1.2.12/roundtrip-tests
# tar czf glassfish-fastinfoset-1.2.12-src-svn.tar.gz glassfish-fastinfoset-1.2.12
Source0:       %{name}-%{version}-src-svn.tar.gz
# add xmlstreambuffer 1.5.x support
Patch0:        %{name}-%{version}-utilities-FastInfosetWriterSAXBufferProcessor.patch

BuildRequires: bea-stax-api
BuildRequires: maven-local
BuildRequires: maven-plugin-jxr
BuildRequires: maven-plugin-tools-api
BuildRequires: maven-project-info-reports-plugin
BuildRequires: maven-release-plugin
BuildRequires: maven-source-plugin
BuildRequires: xsom
BuildRequires: maven-surefire-provider-junit
BuildRequires: jvnet-parent
BuildRequires: xmlstreambuffer

BuildArch:     noarch

%description
Fast Infoset specifies a standardized binary encoding for the XML Information
Set. An XML infoset (such as a DOM tree, StAX events or SAX events in
programmatic representations) may be serialized to an XML 1.x document or, as
specified by the Fast Infoset standard, may be serialized to a fast infoset
document.  Fast infoset documents are generally smaller in size and faster to
parse and serialize than equivalent XML documents.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q
%patch0 -p0
# Remove wagon-webdav
%pom_xpath_remove "pom:build/pom:extensions"

%pom_remove_plugin :findbugs-maven-plugin
%pom_remove_plugin :maven-antrun-extended-plugin

# Replace javax.xml.bind jsr173_api with stax (bea-)stax-api
%pom_remove_dep javax.xml.bind:jsr173_api
%pom_add_dep stax:stax-api:1.0.1

%pom_disable_module roundtrip-tests
%pom_disable_module samples

%build

%mvn_file :FastInfoset %{name}
%mvn_file :FastInfosetUtilities %{name}-utilities
%mvn_build

%install
%mvn_install

%files -f .mfiles

%files javadoc -f .mfiles-javadoc

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 1.2.12-14
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 1.2.12-13
- 为 Magic 3.0 重建

* Thu Aug 14 2014 Liu Di <liudidi@gmail.com> - 1.2.12-12
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.12-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.2.12-10
- Use Requires: java-headless rebuild (#1067528)

* Mon Aug 05 2013 gil cattaneo <puntogil@libero.it> 1.2.12-9
- rebuilt rhbz#992387
- add xmlstreambuffer and jvnet-parent support
- swith to Xmvn
- adapt to new guideline

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 22 2013 Juan Hernandez <juan.hernandez@redhat.com> - 1.2.12-7
- Remove the wagon-webdav build extension (rhbz 914033)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.2.12-5
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 7 2012 Juan Hernandez <juan.hernandez@redhat.com> 1.2.12-3
- Changed name from glassfish-fi to glassfish-fastinfoset

* Tue Feb 14 2012 Juan Hernandez <juan.hernandez@redhat.com> 1.2.12-2
- Cleanup of the spec file

* Sat Jan 21 2012 Marek Goldmann <mgoldman@redhat.com> 1.2.12-1
- Initial packaging
