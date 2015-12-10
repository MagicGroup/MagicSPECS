# Generated from omniauth-1.1.4.gem by gem2rpm -*- rpm-spec -*-
%global gem_name omniauth

Name: rubygem-%{gem_name}
Version: 1.2.1
Release: 7%{?dist}
Summary: A generalized Rack framework for multiple-provider authentication
Group: Development/Languages
License: MIT
URL: http://github.com/intridea/omniauth
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel >= 1.3.6
BuildRequires: ruby
BuildRequires: rubygem(hashie)
BuildRequires: rubygem(rack-test)
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(simplecov)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
A generalized Rack framework for multiple-provider authentication.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

# Remove unneeded coveralls gem from test suite
sed -i '/[Cc]overalls/d' %{_builddir}/%{gem_name}-%{version}/spec/helper.rb

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Remove uneeded files
rm -rf %{buildroot}%{gem_instdir}/{Gemfile{,.rack-1.3.x},Rakefile,Guardfile,\
.gemtest,.gitignore,.rspec,.rubocop.yml,.travis.yml,.yardopts,\
%{gem_name}.gemspec}

%check
pushd .%{gem_instdir}
rspec spec/
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE.md
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/certs/
%{gem_libdir}
%{gem_spec}
%exclude %{gem_cache}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/spec/

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 1.2.1-7
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.2.1-6
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.2.1-5
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jul 04 2014 Achilleas Pipinellis <axilleas@fedoraproject.org> - 1.2.1-3
- Rebuilt for BZ#1107183
- Drop Requires (ruby 2.1 guidelines)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Feb 23 2014 Achilleas Pipinellis <axilleas@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1

* Tue Aug 27 2013 Axilleas Pipinellis <axilleaspi@ymail.com> - 1.1.4-2
- Remove set of noarch in -doc subpackage
- Move removal of coveralls gem to %prep
- Move README.md to main package

* Sun Jul 28 2013 Axilleas Pipinellis <axilleaspi@ymail.com> - 1.1.4-1
- Initial package
