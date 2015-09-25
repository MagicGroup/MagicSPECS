# Initially Generated from mechanize-0.8.5.gem by gem2rpm -*- rpm-spec -*-

%global	majorver		2.7.3
%undefine	preminorver	
%global	rpmminorver		.%(echo %preminorver | sed -e 's|^\\.\\.*||')
%global	fullver		%{majorver}%{?preminorver}

%global	fedorarel		3

%global	gem_name		mechanize

%global	gem_instdir	%{gem_dir}/gems/%{gem_name}-%{version}%{?preminorver}

%if 0%{?fedora} >= 21
%global	gem_minitest	rubygem(minitest4)
%else
%global	gem_minitest	rubygem(minitest)
%endif

Summary:	A handy web browsing ruby object
Name:		rubygem-%{gem_name}
Version:	%{majorver}
Release:	%{?preminorver:0.}%{fedorarel}%{?preminorver:%{rpmminorver}}%{?dist}.2
Group:		Development/Languages
License:	MIT
URL:		http://mechanize.rubyforge.org/
Source0:	https://rubygems.org/gems/%{gem_name}-%{fullver}.gem
# Kill ntlm-http support
# https://github.com/sparklemotion/mechanize/issues/282
Patch0:	rubygem-mechanize-2.6.0-disable-ntlm-http.patch
Patch1:	rubygem-mechanize-2.6.0-disable-ntlm-http-test.patch
# https://github.com/sparklemotion/mechanize/commit/f4a097743ca975476b3766c65c5d58e21e8ec47.patch
Patch2:	rubygem-mechanize-2.7.x-test-unit-5.x.patch
# https://github.com/sparklemotion/mechanize/commit/95f995d0e52386492fe5bedcfeaaca60726f5b54.patch
# And 2 commits
Patch3:	rubygem-mechanize-2.7.3-mime-type-2.x.patch

BuildRequires:	ruby(release)
BuildRequires:	ruby-devel
BuildRequires:	rubygems-devel
# For %%check
BuildRequires:	rubygem(domain_name)
BuildRequires:	rubygem(http-cookie)
BuildRequires:	rubygem(mime-types)
BuildRequires:	rubygem(net-http-digest_auth)
BuildRequires:	rubygem(net-http-persistent)
BuildRequires:	rubygem(nokogiri)
#BuildRequires:	rubygem(ntlm-http)
BuildRequires:	rubygem(webrobots)
BuildRequires:	%gem_minitest

Requires:	ruby(release)
Requires:	ruby(rubygems)
Requires:	rubygem(domain_name)
Requires:	rubygem(http-cookie)
Requires:	rubygem(mime-types)
Requires:	rubygem(net-http-digest_auth)
Requires:	rubygem(net-http-persistent)
#Requires:	rubygem(ntlm-http)
Requires:	rubygem(nokogiri)
Requires:	rubygem(webrobots)
Provides:	rubygem(%{gem_name}) = %{version}-%{release}
#Requires:	rubygem(hoe)

# For non-gem support, net-http-persistent (which this package depends on)
# must also create non-gem package. Let's kill it (at least for F-15)
Obsoletes:	ruby-%{gem_name} < 1.0.0-999

BuildArch:	noarch

%description
The Mechanize library is used for automating interaction with websites. 
Mechanize automatically stores and sends cookies, follows redirects, 
can follow links, and submit forms. Form fields can be populated and 
submitted. Mechanize also keeps track of the sites that you have 
visited as a history.

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
# Directory ownership issue
Requires:	%{name} = %{version}-%{release}
Requires:	ruby(rubygems)

%description	doc
This package contains documentation for %{name}.

%prep
%setup -q -c -T

TOPDIR=$(pwd)
mkdir tmpunpackdir
pushd tmpunpackdir

gem unpack %{SOURCE0}
cd %{gem_name}-%{version}

# Permission
find . -name \*.rb -print0 | xargs --null chmod 0644

# Patches
%patch0 -p1 -b .ntlm
%patch1 -p1 -b .ntlmtest
%patch2 -p1 -b .unit5 -R
%patch3 -p1 -b .mime2 -R

gem specification -l --ruby %{SOURCE0} > %{gem_name}.gemspec
# Kill ntlm-http dependency
sed -i -e '\@ntlm-http@d' %{gem_name}.gemspec
# Also change mime-type dependency
sed -i -e '\@mime-type@s|"~> 2.0"|"~> 1.17"|' %{gem_name}.gemspec


