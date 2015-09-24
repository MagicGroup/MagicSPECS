# Generated from faraday-0.8.7.gem by gem2rpm -*- rpm-spec -*-
%global gem_name faraday

Name: rubygem-%{gem_name}
Version: 0.9.0
Release: 2%{?dist}
Summary: HTTP/REST API client library
Group: Development/Languages
License: MIT
URL: https://github.com/lostisland/faraday
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
# Don't install these until test suite can be ran again. See %%check below
#BuildRequires: wget
#BuildRequires: lsof
#BuildRequires: rubygem(sinatra)
#BuildRequires: rubygem(minitest)
BuildRequires: rubygem(multipart-post) => 1.2
BuildRequires: rubygem(multipart-post) < 3
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildArch: noarch

# Filter from RPM's autorequires.
%global __requires_exclude ^/usr/bin/env$

%description
HTTP/REST API client library

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

# Remove unnecessary files
pushd .%{gem_instdir}/
  rm %{gem_name}.gemspec
  rm Gemfile
  rm Rakefile
  rm .document
popd

%install

mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
# The test suite is ran by a custom bash script.
# Skip test check until this is resolved.
# https://github.com/lostisland/faraday/blob/v0.9.0/script/test
#ruby -Ilib:test -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%{gem_spec}
%doc %{gem_instdir}/LICENSE.md
%doc %{gem_instdir}/README.md
%exclude %{gem_cache}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/CHANGELOG.md
%{gem_instdir}/CONTRIBUTING.md
%{gem_instdir}/script
%{gem_instdir}/test

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 17 2014 Achilleas Pipinellis <axilleas@fedoraproject.org> - 0.9.0-1
- Bump to 0.9.0
- Remove unessecary files

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Nov 17 2013 Achilleas Pipinellis <axilleaspi@ymail.com> - 0.8.8-2
- Remove multibytes.txt
- Remove Gemfile, Rakefile from doc macro

* Sun Aug 04 2013 Anuj More - 0.8.8-1
- From 0.8.7 to 0.8.8

* Tue May 14 2013 Anuj More - 0.8.7-1
- Initial package
