# Generated from addressable-2.2.6.gem by gem2rpm -*- rpm-spec -*-
%global gem_name addressable

Summary: Improved URI/URL Implementation
Name: rubygem-%{gem_name}
Version: 2.3.8
Release: 3%{?dist}
Group: Development/Languages
License: ASL 2.0
URL: http://addressable.rubyforge.org/
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems)

BuildRequires: rubygems-devel
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(rspec-its)
BuildRequires: rubygem(launchy)
BuildRequires: rubygem(json_pure)

BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Addressable is a replacement for the URI implementation that is part of
Ruby's standard library. It more closely conforms to the relevant RFCs and
adds support for URI and URL templates.

%package doc
Summary: Documentation for %{name}
Group: Documentation

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./* %{buildroot}/

## remove all shebang, set permission to 0644
find .%{gem_instdir}/{Rakefile,lib,spec} -type f | \
  xargs -n 1 sed -i -e '/^#!\/usr\/bin\/env ruby/d'
find .%{gem_instdir}/{Rakefile,lib,spec} -type f | \
  xargs chmod 0644

# Fix conflict causing spec test failure - Only needed if test below is not deleted
#sed -i -e 's#^\([[:blank:]]*class\)[[:blank:]]HTTP*$#\1 AddressableHTTP#' -e 's#URI::HTTP#URI::AddressableHTTP#' .%{gem_instdir}/spec/addressable/uri_spec.rb

# Disable hash test, seems to always fail on koji build instances but works fine w/o
sed -i -e '/should have a different hash from http/,+2 s/^/#/' .%{gem_instdir}/spec/addressable/uri_spec.rb

# Disable Coveralls rubygem we don't package travis-ci right now
sed -i '/[Cc]overalls/d' .%{gem_instdir}/spec/spec_helper.rb

# Remove this test since fails on koji mock builders due to DNS lookup
rm .%{gem_instdir}/spec/addressable/net_http_compat_spec.rb

%check
pushd .%{gem_instdir}

rspec spec/

popd

%files
%dir %{gem_instdir}/
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/LICENSE.txt
%{gem_instdir}/lib/
%{gem_instdir}/data/
%{gem_spec}
%exclude %{gem_cache}
%exclude %{gem_instdir}/%{gem_name}.gemspec

%files doc
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/website
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/tasks
%{gem_instdir}/spec
%{gem_docdir}

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.3.8-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Shawn Starr <spstarr@fedoraproject.org> - 2.3.8-1
- New upstream release, fix some build changes

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 23 2014 Shawn Starr <shawn.starr@rogers.com> - 2.3.6-5
- Fix it harder

* Wed Apr 23 2014 Shawn Starr <shawn.starr@rogers.com> - 2.3.6-4
- Disable test 'Addressable::URI when parsed from 'http://example.com' should have a
  different hash from http://EXAMPLE.com' fails on koji but not in mock

* Wed Apr 23 2014 Shawn Starr <shawn.starr@rogers.com> - 2.3.6-3
- Disable GNU idn ruby bindings fallback to pure, rubygem-idn is dead upstream

* Wed Apr 23 2014 Shawn Starr <shawn.starr@rogers.com> - 2.3.6-2
- minor build issue..

* Wed Apr 23 2014 Shawn Starr <shawn.starr@rogers.com> - 2.3.6-1
- New upstream release

* Fri Feb 07 2014 Shawn Starr <shawn.starr@rogers.com> - 2.3.5-1
- New upstream release

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Josef Stribny <jstribny@redhat.com> - 2.3.2-5
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Tue Feb 19 2013 Shawn Starr <shawn.starr@rogers.com> - 2.3.2-4
- Changes in rubygem rspec packaging, adjust build dependencies accordingly

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Aug 23 2012 Shawn Starr <shawn.starr@rogers.com> - 2.3.2-2
- Fix build issue disable one test due to DNS lookup not available on koji mock builders

* Thu Aug 23 2012 Shawn Starr <shawn.starr@rogers.com> - 2.3.2-1
- Bump to latest upstream
- Fix spec test due to namespace/classname conflict

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 09 2012 Shawn Starr <shawn.starr@rogers.com> - 2.2.6-3
- Remove patch passes all tests now.

* Sun Nov 06 2011 Shawn Starr <shawn.starr@rogers.com> - 2.2.6-2
- Fix up package from bugzilla reviews

* Tue Jul 19 2011 Shawn Starr <shawn.starr@rogers.com> - 2.2.6-1
- Bump to latest upstream
- Overhall spec, split -doc packaging 
- Fix loader path to idn.so extension

* Thu Apr 01 2010 Adam Young <ayoung@ayoung.boston.devel.redhat.com> - 2.1.1-1
- Initial package
