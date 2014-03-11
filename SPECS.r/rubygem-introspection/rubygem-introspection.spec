# Generated from introspection-0.0.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name introspection


Summary: Dynamic inspection of the hierarchy of method definitions on a Ruby object
Name: rubygem-%{gem_name}
Version: 0.0.2
Release: 8%{?dist}
Group: Development/Languages
# https://github.com/floehopper/introspection/issues/1
License: MIT
URL: http://jamesmead.org
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# Remove instantiator dependency.
# https://github.com/floehopper/introspection/issues/2
Patch0: %{name}-%{version}-update-dep.patch
Requires: ruby(release)
Requires: ruby(rubygems) >= 1.3.6
Requires: ruby
Requires: rubygem(metaclass) => 0.0.1
Requires: rubygem(metaclass) < 0.1
# Seems to be useless ATM.
# https://github.com/floehopper/introspection/issues/2
# Requires: rubygem(instantiator) => 0.0.3
# Requires: rubygem(instantiator) < 0.1
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(metaclass) => 0.0.1
BuildRequires: rubygem(metaclass) < 0.1
# Required to satisfy the 'blankslate' require. May be replaced
# by rubygem(blankslate) when available in Fedora.
BuildRequires: rubygem(builder)
BuildRequires: rubygem(minitest)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Dynamic inspection of the hierarchy of method definitions on a Ruby object


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}


%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

pushd .%{gem_dir}
%patch0 -p0
popd

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
# Disable Bundler
sed -i '2,2d' test/test_helper.rb
testrb -Ilib test/*_test.rb
popd


%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/.travis.yml
%exclude %{gem_instdir}/introspection.gemspec
%{gem_libdir}
%{gem_instdir}/test
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_instdir}/README.md
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/samples
%doc %{gem_docdir}


%changelog
* Mon Feb 25 2013 Vít Ondruch <vondruch@redhat.com> - 0.0.2-8
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 19 2012 Vít Ondruch <vondruch@redhat.com> - 0.0.2-5
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 04 2011 Vít Ondruch <vondruch@redhat.com> - 0.0.2-3
- Fix BuildRequires and test suite.
- Move README.md into -doc subpackage and mark it properly.

* Tue Oct 04 2011 Vít Ondruch <vondruch@redhat.com> - 0.0.2-2
- Clarified license.

* Mon Oct 03 2011 Vít Ondruch <vondruch@redhat.com> - 0.0.2-1
- Initial package
