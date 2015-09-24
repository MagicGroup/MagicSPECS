%global gem_name dalli

# Depends on Rails and its needed by Rails
%global enable_test 1

Name: rubygem-%{gem_name}
Version: 2.7.4
Release: 2%{?dist}
Summary: High performance memcached client for Ruby
Group: Development/Languages
License: MIT
URL: http://github.com/mperham/dalli
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
%if 0%{enable_test} > 0
BuildRequires: memcached
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(mocha)
BuildRequires: rubygem(rails)
%endif
BuildRequires: ruby
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
High performance memcached client for Ruby


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
%if 0%{enable_test} > 0
pushd .%{gem_instdir}
# connection_pool is not yet in Fedora
sed -i -e '3d' test/test_active_support.rb
sed -i -e '491,506d' test/test_active_support.rb

ruby -Ilib:test -e "Dir.glob('./test/test_*.rb').sort.each{ |x| require x }"
popd
%endif

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/LICENSE

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/Performance.md
%doc %{gem_instdir}/History.md
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/Rakefile
%{gem_instdir}/Gemfile
%{gem_instdir}/test


%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 18 2015 Josef Stribny <jstribny@redhat.com> - 2.7.4-1
- Update to 2.7.4

* Mon Jun 16 2014 Josef Stribny <jstribny@redhat.com> - 2.7.2-2
- Fix the test the right way

* Mon Jun 16 2014 Josef Stribny <jstribny@redhat.com> - 2.7.2-1
- Update to dalli 2.7.2

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug 08 2013 Josef Stribny <jstribny@redhat.com> - 2.6.4-2
- Enable tests

* Wed Jul 31 2013 Josef Stribny <jstribny@redhat.com> - 2.6.4-1
- Initial package
