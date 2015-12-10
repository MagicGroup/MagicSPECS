# Generated from sprockets-rails-2.0.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name sprockets-rails

Name: rubygem-%{gem_name}
Version: 2.3.2
Release: 4%{?dist}
Summary: Sprockets Rails integration
Group: Development/Languages
License: MIT
URL: https://github.com/rails/sprockets-rails
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Get the tests
# git clone https://github.com/rails/sprockets-rails.git && cd sprockets-rails/
# git checkout v2.3.2
# tar czvf sprockets-rails-2.3.2-tests.tgz test/
Source2: sprockets-rails-%{version}-tests.tgz
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(railties) >= 3.0
BuildRequires: rubygem(rake)
BuildRequires: rubygem(sprockets)
BuildArch: noarch

%description
Provides Sprockets implementation for Rails 4.x (and beyond) Asset Pipeline.


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
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
# Move the tests into place
tar xzvf %{SOURCE2}

ruby -Ilib -e 'Dir.glob "./test/**/test_*.rb", &method(:require)'
popd


%files
%license %{gem_instdir}/LICENSE
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 2.3.2-4
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2.3.2-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.3.2-2
- 为 Magic 3.0 重建

* Mon Jun 29 2015 Josef Stribny <jstribny@redhat.com> - 2.3.2-1
- Update to 2.3.2

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 18 2015 Josef Stribny <jstribny@redhat.com> - 2.3.1-1
- Update to 2.3.1

* Thu Jan 29 2015 Vít Ondruch <vondruch@redhat.com> - 2.2.4-2
- Drop the boostrap and depend on railties instead of rails.

* Wed Jan 28 2015 Vít Ondruch <vondruch@redhat.com> - 2.2.4-1
- Update to sprockets-rails 2.2.4.

* Fri Jul 04 2014 Vít Ondruch <vondruch@redhat.com> - 2.1.3-1
- Update to sprockets-rails 2.1.3.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 07 2014 Josef Stribny <jstribny@redhat.com> - 2.0.1-1
- Update to 2.0.1

* Thu Aug 08 2013 Josef Stribny <jstribny@redhat.com> - 2.0.0-3
- Enable tests

* Wed Jul 31 2013 Josef Stribny <jstribny@redhat.com> - 2.0.0-2
- Disable tests for now due to broken deps in Rails

* Mon Jul 22 2013 Josef Stribny <jstribny@redhat.com> - 2.0.0-1
- Initial package
