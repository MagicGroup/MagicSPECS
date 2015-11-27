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
%global subname ant-factory

Name:           %{parent}-%{subname}
Version:        1.0
Release:        0.16.a2.2%{?dist}
Epoch:          0
Summary:        Plexus Ant component factory
# Email from copyright holder confirms license.
# See plexus-ant-factory_license_and_copyright.txt
License:        ASL 2.0
Group:          Development/Tools
URL:            http://plexus.codehaus.org/
Source0:        %{name}-src.tar.bz2
# svn export http://svn.codehaus.org/plexus/tags/plexus-ant-factory-1.0-alpha-2.1/ plexus-ant-factory/
# tar cjf plexus-ant-factory-src.tar.bz2 plexus-ant-factory/
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt

BuildArch:      noarch

BuildRequires:  maven-local

BuildRequires:  ant
BuildRequires:  plexus-classworlds
BuildRequires:  plexus-containers-container-default
BuildRequires:  plexus-utils
BuildRequires:  plexus-component-factories-pom


%description
Ant component class creator for Plexus.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}
cp %{SOURCE1} LICENSE


%build
%mvn_file  : %{parent}/%{subname}
%mvn_build

%install
%mvn_install


%pre javadoc
# workaround for rpm bug, can be removed in F-20
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :

%files -f .mfiles
%doc LICENSE
%dir %{_javadir}/plexus

%files javadoc -f .mfiles-javadoc
%doc LICENSE


%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.16.a2.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug  4 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.0-0.15.a2.2
- Fix build-requires on plexus-classworlds

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.15.a2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.0-0.14.a2.1
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 24 2013 Mat Booth <fedora@matbooth.co.uk> - 0:1.0-0.13.a2.1
- Remove unneeded BRs

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.12.a2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0:1.0-0.11.a2.1
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jan 17 2013 Michal Srb <msrb@redhat.com> - 0:1.0-0.10.a2.1
- Build with xmvn
- Added BR on plexus-component-factories-pom

* Mon Dec 10 2012 Michal Srb <msrb@redhat.com> - 0:1.0-0.9.a2.1
- migrated to plexus-containers-container-default (#878580)
- using global is preferred over define when defining macros
- removed not used custom depmap file and its occurrence in spec file
- removed unused Ant buildfile
- fixed release number

* Mon Nov 12 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.0-0.8.a2.1.4
- Add LICENSE-2.0.txt to sources

* Fri Nov  9 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.0-0.8.a2.1.3
- Install ASL 2.0 license file

* Fri Jul  27 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.0-0.8.a2.1.2
- Update to maven 3
- Replace nonstandard groups names with standard ones
- Drop support for non-maven build
- Add workarounds for RPM bug
- Cleanup according to Fedora Packaging Guidelines
- Include missing copyright file in javadoc package

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.7.a2.1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.6.a2.1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.5.a2.1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 23 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.4.a2.1.2
- BR maven-doxia-sitetools.

* Wed Dec 23 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.4.a2.1.1
- Update to 1.0 alpha 2.1.
- Drop gcj_support.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.4.a1.1.11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Feb 28 2009 Deepak Bhole <dbhole@redhat.com> 1.0-0.3.a1.1.11
- Build with maven

* Sat Feb 28 2009 Deepak Bhole <dbhole@redhat.com> - 0:1.0-0.3.a1.1.10
- Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.3.a1.1.9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Aug 13 2008 Deepak Bhole <dbhole@redhat.com> 1.0-0.2.a1.1.9
- Build for ppc64

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0-0.2.a1.1.8
- drop repotag

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.0-0.2.a1.1jpp.7
- include proof of license
- fix license tag

* Thu Feb 28 2008 Deepak Bhole <dbhole@redhat.com> 1.0-0.2.a1.1jpp.6
- Rebuild

* Fri Sep 21 2007 Deepak Bhole <dbhole@redhat.com> 1.0-0.1.a1.2jpp.5
- ExcludeArch ppc64

* Mon Sep 10 2007 Deepak Bhole <dbhole@redhat.com> 1.0-0.1.a1.2jpp.4
- Build with maven

* Fri Aug 31 2007 Deepak Bhole <dbhole@redhat.com> 1.0-0.1.a1.2jpp.3
- Build without maven (to build on ppc)

* Tue Mar 20 2007 Deepak Bhole <dbhole@redhat.com> 1.0-0.1.a1.2jpp.2
- Build with maven

* Fri Feb 23 2007 Tania Bento <tbento@redhat.com> 0:1.0-0.1.a1.2jpp.1
- Fixed %%Release.
- Fixed %%BuildRoot.
- Removed %%Vendor.
- Removed %%Distribution.
- Removed %%post and %%postun sections for javadoc.
- Defined _with_gcj_supoprt and _gcj_support.
- Changed to use cp -p to preserve timestamps.

* Tue Oct 17 2006 Deepak Bhole <dbhole@redhat.com> 1.0-0.a1.2jpp
- Update for maven2 9jpp.

* Thu Sep 07 2006 Deepak Bhole <dbhole@redhat.com> 1.0-0.a1.1jpp
- Initial build
