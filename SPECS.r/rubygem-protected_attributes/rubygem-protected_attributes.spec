# Generated from protected_attributes-1.0.3.gem by gem2rpm -*- rpm-spec -*-
%global gem_name protected_attributes

Name: rubygem-%{gem_name}
Version: 1.1.0
Release: 2%{?dist}
Summary: Protect attributes from mass assignment in Active Record models
Group: Development/Languages
License: MIT
URL: https://github.com/rails/protected_attributes
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/rails/protected_attributes.git && cd protected_attributes && git checkout v1.1.0
# tar czvf protected_attributes-1.1.0-tests.tgz test/
Source1: %{gem_name}-%{version}-tests.tgz
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(activerecord)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(mocha)
BuildRequires: rubygem(railties)
BuildRequires: rubygem(sqlite3)
BuildArch: noarch

%description
Protect attributes from mass assignment.


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

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
tar xzvf %{SOURCE1}

# Remove Bundler. It just complicates everything.
sed -i "/require 'bundler\/setup'/ s/^/#/" test/test_helper.rb

ruby -Ilib:test -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
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

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.1.0-2
- 为 Magic 3.0 重建

* Thu Jun 25 2015 Vít Ondruch <vondruch@redhat.com> - 1.1.0-1
- Update to protected_attributes 1.1.0.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 18 2014 Vít Ondruch <vondruch@redhat.com> - 1.0.8-1
- Updated to protected_attributes 1.0.8.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Aug 16 2013 Vít Ondruch <vondruch@redhat.com> - 1.0.3-1
- Initial package
