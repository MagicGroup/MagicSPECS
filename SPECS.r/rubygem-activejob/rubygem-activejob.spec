# Generated from activejob-4.2.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name activejob

Name: rubygem-%{gem_name}
Version: 4.2.4
Release: 4%{?dist}
Summary: Job framework with pluggable queues
Group: Development/Languages
License: MIT
URL: http://www.rubyonrails.org
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/rails/rails.git && cd rails/activejob && git checkout v4.2.4
# tar czvf activejob-4.2.4-tests.tgz test/
Source1: %{gem_name}-%{version}-tests.tgz
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 1.9.3
BuildRequires: rubygem(activesupport)
BuildRequires: rubygem(globalid)
BuildArch: noarch

%description
Declare job classes that can be run by a variety of queueing backends.


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




# Run the test suite
%check
pushd .%{gem_instdir}
tar xzvf %{SOURCE1}

# ActiveSupport::TestCase.test_order is not available in AS 4.1.
sed -i "/\.test_order/ s/^/#/" test/helper.rb

# This is just helper used in official repository.
sed -i "/load_paths/ s/^/#/" test/helper.rb

# Do not exexute integration tests, otherwise Railse's generators are requires.
AJ_ADAPTER=inline ruby -Ilib:test -e 'Dir.glob "./test/cases/**/*_test.rb", &method(:require)'
popd

%files
%license %{gem_instdir}/MIT-LICENSE
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.md

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 4.2.4-4
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 4.2.4-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 4.2.4-2
- 为 Magic 3.0 重建

* Wed Aug 26 2015 Josef Stribny <jstribny@redhat.com> - 4.2.4-1
- Update to activejob 4.2.4

* Tue Jun 30 2015 Josef Stribny <jstribny@redhat.com> - 4.2.3-1
- Update to activejob 4.2.3

* Mon Jun 22 2015 Josef Stribny <jstribny@redhat.com> - 4.2.2-1
- Update to activejob 4.2.2

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 20 2015 Josef Stribny <jstribny@redhat.com> - 4.2.1-1
- Update to activejob 4.2.1

* Thu Jan 22 2015 Vít Ondruch <vondruch@redhat.com> - 4.2.0-1
- Initial package
