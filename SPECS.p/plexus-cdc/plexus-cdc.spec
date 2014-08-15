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

%global parent plexus

%global subname cdc

Name:           %{parent}-%{subname}
Version:        1.0
Release:        0.21.a14%{?dist}
Epoch:          0
Summary:        Plexus Component Descriptor Creator
# Almost whole gleaner subpackage is ASL 2.0
License:        MIT and ASL 2.0
Group:          Development/Tools
URL:            http://plexus.codehaus.org/
# svn export -r 7728 http://svn.codehaus.org/plexus/archive/plexus-tools/tags/plexus-tools-1.0.11/plexus-cdc plexus-cdc
# tar czf plexus-cdc-1.0-alpha-14.tar.gz plexus-cdc/
Source0:        %{name}-1.0-alpha-14.tar.gz
Source1:        %{name}-jpp-depmap.xml
Source2:        http://www.apache.org/licenses/LICENSE-2.0.txt
Patch0:         %{name}-qdox-1.9.patch

BuildArch:      noarch

BuildRequires:  jpackage-utils >= 0:1.7.2
BuildRequires:  maven-local
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  jdom
BuildRequires:  plexus-utils
BuildRequires:  maven-doxia-sitetools
BuildRequires:  qdox


%description
The Plexus project seeks to create end-to-end developer tools for
writing applications. At the core is the container, which can be
embedded or for a full scale application server. There are many
reusable components for hibernate, form processing, jndi, i18n,
velocity, etc. Plexus also includes an application server which
is like a J2EE application server, without all the baggage.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}
cp -p %{SOURCE2} .

%patch0 -p1

%build
%mvn_file  : %{parent}/%{subname}
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc LICENSE-2.0.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE-2.0.txt

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.21.a14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.0-0.20.a14
- Use Requires: java-headless rebuild (#1067528)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.19.a14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.18.a14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0:1.0-0.17.a14
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jan 17 2013 Michal Srb <msrb@redhat.com> - 0:1.0-0.16.a14
- Build with xmvn

* Mon Dec 10 2012 Michal Srb <msrb@redhat.com> - 0:1.0-0.15.a14
- Removed dependency to plexus-container-default (Resolves: #878570)
- Removed forgotten older tarball from sources file
- Fixed various rpmlint warnings

* Mon Nov 26 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.0-0.14.a14
- Install license files
- Resolves: rhbz#880206

* Fri Oct  5 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.0-0.13.a14
- Fix license to MIT and ASL 2.0
- Small cleanups in packaging, update to current guidelines

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.12.a14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.11.a14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 12 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.10.a14
- Build with maven 3.x

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.9.a14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jun 24 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.0-0.8.a14
- Update qdox patch

* Thu Jun 24 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.0-0.7.a14
- Update to latest version, update qdox patch
- Cleanup specfile a bit, fix release tag

* Thu Nov 26 2009 Lubomir Rintel <lkundrak@v3.sk> 0:1.0-0.6.a10.1.3
- Fix NULL dereference in the qdox patch

* Mon Nov 23 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.5.a10.1.3
- BR maven-doxia-sitetools.

* Mon Nov 23 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.5.a10.1.2
- Fix build with qdox 1.9.

* Thu Aug 20 2009 Andrew Overholt <overholt@redhat.com> 1.0-0.5.a10.1.1
- Update to alpha 10 (courtesy Deepak Bhole)
- Remove gcj support

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.4.a4.1.7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 23 2009 Deepak Bhole <dbhole@redhat.com> - 0:1.0-0.3.a4.1.7
- Build on ppc64

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.3.a4.1.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.0-0.2.a4.1.6
- drop repotag

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.0-0.2.a4.1jpp.5
- Fix license tag

* Thu Feb 28 2008 Deepak Bhole <dbhole@redhat.com> 1.0-0.2.a4.1jpp.4
- Rebuild

* Fri Sep 21 2007 Deepak Bhole <dbhole@redhat.com> 0:1.0-0.1.a4.2jpp.3
- ExcludeArch ppc64

* Tue Mar 20 2007 Deepak Bhole <dbhole@redhat.com> 0:1.0-0.1.a4.2jpp.2
- Enable gcj

* Tue Feb 20 2007 Tania Bento <tbento@redhat.com> 0:1.0-0.1.a4.2jpp.1
- Fixed %%Release.
- Fixed %%BuildRoot.
- Removed %%Vendor.
- Removed %%Distribution.
- Edited instructions on how to generate the source drops.
- Removed %%post and %%postun sections for javadoc.
- Added gcj support.

* Tue Oct 17 2006 Deepak Bhole <dbhole@redhat.com> 1.0-0.a4.2jpp
- Update for maven2 9jpp

* Mon Jun 12 2006 Deepak Bhole <dbhole@redhat.com> - 0:1.0-0.a4.1jpp
- Initial build