gem build %{gem_name}.gemspec
mv %{gem_name}-%{version}.gem $TOPDIR

popd
rm -rf tmpunpackdir

%build
mkdir -p .%{gem_dir}

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}

# Clean up
rm -f %{buildroot}%{gem_instdir}/{.autotest,.gemtest,.travis.yml}

%check
pushd ./%{gem_instdir}

# http://pkgs.fedoraproject.org/cgit/openssl.git/tree/openssl-1.0.1e-no-md5-verify.patch
# TODO: need "correct" solution
%if 0%{?fedora} >= 21
export OPENSSL_ENABLE_MD5_VERIFY=yes
%endif

ruby -Ilib:. -e 'gem "minitest", "<5" ; Dir.glob("test/test_*.rb").each {|f| require f}'
popd

%files
%defattr(-,root,root,-)
%doc	%{gem_instdir}/[A-Z]*.rdoc
%exclude %{gem_instdir}/Rakefile
%exclude %{gem_instdir}/Manifest.txt
%dir	%{gem_instdir}
%{gem_libdir}/
%exclude	%{gem_cache}
%{gem_spec}

%files	doc
%defattr(-,root,root,-)
%{gem_dir}/doc/%{gem_name}-%{fullver}/
#%%{gem_instdir}/Rakefile
#%%{gem_instdir}/Manifest.txt
%{gem_instdir}/examples/
%exclude	%{gem_instdir}/test/

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.7.3-3.2
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.3-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 12 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.7.3-3
- Force to use minitest ver4 for now

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.3-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 27 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.7.3-2
- Also modify mime-type dependency on spec (bug 1080855)

* Mon Nov 18 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.7.3-1
- 2.7.3

* Mon Nov 11 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.7.2-1
- 2.7.2

* Thu Oct 17 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.6.0-1
- Update to 2.6.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-0.5.beta.20110107104205.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 26 2013 Vít Ondruch <vondruch@redhat.com> - 1.0.1-0.5.beta.20110107104205
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-0.4.beta.20110107104205.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-0.4.beta.20110107104205.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 07 2012 Vít Ondruch <vondruch@redhat.com> - 1.0.1-0.4.beta.20110107104205
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-0.3.beta.20110107104205.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 10 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.0.1-0.3.beta.20110107194205
- Allow net-http-persistent 2.x

* Thu Feb 10 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.0.1-0.2.beta.20110107104205
- Bump release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-0.1.beta.20110107104205.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 23 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.0.1-0.1.beta.20110107104205
- 1.0.1.beta.20110107104205
- Kill non-gem support (at least for F-15)

* Wed Feb 10 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.0.0-2
- 1.0.0
- Fix permission
- F-11: Kill one failing test due to old (< 1.4.0) nokogiri

* Sat Jul 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.9.3-2
- F-12: Mass rebuild

* Thu Jun 11 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.9.3-1
- 0.9.3

* Thu Mar 12 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.9.2-1
- 0.9.2

* Thu Feb 26 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.9.1-1
- 0.9.1

* Tue Feb 24 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.9.0-3
- F-11: Mass rebuild

* Tue Jan 20 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.9.0-2
- Some cleanup

* Thu Dec 25 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.9.0-1
- 0.9.0
- Dependency changed: hpricot -> nokogiri

* Sun Dec 21 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.8.5-2
- Switch to Gem

* Wed Nov 26 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.8.5-1
- 0.8.5

* Wed Oct  8 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.8.4-1
- 0.8.4

* Wed Oct  1 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.8.3-1
- 0.8.3

* Thu Sep 25 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.8.0-1
- 0.8.0

* Thu Aug 28 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.7.8-1
- 0.7.8

* Thu Jul 31 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.7.7-1
- 0.7.7

* Thu May 22 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.7.6-1
- 0.7.6

* Thu Mar 20 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.7.5-1
- 0.7.5

* Thu Mar  6 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.7.1-1
- 0.7.1

* Thu Jan 17 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.7.0-1
- 0.7.0

* Thu Dec 13 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.6.11-1
- 0.6.11

* Fri Nov  9 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.6.10-3
- More cleanup

* Sat Nov  3 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.6.10-2
- BR: ruby
- Remove unneeded CFLAGS

* Sat Nov  3 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.6.10-1
- 0.6.10

* Fri Jun  8 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.6.8-1
- Initial packaging
