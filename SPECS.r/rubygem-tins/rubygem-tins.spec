# Generated from tins-0.8.3.gem by gem2rpm -*- rpm-spec -*-
%global gem_name tins

Name: rubygem-%{gem_name}
Version: 1.0.0
Release: 6%{?dist}
Summary: Useful tools library in Ruby
Group: Development/Languages
License: MIT
URL: http://github.com/flori/tins
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems)
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(test-unit)
BuildRequires: rubygem(simplecov)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
All the stuff that isn't good/big enough for a real library.

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
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Remove uneeded files
rm -rf %{buildroot}%{gem_instdir}/{Gemfile,Rakefile,TODO,VERSION,%{gem_name}.gemspec,.gitignore,.travis.yml}

# Fix shebang
pushd %{buildroot}%{gem_instdir}

for test in mail null_pattern turing; do
  sed -i '1i #!/usr/bin/env ruby' examples/$test.rb
done

popd

%check
pushd .%{gem_instdir}
ruby -rtest-unit -e 'Test::Unit::AutoRunner.run(true)' -Ilib tests/
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%doc %{gem_instdir}/COPYING
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.rdoc
%{gem_instdir}/tests/
%{gem_instdir}/examples

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.0.0-6
- 为 Magic 3.0 重建

* Mon Jun 22 2015 Yaakov Selkowitz <yselkowi@redhat.com> - 1.0.0-5
- Fix test-unit usage for F22+

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Feb 23 2014 Achilleas Pipinellis <axilleas@fedoraproject.org> - 1.0.0-2
- Fix rpmlint errors/warnings

* Sun Feb 23 2014 Achilleas Pipinellis <axilleas@fedoraproject.org> - 1.0.0-1
- Bump to 1.0.0
- Do some cleanup

* Mon Jan 27 2014 Achilleas Pipinellis <axilleas@fedoraproject.org> - 0.13.1-1
- Bump to 0.13.1

* Wed Aug 14 2013 Axilleas Pipinellis <axilleas@fedoraproject.org> - 0.8.4-2
- Add forgotten changelog

* Tue Aug 13 2013 Axilleas Pipinellis <axilleas@fedoraproject.org> - 0.8.4-1
- Version bump

* Tue Aug 13 2013 Axilleas Pipinellis <axilleas@fedoraproject.org> - 0.8.3-1
- Initial package
