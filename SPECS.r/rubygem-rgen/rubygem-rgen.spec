%global gem_name rgen

Name: rubygem-%{gem_name}
Version: 0.7.0
Release: 1%{?dist}
Summary: Ruby Modelling and Generator Framework
Group: Development/Languages
License: MIT
URL: https://github.com/mthiede/rgen
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Use a value larger than Fixnum max to test Bignum support.
# https://github.com/mthiede/rgen/pull/18
Patch0: rubygem-rgen-0.7.0-Use-a-value-larger-than-Fixnum-max-to-test-Bignum-support.patch
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(nokogiri)
BuildRequires: rubygem(test-unit)
BuildArch: noarch

%description
RGen is a framework for Model Driven Software Development (MDSD) in Ruby. This
means that it helps you build Metamodels, instantiate Models, modify and
transform Models and finally generate arbitrary textual content from it.

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

%patch0 -p1

%build
gem build %{gem_name}.gemspec

%gem_install

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Fix line endings.
sed -i 's:\r::' %{buildroot}%{gem_instdir}/CHANGELOG

%check
pushd .%{gem_instdir}
RUBYOPT=-rubygems ruby test/rgen_test.rb
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/MIT-LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/CHANGELOG
%{gem_instdir}/test
%{gem_instdir}/Rakefile

%changelog
* Tue Jul 14 2015 Vít Ondruch <vondruch@redhat.com> - 0.7.0-1
- Update to RGen 0.7.0.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jan 22 2014 Sam Kottler <shk@redhat.com> - 0.6.6-2
- Fixes based on review feedback

* Mon Jan 06 2014 Sam Kottler <shk@redhat.com> - 0.6.6-1
- Initial package
