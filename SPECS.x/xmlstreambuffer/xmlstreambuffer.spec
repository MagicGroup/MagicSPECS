Name:          xmlstreambuffer
Version:       1.5.1
Release:       5%{?dist}
Summary:       XML Stream Buffer
License:       CDDL or GPLv2 with exceptions
Url:           http://java.net/projects/xmlstreambuffer/
# svn export https://svn.java.net/svn/xmlstreambuffer~svn/tags/streambuffer-1.5.1/ xmlstreambuffer-1.5.1
# find xmlstreambuffer-1.5.1/ -name '*.class' -delete
# find xmlstreambuffer-1.5.1/ -name '*.jar' -delete
# find xmlstreambuffer-1.5.1/ -name '*.zip' -delete
# tar czf xmlstreambuffer-1.5.1-src-svn.tar.gz xmlstreambuffer-1.5.1
Source0:       %{name}-%{version}-src-svn.tar.gz
# wget -O glassfish-LICENSE.txt https://svn.java.net/svn/glassfish~svn/tags/legal-1.1/src/main/resources/META-INF/LICENSE.txt
# xmlstreambuffer package don't include the license file
Source1:       glassfish-LICENSE.txt

BuildRequires: java-devel
BuildRequires: jvnet-parent

BuildRequires: maven-local
BuildRequires: maven-enforcer-plugin
BuildRequires: maven-surefire-provider-junit

BuildRequires: bea-stax-api
BuildRequires: stax-ex >= 1.7.1

# test deps
BuildRequires: junit
BuildRequires: woodstox-core

BuildArch:     noarch

%description
A stream buffer is a stream-based representation of an XML
info-set in Java. Stream buffers are designed to: provide
very efficient stream-based memory representations of XML
info-sets; and be created and processed using any Java-based
XML API.
Conceptually a stream buffer is similar to the representation
used in the Xerces deferred DOM implementation, with the crucial
difference that a stream buffer does not store hierarchical
information like parent and sibling information. The deferred
DOM implementation reduces memory usage when large XML documents
are parsed but only a subset of the document needs to be processed.
(Note that using deferred DOM will be more expensive than
non-deferred DOM in terms of memory and processing if all
the document is traversed.)
Stream buffers may be used as an efficient alternative to DOM where:
* most or all of an XML info-set will eventually get traversed; and/or
* targeted access to certain parts of an XML info-set are required
 and need to be efficiently processed using stream-based APIs like
 SAX or StAX.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q

%pom_remove_dep javax.activation:activation
sed -i "s|<artifactId>wstx-asl</artifactId>|<artifactId>woodstox-core-asl</artifactId>|" pom.xml

cp -p %{SOURCE1} LICENSE.txt
sed -i 's/\r//' LICENSE.txt

%mvn_file :streambuffer %{name}

%build

%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE.txt

%files -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.5.1-4
- Use Requires: java-headless rebuild (#1067528)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 29 2013 gil cattaneo <puntogil@libero.it> 1.5.1-2
- switch to XMvn, minor changes to adapt to current guideline

* Tue Oct 30 2012 gil cattaneo <puntogil@libero.it> 1.5.1-1
- update to 1.5.1

* Wed Oct 03 2012 gil cattaneo <puntogil@libero.it> 1.5-1
- update to 1.5

* Sat Mar 31 2012 gil cattaneo <puntogil@libero.it> 1.4-1
- initial rpm
