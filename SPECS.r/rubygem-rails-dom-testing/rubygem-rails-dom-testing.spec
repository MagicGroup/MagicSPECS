# Generated from rails-dom-testing-1.0.5.gem by gem2rpm -*- rpm-spec -*-
%global gem_name rails-dom-testing

Name: rubygem-%{gem_name}
Version: 1.0.5
Release: 5%{?dist}
Summary: Compares doms and assert certain elements exists in doms using Nokogiri
Group: Development/Languages
License: MIT
URL: https://github.com/kaspth/rails-dom-testing
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel 
BuildRequires: ruby 
BuildRequires: rubygem(activesupport) 
BuildRequires: rubygem(nokogiri) 
BuildRequires: rubygem(minitest) 
BuildRequires: rubygem(rails-deprecated_sanitizer)
BuildArch: noarch

%description
Dom and Selector assertions for Rails applications.


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

# Relax AS dependency.
sed -i '/activesupport/ s/4.2.0/4.1.0/' %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/




# Run the test suite
%check
pushd .%{gem_instdir}
# ActiveSupport::TestCase.test_order is not available in AS 4.1.
sed -i "/\.test_order/ s/^/#/" test/test_helper.rb

ruby -Ilib:test -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd

%files
%license %{gem_instdir}/LICENSE.txt
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/test

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 1.0.5-5
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.0.5-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.0.5-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 22 2015 Vít Ondruch <vondruch@redhat.com> - 1.0.5-1
- Initial package
