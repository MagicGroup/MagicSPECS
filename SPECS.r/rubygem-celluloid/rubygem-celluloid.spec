# Generated from celluloid-0.15.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name celluloid

Name: rubygem-%{gem_name}
Version: 0.16.0
Release: 1%{?dist}
Summary: Actor-based concurrent object framework for Ruby
Group: Development/Languages
License: MIT
URL: https://github.com/celluloid/celluloid
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(rspec) < 3
BuildRequires: rubygem(timers)
BuildArch: noarch

%description
Celluloid enables people to build concurrent programs out of concurrent
objects just as easily as they build sequential programs out of sequential
objects.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


%check
pushd .%{gem_instdir}

# Disable code coverrage.
sed -i '/overalls/ s/^/#/' spec/spec_helper.rb

# Get rid of Bundler.
sed -i '/bundler/ s/^/#/' spec/spec_helper.rb

# Test suite expect log directory to exist.
mkdir log

rspec2 spec
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE.txt
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/spec

%changelog
* Mon Jun 22 2015 Vít Ondruch <vondruch@redhat.com> - 0.16.0-1
- Update to Celluloid 0.16.0.
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Sep 01 2014 Vít Ondruch <vondruch@redhat.com> - 0.15.2-2
- spec/support is needed by runtime.

* Thu Aug 28 2014 Vít Ondruch <vondruch@redhat.com> - 0.15.2-1
- Initial package
